#############################
# SLAMBot library
#############################
add_library(SLAMBot
    ExampleDivFunction.cpp
)

# Add root directory.
target_include_directories(SLAMBot
    PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/..
)

#############################
# SLAMBot executable
#############################
add_executable(SLAMBotApp
    main.cpp)
target_link_libraries(SLAMBotApp PRIVATE
    SLAMBot
)

#############################
# SLAMBot tests
#############################
if(BUILD_TESTING)
    # Add the test executable.
    add_executable(SLAMBot_test ExampleDivFunction_test.cpp)

    # Link to Catch2 from Conan.
    find_package(Catch2 REQUIRED)

    # Link test.
    target_link_libraries(SLAMBot_test PRIVATE
        SLAMBot
        Catch2::Catch2WithMain)

    # Register with CTest (enabled in the top-level CMakeLists.txt).
    include(Catch)
    catch_discover_tests(SLAMBot_test)
endif()
