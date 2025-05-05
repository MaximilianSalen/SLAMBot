#include <opencv2/opencv.hpp>
#include <opencv2/features2d.hpp>


void featureExtraction(std::string imgPath1, std::string imgPath2){

    // read images
    cv::Mat img1 = cv::imread(imgPath1);
    cv::Mat img2 = cv::imread(imgPath2);
    assert(img1.data != nullptr && img2.data != nullptr);


    // initialization
    std::vector<cv::KeyPoint> keypoints1, keypoints2;
    cv::Mat descriptors1, descriptors2;


}