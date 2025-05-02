#include <opencv2/opencv.hpp>


void test_opencv() {
    int width = 400;
    int height = 400;
    cv::Mat image(height, width, CV_8UC3, cv::Scalar(0, 0, 255)); // Red image (BGR format)

    cv::imshow("Display Window", image);

    cv::waitKey(0);

}

int main() {
    test_opencv();
    return 0;
}
