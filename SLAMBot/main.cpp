#include "Eigen/Dense"

#include <iostream>

void createAndPrintMatrix() {
  // Create a 3x3 matrix of doubles
  Eigen::MatrixXd mat(3, 3);

  // Fill it with values
  mat << 1, 2, 3, 4, 5, 6, 7, 8, 9;

  // Print the matrix
  std::cout << "Matrix:\n" << mat << std::endl;
}

int main() {
  createAndPrintMatrix();
  return 0;
}
