# slambot_add_module(<name>
#     [SOURCES <file>...]   # .cpp files; without them the module is header-only
#     [DEPS <target>...]    # libraries the module's headers need
#     [TESTS <file>...])    # Catch2 test files, built when BUILD_TESTING is on
#
# Creates the library slambot_<name>, with the alias slambot::<name>, and the
# test executable slambot_<name>_test. Includes are written from the repo root,
# e.g. #include "slambot/core/timestamp.hpp".
function(slambot_add_module name)
    cmake_parse_arguments(PARSE_ARGV 1 arg "" "" "SOURCES;DEPS;TESTS")
    set(target slambot_${name})

    if(arg_SOURCES)
        add_library(${target} ${arg_SOURCES})
        set(scope PUBLIC)
        slambot_set_warnings(${target})
    else()
        add_library(${target} INTERFACE)
        set(scope INTERFACE)
    endif()
    add_library(slambot::${name} ALIAS ${target})
    target_include_directories(${target} ${scope} ${PROJECT_SOURCE_DIR})
    target_compile_features(${target} ${scope} cxx_std_20)
    target_link_libraries(${target} ${scope} ${arg_DEPS})

    if(BUILD_TESTING AND arg_TESTS)
        add_executable(${target}_test ${arg_TESTS})
        target_link_libraries(${target}_test PRIVATE ${target} Catch2::Catch2WithMain)
        slambot_set_warnings(${target}_test)
        catch_discover_tests(${target}_test)
    endif()
endfunction()
