#include <catch2/catch_all.hpp>

#include "SLAMBot/ExampleDivFunction.h"

namespace slam {

TEST_CASE("slam::example_div_function") {
    double a = 4.0;
    double b = 2.0;
    auto c = example_div_function(a, b);
    REQUIRE(c == 2.0);
}

} // namespace slam
