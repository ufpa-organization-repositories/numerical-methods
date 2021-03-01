import numpy as np
from sympy import Symbol, init_printing
x = Symbol('x')

def get_table(file_name: str = 'table.csv'):
    return np.genfromtxt(file_name, delimiter=',')[1:, 1:]

def calc_coefs_min_squares(table):
	"""
	Calculte the coeficients of the line equation
	by the mins squares method
	"""	
	n = table.shape[0]
	sum_xy = 0
	sum_x = 0
	sum_y = 0
	sum_x_squared = 0

	for i in range (table.shape[0]):
		_x = table[i][0]
		_y = table[i][1]
		
		sum_xy += (_x * _y)
		sum_x += _x
		sum_y += _y
		sum_x_squared += _x ** 2

	a = ((n * sum_xy) - (sum_x * sum_y)) / ((n * sum_x_squared) - (sum_x ** 2))
	b = (sum_y - (a * sum_x)) / n

	return a, b

def calc_line_equation_by_min_squares_method(coefs: list):
	a, b = coefs[0], coefs[1]
	return (a * x) + b