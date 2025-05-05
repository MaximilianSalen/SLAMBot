#include <memory>
#include <opencv2/opencv.hpp>
#include <sophus/geometry.hpp>
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
       Sophus::SE3d m_pose;

       

       cv::Mat image;

    public:
        Frame() {}

        Frame(long id, const Sophus::SE3d &pose, const cv::Mat image);

        Sophus::SE3d pose() {
            return m_pose;
        }

        void setPose(const Sophus::SE3d &pose) {
            m_pose = pose;
        }

        void setKeyFrame();

        static std::shared_ptr<Frame> CreateFrame();


};    
} // namespace SLAMBot