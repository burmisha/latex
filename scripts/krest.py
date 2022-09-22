import random

m_values = [0.100, 0.150, 0.200, 0.250, 0.300, 0.350, 0.400]
g = 9.81
dm = 0.01
dx = 0.002


def delta(max_v):
    return max_v * (random.random() - 0.5) * 2


def get(k, beta_k):
    beta = dm * g / (max(m_values) ** 2) * beta_k
    print(f'k={k}\tbeta_k={beta_k}')
    for m in m_values:
        real_m = m + delta(dm)
        real_m_g = real_m * 1000
        real_x = (m * g + beta * m ** 2) / k + delta(dx)
        real_x_sm = real_x * 100
        print(f'{real_m_g:.1f}\t{real_x_sm:.2f}')
    print('')


get(60, 0)
get(80, 10)
get(100, 30)
