from sympy import symbols, Eq, solve

# Define symbols
a, b, c = symbols('a b c')

# Known values
x1, y1 = 2025, 621765841
x2, y2 = 2050, 621765841 / 2
x3, y3 = 2070, 0

# Define the three equations
eq1 = Eq(a * x1**2 + b * x1 + c, y1)
eq2 = Eq(a * x2**2 + b * x2 + c, y2)
eq3 = Eq(a * x3**2 + b * x3 + c, y3)

# Solve the system of equations
solution = solve((eq1, eq2, eq3), (a, b, c))
print(solution)

from sympy import Rational

# Given decimal approximations
a_val = -69085.0934444444
b_val = 269086438.966111
c_val = -260986211759.750

# Convert to Rational (fraction) approximations
a_frac = Rational(a_val).limit_denominator()
b_frac = Rational(b_val).limit_denominator()
c_frac = Rational(c_val).limit_denominator()

print("a =", a_frac)
print("b =", b_frac)
print("c =", c_frac)
