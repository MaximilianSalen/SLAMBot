#include <opencv2/opencv.hpp>
#include <memory>
#include "Eigen/Dense"
#pragma once


namespace SLAMBot{


struct Frame {
    public:
       EIGEN_MAKE_ALIGNED_OPERATOR_NEW;
       typedef std::shared_ptr<Frame> Ptr;

       unsigned long m_id = 0; //ID of this frame
       unsigned long m_keyframeId = 0; //ID of keyframe
       bool isKeyframe = false;

       cv::Mat image;


};    
} // namespace SLAMBot