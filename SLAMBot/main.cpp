#include <iostream>

#include "SLAMBot/ExampleDivFunction.h"

int main() {
    double div_res = slam::example_div_function(4.0, 2.0);
    std::cout << div_res << std::endl;

    return 0;
}
