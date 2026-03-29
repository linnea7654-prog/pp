#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <random>
#include <omp.h>
#include <iomanip>
#include <windows.h>

using namespace std;
using namespace chrono;

typedef vector<vector<int>> Matrix;

Matrix generateMatrix(int n, int min_val, int max_val) {
    Matrix mat(n, vector<int>(n));
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dist(min_val, max_val);

    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            mat[i][j] = dist(gen);
    return mat;
}

Matrix multiplyMatrices(const Matrix& A, const Matrix& B, int threads) {
    int n = A.size();
    Matrix C(n, vector<int>(n, 0));

    omp_set_num_threads(threads);

#pragma omp parallel for collapse(2)
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            int sum = 0;
            for (int k = 0; k < n; ++k) {
                sum += A[i][k] * B[k][j];
            }
            C[i][j] = sum;
        }
    }
    return C;
}

int main() {
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
    vector<int> sizes = { 200, 400, 800, 1200, 1600, 2000 };  
    vector<int> threads_list = { 1, 2, 4, 8, 12, 16 };    
    int min_val = 0, max_val = 100;
    int num_runs = 3;

    ofstream result_file("results.csv");
    result_file << "size,threads,time_ms,flops,speedup\n";

    for (int n : sizes) {
        cout << "\n[" << n << "x" << n << "]" << endl;

        Matrix A = generateMatrix(n, min_val, max_val);
        Matrix B = generateMatrix(n, min_val, max_val);


        double base_time = 0;

        for (int threads : threads_list) {
            vector<double> times;

            for (int run = 0; run < num_runs; run++) {
                auto start = high_resolution_clock::now();
                Matrix C = multiplyMatrices(A, B, threads);
                auto end = high_resolution_clock::now();

                double time_ms = duration<double, milli>(end - start).count();
                times.push_back(time_ms);
            }

            double avg_time = 0;
            for (double t : times) avg_time += t;
            avg_time /= num_runs;

            double flops = 2.0 * n * n * n;

            if (threads == 1) {
                base_time = avg_time;
            }
            double speedup = (threads == 1) ? 1.0 : base_time / avg_time;

            cout << "  potok: " << setw(2) << threads
                << " | time: " << setw(8) << fixed << setprecision(2) << avg_time << " mc"
                << " | uscor: " << fixed << setprecision(2) << speedup << "x"
                << endl;

            result_file << n << "," << threads << "," << avg_time << "," << flops << "," << speedup << "\n";
        }
    }

    result_file.close();
    return 0;
}
