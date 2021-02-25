import numpy as np

def get_table(file_name: str = 'table.csv'):
    return np.genfromtxt(file_name, delimiter=',')[1:, 1:]

def calc_integral_by_second_simpson_rule(table):
	sum_y_prod_4_and_2: int = sum([4*y if i % 2 == 0 else 2*y for i, y in enumerate(table[1:-1,1])])
	y0 = table[0][1]
	yn = table[-1][1]
	h = table[1][0] - table[0][0]

	integral = h/3 * (y0 + sum_y_prod_4_and_2 + yn)
	return integral