#include "slambot/core/timestamp.hpp"

#include <cmath>

namespace slambot::core {

Timestamp Timestamp::from_seconds(double seconds) {
    return Timestamp(std::llround(seconds * 1e9));
}

} // namespace slambot::core
