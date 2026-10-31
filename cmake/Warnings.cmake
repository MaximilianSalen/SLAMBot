# Compiler warnings for our own targets. Headers of dependencies come from
# imported targets, which CMake treats as system headers, so their warnings
# are not shown.
option(SLAMBOT_WARNINGS_AS_ERRORS "Treat compiler warnings as errors (on in CI)" OFF)

function(slambot_set_warnings target)
    target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic -Wshadow)
    if(SLAMBOT_WARNINGS_AS_ERRORS)
        target_compile_options(${target} PRIVATE -Werror)
    endif()
endfunction()
