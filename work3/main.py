import sympy as sp

x, y, lam = sp.symbols("x y lam", real=True)

f = x**2 + y**2
h = x + 2*y - 5
L = f + lam*h

equations = [
    sp.diff(L, x),
    sp.diff(L, y),
    sp.diff(L, lam),
]

solutions = sp.solve(equations, (x, y, lam), dict=True)

print("Решения системы:", solutions)

for sol in solutions:
    print("Невязка ограничения:", sp.simplify(h.subs(sol)))
    print("Значение функции:", sp.simplify(f.subs(sol)))