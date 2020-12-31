import numpy as np

def get_table(file_name: str = 'table.csv'):
    return np.genfromtxt(file_name, delimiter=',')[1:, 1:]

def calc_integral_by_second_simpson_rule(table):
	sum_y_prod_332: int = 0
	y0 = table[0][1]
	yn = table[-1][1]
	h = table[1][0] - table[0][0]	

	coefs = [3,3,2]
	length_coefs = len(coefs)
	j = 0
	for i, y in enumerate(table[1:-1,1]):		
		if j < length_coefs:
			pass
		else:
			j = 0		
		sum_y_prod_332 += (coefs[j] * y)
		j += 1

	integral = ((3*h)/8) * (y0 + sum_y_prod_332 + yn)
	return integral