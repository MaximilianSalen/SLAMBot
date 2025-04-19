#include "SLAMBot/ExampleDivFunction.h"

#include <stdexcept>

namespace slam {

auto example_div_function(double ax, double bx) -> double
{
	if (bx == 0) {
		throw std::runtime_error("Division with zero.");
	}
	return ax / bx;
}

} // namespace slam
