from modules import *
from sympy import Symbol, diff, init_printing

init_printing(use_unicode=True)

integral = calc_integral_by_gauss_quadrature_method(a=-1, b=1)
print(integral)
