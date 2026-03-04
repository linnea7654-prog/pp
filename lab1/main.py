import subprocess
import numpy as np
import time
import os
import matplotlib.pyplot as plt


def run_experiment(n, min_val, max_val):
    result = subprocess.run(
        ["./osn_pr_v_1.exe", str(n), str(min_val), str(max_val), "A.txt", "B.txt"],
        capture_output=True, text=True
    )
    cpp_time = 0
    for line in result.stdout.split('\n'):
        if "Время выполнения:" in line:
            cpp_time = float(line.split(':')[1].strip().replace('мс', ''))

    A = np.loadtxt('A.txt')
    B = np.loadtxt('B.txt')
    C_cpp = np.loadtxt('result.txt')

    start = time.time()
    C_numpy = A @ B
    py_time = (time.time() - start) * 1000

    correct = np.allclose(C_cpp, C_numpy, rtol=1e-5)

    return cpp_time, py_time, correct


def main():
    n = int(input("Размер матрицы: "))
    min_val = float(input("Min: "))
    max_val = float(input("Max: "))

    print(f"\nЗапуск 10 экспериментов...")

    cpp_times = []
    py_times = []
    correct_count = 0

    for i in range(10):
        cpp_t, py_t, ok = run_experiment(n, min_val, max_val)
        cpp_times.append(cpp_t)
        py_times.append(py_t)
        if ok:
            correct_count += 1
        print(f"{i + 1}: C++={cpp_t:.1f}мс Python={py_t:.1f}мс")

    # График
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, 11), cpp_times, 'bo-', label='C++', linewidth=2)
    plt.plot(range(1, 11), py_times, 'rs-', label='Python', linewidth=2)
    plt.xlabel('Эксперимент')
    plt.ylabel('Время (мс)')
    plt.title(f'Сравнение производительности (матрица {n}x{n})')
    plt.legend()
    plt.grid(True)
    plt.xticks(range(1, 11))

    # Текст с результатами
    text = f"""
    Среднее C++: {np.mean(cpp_times):.1f} мс
    Среднее Python: {np.mean(py_times):.1f} мс
    """
    plt.text(0.5, -0.2, text, transform=plt.gca().transAxes,
             fontsize=10, verticalalignment='top')

    plt.tight_layout()
    plt.savefig('results.png')
    plt.show()
    print(text)

if __name__ == "__main__":
    main()