import heapq
import time

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

formula = input("функция f(x): ").strip()
a = float(input("левая границу a: "))
b = float(input("Введите правую границу b: "))
eps = float(input("Введите точность eps: "))
mode = input("min или max?: ").strip().lower()
L = float(input("Введите корректную верхнюю оценку константы Липшица L: "))

x = sp.symbols("x")
expression = sp.sympify(formula.replace("f(x)=", "").strip(), locals={"x": x, "pi": sp.pi})
function = sp.lambdify(x, expression, "numpy")
direction = 1 if mode == "min" else -1


def value(point):
    return direction * float(function(point))


def interval(left, right):
    yl, yr = points[left], points[right]
    candidate = (left + right) / 2 + (yl - yr) / (2 * L)
    lower_bound = (yl + yr - L * (right - left)) / 2
    return lower_bound, candidate


start = time.perf_counter()
points = {a: value(a), b: value(b)}
best_x = min(points, key=points.get)
best_value = points[best_x]
queue = []

def add_interval(left, right):
    lower_bound, candidate = interval(left, right)
    heapq.heappush(queue, (lower_bound, left, right, candidate))

add_interval(a, b)
iterations = 0

while best_value - queue[0][0] > eps:
    _, left, right, candidate = heapq.heappop(queue)
    candidate_value = value(candidate)
    points[candidate] = candidate_value
    if candidate_value < best_value:
        best_x, best_value = candidate, candidate_value
    add_interval(left, candidate)
    add_interval(candidate, right)
    iterations += 1

elapsed = time.perf_counter() - start
error_bound = best_value - queue[0][0]
extreme_value = direction * best_value

print(f"x экстремума: {best_x:.10g}")
print(f"f(x): {extreme_value:.10g}")
print(f"L: {L:g}; eps: {eps:g}")
print(f"Итераций: {iterations}; вычислений функции: {len(points)}")
print(f"Зазор оценки: {error_bound:.6g}; время поиска: {elapsed:.6f} с")

plot_x = np.linspace(a, b, 1600)
plot_y = function(plot_x)
sample_x = sorted(points)
plt.plot(plot_x, plot_y, label="Исходная функция")
plt.scatter(sample_x, [direction * points[p] for p in sample_x], s=14,
            label="Вычисленные точки", zorder=3)

for left, right in zip(sample_x, sample_x[1:]):
    lower_bound, candidate = interval(left, right)
    plt.plot([left, candidate, right],
             [direction * points[left], direction * lower_bound, direction * points[right]],
             "--", color="darkorange", alpha=0.8,
             label="Итоговая ломаная оценок" if left == sample_x[0] else None)

plt.scatter([best_x], [extreme_value], color="red", s=45,
            label="Найденный экстремум", zorder=4)
plt.title("Глобальный экстремум методом ломаных Пиявского")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid(alpha=0.25)
plt.legend()
plt.tight_layout()
plt.savefig("method_lomanykh.png", dpi=180)
plt.show()
