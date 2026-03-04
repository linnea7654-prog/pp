#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>
#include <random>
#include <iomanip>
#include <sstream>

using Matrix = std::vector<std::vector<double>>;

Matrix generateMatrix(int n, double min_val, double max_val) {
    Matrix mat(n, std::vector<double>(n));
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dist(min_val, max_val);

    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            mat[i][j] = dist(gen);
    return mat;
}

void writeMatrix(const std::string& filename, const Matrix& mat) {
    std::ofstream file(filename);
    for (const auto& row : mat) {
        for (double val : row)
            file << std::fixed << std::setprecision(6) << val << " ";
        file << std::endl;
    }
}

Matrix multiplyMatrices(const Matrix& A, const Matrix& B) {
    int n = A.size();
    Matrix C(n, std::vector<double>(n, 0.0));

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            double sum = 0.0;
            for (int k = 0; k < n; ++k) {
                sum += A[i][k] * B[k][j];
            }
            C[i][j] = sum;
        }
    }
    return C;
}

int main(int argc, char* argv[]) {
    if (argc != 6) {
        std::cerr << "Usage: " << argv[0] << " n min_val max_val A.txt B.txt" << std::endl;
        return 1;
    }

    int n = std::atoi(argv[1]);
    double min_val = std::atof(argv[2]);
    double max_val = std::atof(argv[3]);
    std::string fileA = argv[4];
    std::string fileB = argv[5];
    std::string fileC = "result.txt";

    Matrix A = generateMatrix(n, min_val, max_val);
    Matrix B = generateMatrix(n, min_val, max_val);

    writeMatrix(fileA, A);
    writeMatrix(fileB, B);

    auto start = std::chrono::high_resolution_clock::now();
    Matrix C = multiplyMatrices(A, B);
    auto end = std::chrono::high_resolution_clock::now();

    writeMatrix(fileC, C);

    double time_ms = std::chrono::duration<double, std::milli>(end - start).count();
    double flops = 2.0 * n * n * n;

    std::cout << "Время выполнения: " << time_ms << " мс" << std::endl;
    std::cout << "Объем задачи: " << flops << " операций" << std::endl;

    return 0;
}