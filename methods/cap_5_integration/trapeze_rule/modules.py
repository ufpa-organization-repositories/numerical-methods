import numpy as np

def get_table(file_name: str = 'table.csv'):
    return np.genfromtxt(file_name, delimiter=',')[1:, 1:]

def calc_integral_by_trapeze_method(table):
	sum_y_prod_2 = sum([y*2 for y in table[1:-1,1]])
	y0 = table[0][1]
	yn = table[-1][1]
	h = table[1][0] - table[0][0]

	integral = h/2 * (y0 + sum_y_prod_2 + yn)
	return integral