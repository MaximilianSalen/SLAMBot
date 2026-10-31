#include <cassert>
#include <iostream>
#include <string>
#include <vector>

#include <opencv2/features2d.hpp>
#include <opencv2/opencv.hpp>

void featureExtraction(std::string imgPath1, std::string imgPath2) {

    // read images
    cv::Mat img1 = cv::imread(imgPath1, cv::IMREAD_COLOR);
    cv::Mat img2 = cv::imread(imgPath2, cv::IMREAD_COLOR);
    assert(img1.data != nullptr && img2.data != nullptr);

    // initialization
    std::vector<cv::KeyPoint> keypoints1, keypoints2;
    cv::Mat descriptors1, descriptors2;

    // TODO(human): detect ORB keypoints, compute descriptors and match them
    // (book ch7, orb_cv.cpp)
}

int main(int argc, char **argv) {
    if (argc != 3) {
        std::cerr << "usage: " << argv[0] << " img1 img2" << std::endl;
        return 1;
    }
    featureExtraction(argv[1], argv[2]);
    return 0;
}
