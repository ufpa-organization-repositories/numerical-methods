import numpy as np
from sympy import Symbol, diff, init_printing
from math import e

init_printing(use_unicode=True)

x = Symbol('x')

def calc_integral_by_gauss_quadrature_method(a: float, b: float):

	A0 = A1  = (b - a) / 2

	x0 = ((b - a) / 2) * (- 3 ** (- 1 / 2))
	x1 = ((b - a) / 2) * (3 ** (- 1 / 2))

	integral = A0 * f(x0) + A1 * f(x1)
	return integral

def f(x_point = x):					
	return e**x_point