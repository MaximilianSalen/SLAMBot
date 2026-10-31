#include "slambot/core/timestamp.hpp"

#include <catch2/catch_test_macros.hpp>

#include <cstdint>

namespace slambot::core {
namespace {

// A Unix-time stamp in nanoseconds, the size EuRoC uses (2014).
constexpr std::int64_t kEurocSizedNs = 1'403'636'579'763'555'584;

TEST_CASE("Timestamp converts between nanoseconds and seconds") {
    const auto t = Timestamp::from_nanoseconds(1'500'000'000);
    CHECK(t.nanoseconds() == 1'500'000'000);
    CHECK(t.seconds() == 1.5);
    CHECK(Timestamp::from_seconds(1.5) == t);
}

TEST_CASE("Timestamp::from_seconds rounds to the nearest nanosecond") {
    CHECK(Timestamp::from_seconds(0.6e-9).nanoseconds() == 1);
    CHECK(Timestamp::from_seconds(0.4e-9).nanoseconds() == 0);
    CHECK(Timestamp::from_seconds(-0.6e-9).nanoseconds() == -1);
}

TEST_CASE("Timestamps compare by time") {
    const auto earlier = Timestamp::from_nanoseconds(1);
    const auto later = Timestamp::from_nanoseconds(2);
    CHECK(earlier < later);
    CHECK(later > earlier);
    CHECK(earlier != later);
    CHECK(Timestamp() == Timestamp::from_nanoseconds(0));
}

// Why we compare in nanoseconds: as seconds, these two times are equal.
TEST_CASE("Seconds can't tell apart Unix-time stamps 100 ns apart") {
    const auto t = Timestamp::from_nanoseconds(kEurocSizedNs);
    const auto later = Timestamp::from_nanoseconds(kEurocSizedNs + 100);
    CHECK(t < later);
    CHECK(t.seconds() == later.seconds());
}

} // namespace
} // namespace slambot::core
