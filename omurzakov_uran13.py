import math

def task_18():
    print("--- Задача 18 ---")
    x = float(input("Введите значение x (например, 9.03): ").replace(',', '.'))
    eps = 1e-6

    x_red = x % (2 * math.pi)
    if x_red > math.pi:
        x_red -= 2 * math.pi
    if x_red > math.pi / 2:
        x_red = math.pi - x_red
    elif x_red < -math.pi / 2:
        x_red = -math.pi - x_red

    term = x_red
    s = term
    n = 1
    while abs(term) >= eps:
        term *= -x_red**2 / ((2 * n) * (2 * n + 1))
        s += term
        n += 1

    print(f"Приведенный угол: {x_red:.5f}")
    print(f"sin({x}) = {s:.6f}")
    print(f"Количество использованных членов: {n}")


def task_19():
    print("\n--- Задача 19 ---")
    x = float(input("Введите значение x (например, 0.54): ").replace(',', '.'))
    eps = 1e-8

    term = 1.0
    s = term
    k = 0

    while abs(term) >= eps:
        term *= -x**2 / ((2 * k + 1) * (2 * k + 2))
        s += term
        k += 1

    print(f"cos({x}) = {s:.8f}")
    print(f"Число членов: {k}")


def task_20():
    print("\n--- Задача 20 ---")
    t = float(input("Введите значение t (например, 0.43): ").replace(',', '.'))
    eps = 1e-8

    term_e = 1.0
    sum_e = term_e
    k_e = 0
    while abs(term_e) >= eps:
        k_e += 1
        term_e *= t / k_e
        sum_e += term_e

    term_c = 1.0
    sum_c = term_c
    k_c = 0
    while abs(term_c) >= eps:
        k_c += 1
        term_c *= -t**2 / ((2 * k_c - 1) * (2 * k_c))
        sum_c += term_c

    F = sum_e * sum_c
    true_F = math.exp(t) * math.cos(t)
    error = abs(F - true_F)

    print(f"F({t}) = {F:.8f}")
    print(f"Число членов для e^t: {k_e}")
    print(f"Число членов для cos(t): {k_c}")
    print(f"Ошибка относительно библиотечных функций: {error:.2e}")


if __name__ == "__main__":
    task_18()
    task_19()
    task_20()