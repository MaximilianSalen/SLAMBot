#include "Eigen/Dense"
#include <memory>

#pragma once

namespace SLAMBot {
class Dataset {
public:
  EIGEN_MAKE_ALIGNED_OPERATOR_NEW;
  typedef std::shared_ptr<Dataset> Ptr;
  Dataset(const std::string &datasetPath);

  // Initialization, returns if sucessful
  bool init();

private:
  std::string m_datasetPath;
  int m_currentImageIndex = 0;
};
} 