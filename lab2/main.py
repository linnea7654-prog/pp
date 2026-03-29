import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Твои данные
data = {
    'size': [200, 200, 200, 200, 200, 200,
             400, 400, 400, 400, 400, 400,
             800, 800, 800, 800, 800, 800,
             1200, 1200, 1200, 1200, 1200, 1200,
             1600, 1600, 1600, 1600, 1600, 1600,
             2000, 2000, 2000, 2000, 2000, 2000],
    'threads': [1, 2, 4, 8, 12, 16,
                1, 2, 4, 8, 12, 16,
                1, 2, 4, 8, 12, 16,
                1, 2, 4, 8, 12, 16,
                1, 2, 4, 8, 12, 16,
                1, 2, 4, 8, 12, 16],
    'time_ms': [112.80, 111.50, 107.84, 106.32, 104.62, 104.28,
                861.95, 868.05, 853.97, 851.45, 857.01, 848.73,
                6975.15, 6999.36, 7086.29, 7024.82, 7451.56, 7851.61,
                25016.18, 24808.30, 24661.05, 24764.44, 41982.21, 32951.19,
                81470.39, 73031.00, 60636.22, 60494.03, 61025.45, 60737.45,
                184357.59, 185335.32, 184700.82, 183347.98, 183199.13, 184120.12],
    'speedup': [1.00, 1.01, 1.05, 1.06, 1.08, 1.08,
                1.00, 0.99, 1.01, 1.01, 1.01, 1.02,
                1.00, 1.00, 0.98, 0.99, 0.94, 0.89,
                1.00, 1.01, 1.01, 1.01, 0.60, 0.76,
                1.00, 1.12, 1.34, 1.35, 1.34, 1.34,
                1.00, 0.99, 1.00, 1.01, 1.01, 1.00]
}

df = pd.DataFrame(data)
sizes = df['size'].unique()
threads = df['threads'].unique()

print("=" * 70)
print("АНАЛИЗ РЕЗУЛЬТАТОВ ЭКСПЕРИМЕНТОВ")
print("=" * 70)

# 1. График: Время от количества потоков
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for idx, size in enumerate(sizes):
    ax = axes[idx]
    data_size = df[df['size'] == size]

    ax.plot(data_size['threads'], data_size['time_ms'], 'bo-', linewidth=2, markersize=8)
    ax.set_xlabel('Количество потоков')
    ax.set_ylabel('Время (мс)')
    ax.set_title(f'Матрица {size}x{size}')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(threads)

plt.suptitle('Зависимость времени умножения от числа потоков', fontsize=16)
plt.tight_layout()
plt.savefig('time_vs_threads.png', dpi=150)
plt.show()

# 2. График: Ускорение от количества потоков
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for idx, size in enumerate(sizes):
    ax = axes[idx]
    data_size = df[df['size'] == size]

    ax.plot(data_size['threads'], data_size['speedup'], 'ro-', linewidth=1, markersize=4, label='Реальное')
    ax.plot([1, max(threads)], [1, 2], 'b--', linewidth=2, alpha=0.5, label='Идеальное')
    ax.set_xlabel('Количество потоков')
    ax.set_ylabel('Ускорение')
    ax.set_title(f'Матрица {size}x{size}')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xticks(threads)

plt.suptitle('Ускорение при увеличении числа потоков', fontsize=16)
plt.tight_layout()
plt.savefig('speedup_vs_threads.png', dpi=150)
plt.show()

# 3. График: Время от размера
plt.figure(figsize=(12, 8))

colors = plt.cm.viridis(np.linspace(0, 1, len(threads)))

for idx, t in enumerate(threads):
    data_threads = df[df['threads'] == t]
    plt.plot(data_threads['size'], data_threads['time_ms'], 'o-',
             color=colors[idx], label=f'{t} потоков', linewidth=2, markersize=6)

plt.xlabel('Размер матрицы (n)', fontsize=12)
plt.ylabel('Время (мс)', fontsize=12)
plt.title('Зависимость времени от размера матрицы', fontsize=14)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.yscale('log')  # Логарифмическая шкала, так как время растет быстро
plt.tight_layout()
plt.savefig('time_vs_size.png', dpi=150)
plt.show()

# 5. График эффективности (ускорение / потоки)
plt.figure(figsize=(12, 8))

for size in sizes:
    data_size = df[df['size'] == size]
    efficiency = data_size['speedup'] / data_size['threads']
    plt.plot(data_size['threads'], efficiency * 100, 'o-',
             label=f'{size}x{size}', linewidth=2, markersize=8)

plt.xlabel('Количество потоков', fontsize=12)
plt.ylabel('Эффективность (%)', fontsize=12)
plt.title('Эффективность использования потоков', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.axhline(y=100, color='k', linestyle='--', alpha=0.5, label='Идеальная эффективность')
plt.tight_layout()
plt.savefig('efficiency.png', dpi=150)
plt.show()

# 6. Сводная таблица
print("\n" + "=" * 70)
print("СВОДНАЯ ТАБЛИЦА ВРЕМЕНИ ВЫПОЛНЕНИЯ (мс)")
print("=" * 70)
pivot_time = df.pivot(index='size', columns='threads', values='time_ms')
print(pivot_time.round(1))
