"""Download datasets for SLAMBot.

    uv run scripts/datasets.py list
    uv run scripts/datasets.py download MH_01_easy V1_01_easy

Datasets go to $SLAMBOT_DATA, or to data/ in the repo. Each EuRoC sequence ends
up in <data>/euroc/<sequence>/mav0 (the ASL format).

EuRoC is only offered as one large zip per environment (machine_hall.zip is
12.7 GB). Each holds one zip per sequence, so we download only the bytes of
that inner zip with HTTP range requests. The download resumes after an
interruption and is checked against the size and CRC-32 listed below.

EuRoC license: "In Copyright - Non-Commercial Use Permitted"
(https://doi.org/10.3929/ethz-b-000690084). Don't commit or share the data.
"""

import argparse
import os
import struct
import sys
import time
import urllib.error
import urllib.request
import zipfile
import zlib
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
USER_AGENT = "SLAMBot-datasets/1.0 (+https://github.com/MaximilianSalen/SLAMBot)"
BITSTREAM_URL = (
    "https://www.research-collection.ethz.ch/server/api/core/bitstreams/{}/content"
)
# ETH Research Collection files of https://doi.org/10.3929/ethz-b-000690084
EUROC_ARCHIVES = {
    "machine_hall": "7b2419c1-62b5-4714-b7f8-485e5fe3e5fe",
    "vicon_room1": "02ecda9a-298f-498b-970c-b7c44334d880",
    "vicon_room2": "ea12bc01-3677-4b4c-853d-87c7870b8c44",
}
CHUNK_SIZE = 1 << 20
RETRIES = 5


@dataclass(frozen=True)
class Sequence:
    name: str
    archive: str
    header_offset: int  # where the inner zip's local file header starts
    compressed_size: int
    size: int
    crc32: int

    @property
    def member(self) -> str:
        return f"{self.archive}/{self.name}/{self.name}.zip"


# Read from the archives' zip directories on 2026-10-31.
EUROC = {
    s.name: s
    for s in [
        Sequence("MH_01_easy", "machine_hall", 8572437937, 1571131855, 1571292346, 0xA1C54DD7),
        Sequence("MH_02_easy", "machine_hall", 5241192924, 1292280179, 1292413952, 0x05BD2C2F),
        Sequence("MH_03_medium", "machine_hall", 11578555345, 1105171496, 1105301873, 0xFD0EFA08),
        Sequence("MH_04_difficult", "machine_hall", 2827222021, 726388661, 726518489, 0xEF013401),
        Sequence("MH_05_difficult", "machine_hall", 1062184285, 828285034, 828426215, 0xC8794414),
        Sequence("V1_01_easy", "vicon_room1", 1540401879, 1149535352, 1149702102, 0x1ABE6A0D),
        Sequence("V1_02_medium", "vicon_room1", 872423291, 667976653, 668079368, 0x369B3AFD),
        Sequence("V1_03_difficult", "vicon_room1", 5241055017, 801206634, 801343542, 0xD12F04FA),
        Sequence("V2_01_easy", "vicon_room2", 2088951459, 882940281, 883081407, 0x53D8D375),
        Sequence("V2_02_medium", "vicon_room2", 161, 898305586, 898452319, 0xC31003DA),
        Sequence("V2_03_difficult", "vicon_room2", 4135028573, 820666078, 820796031, 0xBA8F2BFF),
    ]
}


def data_dir() -> Path:
    return Path(os.environ.get("SLAMBOT_DATA", REPO_ROOT / "data"))


def open_range(url: str, start: int, end: int):
    """Opens the bytes [start, end] of url, retrying on server and network errors."""
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Range": f"bytes={start}-{end}"}
    )
    for attempt in range(RETRIES):
        try:
            response = urllib.request.urlopen(request, timeout=60)
        except urllib.error.HTTPError as e:
            if e.code != 429 and e.code < 500:
                raise
            error = e
        except (urllib.error.URLError, TimeoutError) as e:
            error = e
        else:
            if response.status != 206:
                raise RuntimeError(f"{url} ignored the range request ({response.status})")
            return response
        wait = 2**attempt
        print(f"  {error}, retrying in {wait} s", file=sys.stderr)
        time.sleep(wait)
    raise RuntimeError(f"giving up on {url} after {RETRIES} attempts")


def read_range(url: str, start: int, length: int) -> bytes:
    with open_range(url, start, start + length - 1) as response:
        return response.read()


def data_offset(url: str, seq: Sequence) -> int:
    """Returns where the compressed data starts, after the local file header."""
    header = read_range(url, seq.header_offset, 30)
    signature, name_length, extra_length = struct.unpack("<I22xHH", header)
    if signature != 0x04034B50:
        raise RuntimeError(f"no zip entry at offset {seq.header_offset}, did the archive change?")
    name = read_range(url, seq.header_offset + 30, name_length).decode()
    if name != seq.member:
        raise RuntimeError(f"expected {seq.member} but found {name}, did the archive change?")
    return seq.header_offset + 30 + name_length + extra_length


def download_compressed(url: str, start: int, seq: Sequence, part: Path) -> None:
    """Downloads the compressed bytes to part, resuming where a previous run stopped."""
    while (done := part.stat().st_size if part.exists() else 0) < seq.compressed_size:
        try:
            with open_range(url, start + done, start + seq.compressed_size - 1) as response, part.open("ab") as out:
                while chunk := response.read(CHUNK_SIZE):
                    out.write(chunk)
                    done += len(chunk)
                    print(f"\r  {done / 1e9:.2f} / {seq.compressed_size / 1e9:.2f} GB", end="", flush=True)
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            print(f"\n  {e}, resuming", file=sys.stderr)
    print()
    if done != seq.compressed_size:
        raise RuntimeError(f"{part} has {done} bytes, expected {seq.compressed_size}")


def inflate(part: Path, out_zip: Path, seq: Sequence) -> None:
    """Decompresses part to out_zip and checks its size and CRC-32."""
    decompressor = zlib.decompressobj(-zlib.MAX_WBITS)  # raw deflate, as in zip
    crc, size = 0, 0
    with part.open("rb") as src, out_zip.open("wb") as dst:
        while chunk := src.read(CHUNK_SIZE):
            data = decompressor.decompress(chunk)
            crc, size = zlib.crc32(data, crc), size + len(data)
            dst.write(data)
        data = decompressor.flush()
        crc, size = zlib.crc32(data, crc), size + len(data)
        dst.write(data)
    if size != seq.size or crc != seq.crc32:
        out_zip.unlink()
        part.unlink()
        raise RuntimeError(f"{seq.name} failed the check (size {size}, CRC-32 {crc:08x}), try again")


def extract(inner_zip: Path, dest: Path) -> None:
    """Unpacks into a temporary folder first, so dest never ends up half filled."""
    tmp = dest.with_name(dest.name + ".tmp")
    with zipfile.ZipFile(inner_zip) as z:
        members = [m for m in z.namelist() if not m.startswith("__MACOSX/") and ".DS_Store" not in m]
        z.extractall(tmp, members)  # also checks each file's CRC-32
    tmp.rename(dest)


def download(seq: Sequence) -> None:
    dest = data_dir() / "euroc" / seq.name
    if (dest / "mav0").is_dir():
        print(f"{seq.name}: already in {dest}")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_name(seq.name + ".zip.part")
    inner_zip = dest.with_name(seq.name + ".zip")

    print(f"{seq.name}: downloading {seq.compressed_size / 1e9:.2f} GB")
    url = BITSTREAM_URL.format(EUROC_ARCHIVES[seq.archive])
    download_compressed(url, data_offset(url, seq), seq, part)
    print(f"{seq.name}: checking and unpacking")
    inflate(part, inner_zip, seq)
    part.unlink()
    extract(inner_zip, dest)
    inner_zip.unlink()
    print(f"{seq.name}: ready in {dest}")


def list_sequences() -> None:
    for seq in EUROC.values():
        there = (data_dir() / "euroc" / seq.name / "mav0").is_dir()
        print(f"{seq.name:16s} {seq.size / 1e9:5.2f} GB  {'downloaded' if there else ''}")
    print(f"\nData folder: {data_dir()} (set SLAMBOT_DATA to change it)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="show the EuRoC sequences and which are downloaded")
    get = commands.add_parser("download", help="download EuRoC sequences")
    get.add_argument("sequences", nargs="+", choices=EUROC, metavar="SEQUENCE")
    args = parser.parse_args()

    if args.command == "list":
        list_sequences()
    else:
        for name in args.sequences:
            download(EUROC[name])


if __name__ == "__main__":
    main()
