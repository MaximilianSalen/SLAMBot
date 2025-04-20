set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

#############################
# SLAMBot library
#############################
# Find packages
find_package(Eigen3 REQUIRED)
find_package(Sophus REQUIRED)
find_package(OpenCV REQUIRED)

add_library(SLAMBot
    ExampleDivFunction.cpp)

# Add root directory.
target_include_directories(SLAMBot PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/..)

# Link Eigen and Sophus
target_link_libraries(SLAMBot PRIVATE Sophus::Sophus
    Eigen3::Eigen
    ${OpenCV_LIBS})

#############################
# SLAMBot executable 
#############################
add_executable(SLAMBotApp
    main.cpp)
add_executable(test_sophus TestSophus.cpp)
add_executable(test_opencv TestOpenCV.cpp)
target_link_libraries(SLAMBotApp PRIVATE
    SLAMBot
    Eigen3::Eigen)

target_link_libraries(test_sophus PRIVATE
    SLAMBot
    Eigen3::Eigen
    Sophus::Sophus)

target_link_libraries(test_opencv PRIVATE
    SLAMBot
    ${OpenCV_LIBS})

#############################
# SLAMBot tests 
#############################
# Add the test executable.
add_executable(SLAMBot_test ExampleDivFunction_test.cpp)

# Link to Catch2 from Conan.
find_package(Catch2 REQUIRED)

# Add root directory to tests.
target_include_directories(SLAMBot_test PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/..)

# Link test.
target_link_libraries(SLAMBot_test PRIVATE
    SLAMBot
    Catch2::Catch2WithMain)

# Register with CTest.
include(CTest)
include(Catch)
catch_discover_tests(SLAMBot_test)
