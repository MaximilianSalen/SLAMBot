#include "Dataset.h"
#include <iostream>

namespace SLAMBot {
Dataset::Dataset(const std::string &datasetPath) 
: m_datasetPath(datasetPath) {}

bool Dataset::init(){
};
} 