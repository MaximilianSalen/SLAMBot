#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/features2d.hpp>


void featureExtraction(std::string imgPath1, std::string imgPath2){

    // read images
    cv::Mat img1 = cv::imread(imgPath1, CV_LOAD_IMAGE_COLOR);
    cv::Mat img2 = cv::imread(imgPath2, CV_LOAD_IMAGE_COLOR);
    assert(img1.data != nullptr && img2.data != nullptr);


    // initialization
    std::vector<cv::KeyPoint> keypoints1, keypoints2;
    cv::Mat descriptors1, descriptors2;


}