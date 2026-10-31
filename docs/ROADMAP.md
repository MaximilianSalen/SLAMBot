# SLAMBot roadmap

The plan for learning visual SLAM while building a robot that localizes
robustly. This file holds the plan and the decisions; GitHub issues track the
work. Last updated 2026-10-31.

The project follows Gao & Zhang, *Introduction to Visual SLAM* (2nd ed., also
known as *14 Lectures on Visual SLAM*): [text](https://github.com/gaoxiang12/slambook-en),
[code](https://github.com/gaoxiang12/slambook2). Chapter numbers below match the
book's code folders `ch2` to `ch13`.

Two stages (issue #5): first run on datasets, then on our own robot.

## How we work

- Each phase: read the chapter, try it in `experiments/`, build a module with
  tests, then measure the whole system.
- Get a full pipeline running early (Phase 5). After that, every phase must
  improve a measured number: accuracy (ATE/RPE), robustness or speed.
- The book's code is a reference, not a template. Its chapter 13 system targets
  KITTI (rectified stereo, no IMU) and has design problems we fix (see
  [Architecture](#changes-from-the-books-chapter-13)).
- Robustness matters as much as accuracy: we measure how often tracking is lost
  and how fast it recovers.
- Geometry and optimization code is tested on synthetic data with known answers,
  and every Jacobian is checked against a numerical one.
- We write the core algorithms ourselves. Claude writes infrastructure, tests
  and stubs, and reviews. Tasks below are marked *(us)*, *(pair)* or *(Claude)*.

## Decisions

| | Topic | Choice | Status |
|---|---|---|---|
| D1 | Optimization library | Ceres, plus our own Gauss-Newton and Levenberg-Marquardt for learning | Open, decide in Phase 3 |
| D2 | Viewer | Rerun | Decided |
| D3 | C++ standard | C++20, gcc 11 as the minimum | Decided |
| D4 | Main dataset | EuRoC MAV | Decided |
| D5 | Naming | snake_case | Decided |
| D6 | Place recognition | Our own vocabulary tree first | Decide in Phase 7 |
| D7 | Hardware | See candidates below | Decide in Phase 9 |
| D8 | Sensors | Stereo camera with synced IMU, wheel encoders, optional 2D lidar | Decided |

All decided ones were decided on 2026-10-31.

### D1 Optimization library
Ceres (on ConanCenter) has automatic differentiation, robust losses and
manifolds, and Sophus provides `sophus/ceres_manifold.hpp` for SE(3). g2o, the
book's choice, is not on ConanCenter and its API has changed since the book.
GTSAM hides much of what we want to learn, but can cross-check our IMU code in
Phase 8. Ceres has no marginalization, so we write that ourselves.

### D2 Viewer
Rerun: the program logs timestamped data from any thread, and a separate viewer
shows it live or from a `.rrd` recording. It works the same in Docker, CI and on
the robot, and recordings can be replayed. The library only talks to a
`viz::Visualizer` interface (with a null version for tests), so another viewer
can be added later. One Rerun version is pinned for both the C++ SDK and the
viewer (`rerun-sdk` in `pyproject.toml`). Pangolin, the book's viewer, was
removed.

### D3 C++ standard
C++20. gcc 11 stays the minimum because Jetson boards (JetPack 6, Ubuntu 22.04)
ship it, so we use `fmt` instead of `std::format`. The dev image moves to
Ubuntu 24.04 (gcc 13), and CI keeps a gcc 11 build.

### D5 Naming
- Namespace `slambot::<module>`. Files `snake_case.hpp` / `.cpp`, with tests
  next to the code as `<file>_test.cpp`.
- Types `PascalCase`. Functions and variables `snake_case`. Private and
  protected members end in `_`. Constants and enumerators `kPascalCase`.
- Poses keep the `T_a_b` form (`T_w_c`, member `T_w_c_`).

clang-tidy (`.clang-tidy`) checks this in CI.

### D7 Hardware candidates
- Stereo camera, global shutter, IMU synced in hardware: Luxonis OAK-D,
  Stereolabs ZED Mini / ZED 2i, Intel RealSense D435i / D455.
- Computer: Jetson Orin Nano / NX or Raspberry Pi 5.
- A robot base with wheel encoders we can read. Optionally a cheap 2D lidar.

We record our own data in EuRoC's ASL format, so the same reader works.

### D8 Sensors
For a small wheeled robot, mostly indoors:
- Stereo camera with a hardware-synced IMU. Stereo gives metric scale. The
  IMU keeps tracking through fast motion, blur and darkness. Hardware sync
  avoids the hardest calibration and timing problems.
- Wheel encoders. Nearly free on a wheeled robot. They keep the pose going
  when vision fails and constrain motion when vision is weak.
- 2D lidar (optional). Only as a reference: an existing lidar SLAM gives a
  reference trajectory for our own recordings.

Not planned: 3D lidar, radar, event cameras.

## Architecture

### Modules
Each module is one CMake library, `slambot::<name>`, added when a phase needs
it. A module only depends on modules above it in this table.

| Module | Contents | Phase |
|---|---|---|
| `core` | `Timestamp` (exists), common types | 0–1 |
| `geometry` | Lie group functions, two-view geometry, triangulation, PnP, ICP | 1, 4 |
| `camera` | Camera models, distortion, stereo rectification | 2 |
| `io` | EuRoC reader (later OpenLORIS and our own recordings), trajectory files | 1–2 |
| `eval` | Trajectory alignment, ATE, RPE | 1 |
| `optimization` | Our Gauss-Newton and LM, Ceres helpers | 3 |
| `testing` | Test-only: synthetic scenes, Jacobian checker | 3–4 |
| `features` | Detectors, descriptors, matching, KLT tracking | 4 |
| `map` | `Frame`, `Feature`, `MapPoint`, `Map` | 5 |
| `viz` | `Visualizer` interface, Rerun and null versions | 2 |
| `frontend` | Stereo initialization, tracking, keyframe choice | 5 |
| `backend` | Sliding-window bundle adjustment, later IMU and wheel factors | 6, 8 |
| `loop_closure` | Place recognition, loop verification, pose graph | 7 |
| `system` | Connects the pipeline, synchronous or threaded | 5 |

Data flow: `io` delivers timestamped stereo frames, IMU samples and wheel
odometry. The frontend tracks each frame and passes keyframes to the backend,
which optimizes a sliding window. Loop closure corrects drift across the whole
map. All three share `map`. `viz` and `eval` only observe; the pipeline doesn't
depend on them. Programs in `apps/` parse options and run `system`.

Repository layout:
```
slambot/<module>/   library code, unit tests next to it
apps/               programs, e.g. slambot_run, slambot_eval (planned)
experiments/        book exercises and demos, not part of the library
tests/              integration and regression tests (planned)
config/             YAML settings (planned)
scripts/            datasets.py, later evaluation scripts
cmake/              slambot_add_module(), warnings, sanitizers
docs/               this roadmap, later learning notes
```

### Changes from the book's chapter 13

| Book (`myslam`) | Problem | SLAMBot |
|---|---|---|
| `Config` singleton | Global state, hard to test | Typed config structs, loaded once and passed in |
| KITTI-only `Dataset`, no timestamps | No EuRoC, no IMU | Timestamped sensor input, EuRoC first |
| Pinhole camera, rectified input | EuRoC images are raw and distorted | Camera models with distortion; rectification from calibration |
| Frontend calls the backend and viewer directly | Tight coupling | Keyframes go through a queue; the viewer observes |
| Backend waits on a condition variable without a predicate and holds the lock while optimizing | Missed wakeups; the frontend blocks | Work queue; optimize a copy without holding the lock |
| Non-atomic static id counters | Data race | Ids come from the `Map` |
| `Reset()` is empty | Tracking loss is permanent | Tracking state machine; relocalization in Phase 7 |
| Threaded only | Results not repeatable | Synchronous mode for tests and CI |
| One test, no trajectory evaluation | Regressions go unnoticed | See [Testing](#testing) |

### Conventions
- Poses: `T_a_b` maps points from frame `b` to frame `a`: `p_a = T_a_b * p_b`.
  Frames: world `w`, body/IMU `b`, cameras `c0` and `c1`, robot base `r`. The
  book's `Tcw` is our `T_c_w`. EuRoC's `T_BS` is `T_b_c0`.
- Time: `core::Timestamp`, integer nanoseconds as in EuRoC. Convert to
  seconds only at the edges.
- Units: SI (m, rad, s).
- Quaternions: Eigen's constructor takes `(w, x, y, z)`, but `.coeffs()`
  returns `(x, y, z, w)`. TUM files store `qx qy qz qw`; EuRoC files store
  `qw qx qy qz`. Every reader gets a test for this.
- Pixels: `(u, v)` is (column, row); `cv::Mat::at(row, col)`.
- Tangent vectors: se(3) is `[translation, rotation]`, as in Sophus and
  the book.

## Phases

| Phase | Book | Build | Done when |
|---|---|---|---|
| 0 Foundations | – | Build, CI, datasets, evaluation tools | A fresh clone builds and tests with one command, in Docker and CI |
| 1 Geometry and evaluation | ch2–4 | `core`, `geometry` (Lie groups), `eval`, trajectory files | Our ATE/RPE equals evo's on EuRoC ground truth |
| 2 Cameras and EuRoC | ch5 | `camera`, EuRoC reader, `viz` | Rectified EuRoC stereo plays in the viewer, epipolar error < 1 px |
| 3 Optimization | ch6, appendices A–B | `optimization`, Jacobian checker | Our GN/LM matches Ceres on test problems |
| 4 Features and two-view geometry | ch7 | `features`, two-view geometry, PnP, ICP, synthetic scenes | A simple frame-to-frame VO runs on MH_01 and is evaluated |
| 5 First stereo VO | ch8, ch13 frontend | `map`, `frontend`, `system`, `slambot_run` | All 11 EuRoC sequences run, and CI guards the ATE baseline |
| 6 Backend | ch9, ch10 (sliding window), ch13 backend | Sliding-window BA, threaded mode | ATE beats Phase 5 on every sequence; TSan clean |
| 7 Loop closure | ch10 (pose graph), ch11 | `loop_closure` | Loops found on MH_01–05 with no false positives; ATE improves |
| 8 Fusion and robustness | Papers (ch14 has pointers) | IMU, wheel odometry, failure handling | See below |
| 9 Own robot | ch5 (calibration) | Drivers, calibration, arm64 | Live run on the robot at the target frame rate, checked against a lidar reference |
| Optional: dense mapping | ch12 | Stereo depth to an octomap or TSDF | When the robot needs a map to navigate |

Chapters 2–6 are needed for everything else. The book's full system (ch13)
comes right after the frontend chapters, so each backend chapter improves a
system that already runs.

### Phase 0: Foundations
Done: build fixes, module layout, C++20, clang-tidy naming check, warnings,
ASan/TSan presets, CI (format, build, tests, clang-tidy, ASan),
`scripts/datasets.py`, evo.

To do:
- Ubuntu 24.04 dev image published to GHCR, and a gcc 11 CI job (D3).
- `CLAUDE.md`: build and test commands, conventions, who writes what.
- pre-commit hooks, a PR template, branch protection on `main`.

### Phase 1: Geometry and evaluation (ch2–4)
- Read: ch2–4, with Solà et al., *A micro Lie theory*.
- Experiments: rotation representations (ch3); Sophus exp/log and
  perturbations (ch4).
- Build:
  - Lie group functions: hat/vee, SO(3) and SE(3) exp/log, Jacobians, adjoint.
    Tested against Sophus; the library keeps using Sophus. *(us)*
  - Trajectory files: TUM format and EuRoC ground truth. *(Claude)*
  - Evaluation: timestamp matching, Umeyama alignment, ATE, RPE. *(us)*
- Tests: exp/log round trips, including angles near 0 and π; analytic vs
  numerical Jacobians; ATE is 0 for identical trajectories and unchanged by a
  rigid transform; quaternion order in every reader; results match evo.
- Done when: `slambot_eval` gives the same ATE/RPE as evo (within 1e-6) on
  EuRoC ground truth vs a perturbed copy.

### Phase 2: Cameras and EuRoC (ch5)
- Read: ch5, and OpenCV's calibration and `stereoRectify` docs.
- Experiments: undistortion by hand vs `cv::undistort`; stereo disparity to
  a point cloud.
- Build:
  - Pinhole camera with radial-tangential distortion and its projection
    Jacobian. *(us)*
  - Stereo rig from EuRoC's `sensor.yaml`, rectification, depth from
    disparity. *(pair)*
  - EuRoC reader: images, IMU, ground truth, calibration. *(Claude)*
  - Rerun viewer behind `viz::Visualizer`. *(Claude)*
- Tests: project/unproject and distort/undistort round trips; projection
  Jacobian; rectified matches on the same row within 1 px; reader tests on a
  small fixture.
- Done when: an EuRoC sequence plays in the viewer with rectified stereo,
  IMU plots and the ground-truth pose.

### Phase 3: Optimization (ch6, appendices A–B)
- Read: ch6, appendix A (Gaussians), appendix B (matrix derivatives), the
  Ceres tutorial.
- Experiment: the book's curve fit with gradient descent, Newton, GN and
  LM, in our code and in Ceres.
- Build:
  - Small dense Gauss-Newton and Levenberg-Marquardt. *(us)*
  - Jacobian checker using central differences, also on manifolds. *(Claude)*
  - Ceres helpers with Sophus's SE(3) manifold. *(pair)*
- Tests: noise-free problems are solved exactly; the LM cost never
  increases; GN reports failure on a singular system where LM continues; our
  GN/LM matches Ceres.
- Done when: the Jacobian checker is in place for every later residual,
  and D1 is decided.

### Phase 4: Features and two-view geometry (ch7)
- Read: ch7.
- Experiments: ORB with OpenCV (started in `experiments/ch07_orb`) and by
  hand (with `std::popcount`, so it builds on ARM); pose from 2D-2D, 3D-2D and
  3D-3D matches.
- Build:
  - Synthetic scene generator: landmarks, trajectory, stereo rig, noise,
    outliers, with ground truth. *(Claude)*
  - Feature detection and matching wrappers. *(pair)*
  - Eight-point algorithm and essential-matrix decomposition, triangulation,
    PnP refined with Gauss-Newton, ICP with SVD. *(us)*
- Tests (on synthetic scenes): exact without noise; PnP with RANSAC
  handles 30% outliers; degenerate cases are detected; Jacobians vs numerical.
- Done when: a simple frame-to-frame stereo VO (triangulate, then PnP in
  the next frame) produces an evaluated trajectory on MH_01. It will drift.

### Phase 5: First stereo VO (ch8, ch13 frontend)
- Read: ch8 (optical flow, direct method), then ch13.
- Experiments: our pyramidal Lucas-Kanade vs OpenCV's; the sparse direct
  method.
- Build:
  - `map` data model, without ch13's data races. *(pair)*
  - Frontend: stereo initialization, tracking, pose refinement, keyframe
    choice. *(us)*
  - Tracking state machine: initializing, good, bad, lost. *(pair)*
  - `system` in synchronous mode and `apps/slambot_run`, writing a TUM
    trajectory and a Rerun recording. *(Claude)*
- Tests: LK on synthetic sub-pixel shifts; state transitions; 50 frames of
  MH_01 tracked without loss; ATE/RPE per sequence vs stored baselines.
- Done when: all 11 EuRoC sequences run (losing track on the hardest is
  allowed, but recorded), and CI guards the baseline numbers.

### Phase 6: Backend (ch9, ch10 sliding window, ch13 backend)
- Read: ch9 and the sliding-window part of ch10. The book has no code or
  equations for the marginalization prior; that comes in Phase 8.
- Experiments: the book's BAL problem in Ceres with different Schur
  solvers; a small dense bundle adjustment with an explicit Schur complement.
  *(us)*
- Build:
  - Stereo reprojection residual. *(us)*
  - Sliding-window bundle adjustment in Ceres. *(pair)*
  - Threaded mode with a work queue. *(pair)*
- Tests: synthetic BA converges to the noise level; the Schur solve equals
  the dense solve; a Huber loss beats plain least squares with 10% outliers;
  threaded results match synchronous ones; TSan is clean.
- Done when: ATE beats Phase 5 on every sequence.

### Phase 7: Loop closure (ch10 pose graph, ch11)
- Read: the pose-graph part of ch10, and ch11.
- Experiments: the book's `sphere.g2o` pose graph in Ceres; train a
  vocabulary.
- Build:
  - Vocabulary tree with TF-IDF scoring (D6). *(us)*
  - Loop detection and geometric verification. *(pair)*
  - Pose-graph residual. *(us)*
  - Relocalization after tracking loss, using the same place recognition.
    *(pair)*
- Tests: scoring on small hand-made examples; precision 1.0 on EuRoC loops
  taken from the ground truth; drift on a synthetic loop shrinks after closing it.
- Done when: loops are found on MH_01–05 with no false positives, and ATE
  improves.

### Phase 8: Fusion and robustness
The book only points to papers here. Three steps, each measured on its own.

- 8a IMU.
  - Read Forster et al. (preintegration), Solà (quaternion kinematics),
    VINS-Mono and OKVIS, and ORB-SLAM3 for initialization.
  - Build IMU preintegration with covariance and bias Jacobians,
    visual-inertial initialization, the IMU residual and the marginalization
    prior *(us)*, and the visual-inertial sliding window *(pair)*. Tests
    cross-check preintegration against GTSAM.
  - Done when stereo-inertial beats stereo-only on V1_03 and V2_03 (fast motion).
- 8b Wheel odometry.
  - Read Wu et al., *VINS on Wheels*.
  - Build the OpenLORIS-Scene reader *(Claude)*, the wheel-odometry residual
    *(us)*, calibration of the camera-to-base transform and wheel parameters
    *(pair)*, and a fisheye camera model (OpenLORIS and TUM-VI use fisheye
    lenses) *(us)*.
  - Done when wheel odometry lowers ATE and tracking loss on OpenLORIS-Scene.
- 8c Failure handling.
  - Build a health monitor (good, degraded, lost), dead reckoning on IMU and
    wheels while vision is lost, and relocalization in a saved map. *(pair)*
  - Done when the robustness tests show no unrecovered tracking loss on EuRoC
    and OpenLORIS-Scene.

### Phase 9: Own robot
- Choose the hardware (D7). Calibrate the cameras, camera to IMU (Kalibr),
  the wheels, and camera to base.
- Drivers, or record in ASL format and replay. *(Claude)*
- Reference trajectories from an existing 2D lidar SLAM (slam_toolbox or
  Cartographer).
- arm64 build in CI; profiling with Tracy.
- Done when: the robot runs live at the target frame rate, and recorded
  runs, including the robustness tests, are evaluated against the lidar
  reference.

## Datasets

| Dataset | Contents | Use |
|---|---|---|
| EuRoC MAV | Drone. Stereo 752×480 global shutter at 20 Hz (raw, distorted), IMU at 200 Hz, ground truth. 11 sequences, easy to difficult. | Main dataset, Phases 1–8 |
| OpenLORIS-Scene | Wheeled robot. RealSense T265 (fisheye stereo + IMU) and D435i, wheel odometry. | Phase 8b–8c |
| TUM-VI | Handheld. Fisheye stereo + IMU, hardware-synced. | Optional, after Phase 6 |
| KITTI odometry | Car. Rectified stereo. | Optional, to compare with the book's ch13 |
| Own recordings | Our robot, ASL format, lidar reference. | Phase 9 |

- `scripts/datasets.py` downloads EuRoC sequences to `data/` (or
  `$SLAMBOT_DATA`). EuRoC comes as one zip per environment (12.7 GB for the
  machine hall), so the script downloads just the requested sequence and checks
  its size and CRC-32.
- Never commit datasets. EuRoC's license is "In Copyright, Non-Commercial Use
  Permitted"; KITTI's is CC BY-NC-SA 3.0. Prefer synthetic test data, and keep
  committed test data under 5 MB.
- evo evaluates trajectories, and cross-checks our `eval` module.

## Testing

- Unit tests (Catch2) next to the code, on every PR, with fixed random seeds.
- Numerical checks: round trips, invariants, and Jacobians against finite
  differences.
- Synthetic scenes with known ground truth, noise and outliers.
- Integration tests on small real snippets.
- Regression: the full pipeline on EuRoC (later OpenLORIS-Scene). ATE, RPE
  and tracking-loss rate are compared with stored baselines, nightly and on
  request. A PR that improves the numbers updates the baselines.
- Robustness (from Phase 7): sequences with dark or covered frames, dropped
  frames and blur, plus the fast EuRoC sequences. Measures tracking loss,
  recovery time and relocalization.
- Sanitizers: ASan + UBSan now; TSan once there are threads.

Synchronous mode, seeded RANSAC and fixed thread counts make runs repeatable,
so a changed number means a real change.

## CI and tools

CI today (`.github/workflows/ci.yml`, on every PR and push to `main`): a
clang-format check, then in the dev image a build with warnings as errors, unit
tests, clang-tidy, and the tests again under ASan + UBSan.

Planned:
- Ubuntu 24.04 dev image published to GHCR; a gcc 11 build job.
- pre-commit hooks, PR template, branch protection on `main`.
- Nightly regression job: runs EuRoC sequences, shows the ATE table in the job
  summary, and keeps trajectories and Rerun recordings as artifacts.
- arm64 build (Phase 9).

Tools:
- Docker + devcontainer: the same environment for both of us and CI.
- uv: Python tools (cmake, conan, ninja, clang-format, clang-tidy, evo,
  later the Rerun viewer).
- Conan 2 with a lockfile: C++ packages.
- CMake presets: `conan-release` (from Conan), `asan`, `tsan`.

## Working with Claude Code

Who writes what:
- Us: the core algorithms. Lie group functions, camera models, GN/LM,
  two-view geometry, triangulation, PnP, ICP, optical flow, residuals, Schur
  complement and marginalization, keyframe choice, vocabulary tree, IMU
  preintegration.
- Claude: build, CI, Docker, dataset readers, viewer code, scripts, test
  scaffolding, the synthetic scene generator, reviews.
- Together: module interfaces, connecting frontend and backend, threading.

For each *(us)* task:
1. Read the book section.
2. Have Claude explain it and quiz us. Write notes in `docs/learning/chNN.md`.
3. Claude writes the header, the tests and a `TODO(human)` stub.
4. We implement until the tests pass, without asking Claude for the answer.
5. Review with `/code-review`, and compare with the library version.
6. Open a PR for the other person to review, with a short "what I learned".

`CLAUDE.md` holds the build commands, the conventions, and the rule that Claude
doesn't write *(us)* code unless asked. Use the "Learning" output style for
learning sessions.

## GitHub

- Milestones are the phases; issues are the tasks in each phase. Labels:
  `phase-N`, `learning`, `infra`, `decision`, `bug`, `experiment`.
- Issue #5 (project plan) points here. #3 (dataset) can close: EuRoC. #2 (CI)
  can close: CI is in place.
- Old branches: delete `2-Add-CI` (replaced); archive
  `experimental/pangolin-conan-recipe` (Pangolin removed); move the `Frame` and
  `Dataset` ideas from `frontend/dataset-frames` into Phases 2 and 5.

## References

- Solà, Deray, Atchuthan, *A micro Lie theory for state estimation in robotics*, 2018.
- Solà, *Quaternion kinematics for the error-state Kalman filter*, 2017.
- Forster, Carlone, Dellaert, Scaramuzza, *On-Manifold Preintegration for Real-Time Visual-Inertial Odometry*, T-RO 2017.
- Leutenegger et al., *OKVIS*, IJRR 2015.
- Qin, Li, Shen, *VINS-Mono*, T-RO 2018.
- Wu, Guo, Georgiou, Roumeliotis, *VINS on Wheels*, ICRA 2017.
- Mourikis, Roumeliotis, *MSCKF*, ICRA 2007; Geneva et al., *OpenVINS*, ICRA 2020.
- Campos et al., *ORB-SLAM3*, T-RO 2021.
- Usenko et al., *Basalt*, RA-L 2020.
- Zhang, Scaramuzza, *A Tutorial on Quantitative Trajectory Evaluation for Visual(-Inertial) Odometry*, IROS 2018.
- Barfoot, *State Estimation for Robotics*, 2nd ed., 2024.
- Cadena et al., *Past, Present, and Future of SLAM*, T-RO 2016.

## Porting book code

The book's code targets OpenCV 3, C++11, CMake 2.8 and an older g2o. Common
fixes when moving an example into `experiments/`:

| Book | Now |
|---|---|
| `cmake_minimum_required(VERSION 2.8)`, `include_directories(...)` | Our CMake 3.23 setup with `target_link_libraries(x PRIVATE Eigen3::Eigen Sophus::Sophus)` |
| `namespace myslam`, `SetPose()`, `CreateFrame()` | `namespace slambot::<module>`, `set_pose()`, `create()` (D5) |
| `CV_LOAD_IMAGE_COLOR`, `imread(f, 0)` | `cv::IMREAD_COLOR`, `cv::IMREAD_GRAYSCALE` |
| `CV_GRAY2BGR`, `CV_FILLED`, `CV_FM_8POINT` | `cv::COLOR_GRAY2BGR`, `cv::FILLED`, `cv::FM_8POINT` |
| g2o examples | Port to Ceres (D1) |
| `virtual bool read(...) {}` without a return | Undefined behavior; return a value |
| `while (!fin.eof())` | `while (fin >> a >> b ...)`, otherwise you get one extra, garbage pose at the end |
| `_mm_popcnt_u32`, `-msse4` | `std::popcount`, so it builds on ARM |
| `boost::format` | `fmt::format` |
| Hard-coded dataset paths | A command-line argument or config, with `$SLAMBOT_DATA` |
| `assert(vo->Init())` | The call disappears in release builds; check the result explicitly |
| `EIGEN_MAKE_ALIGNED_OPERATOR_NEW` | Not needed since C++17 |
