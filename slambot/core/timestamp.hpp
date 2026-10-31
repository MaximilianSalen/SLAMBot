#pragma once

#include <compare>
#include <cstdint>

namespace slambot::core {

// A sensor time in nanoseconds, as EuRoC and ROS store it. Compare and subtract
// in nanoseconds, and convert to seconds only at the edges (e.g. TUM files).
class Timestamp {
  public:
    constexpr Timestamp() = default;

    static constexpr Timestamp from_nanoseconds(std::int64_t ns) {
        return Timestamp(ns);
    }

    // Rounds to the nearest nanosecond.
    static Timestamp from_seconds(double seconds);

    constexpr std::int64_t nanoseconds() const { return ns_; }

    // A double keeps only about 16 digits, so for Unix-time stamps (~1.4e18 ns)
    // times a few hundred nanoseconds apart give the same seconds.
    constexpr double seconds() const { return static_cast<double>(ns_) / 1e9; }

    friend constexpr auto operator<=>(Timestamp, Timestamp) = default;

  private:
    constexpr explicit Timestamp(std::int64_t ns) : ns_(ns) {}

    std::int64_t ns_ = 0;
};

} // namespace slambot::core
