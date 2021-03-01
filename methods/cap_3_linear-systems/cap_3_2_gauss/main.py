import pandas as pd
import numpy as np
from modules import *


n_iterations = 2

MATRIX = None
PIVOT = None
MATRIX_WITH_MULTIPLICATORS = None
Y_MATRIX = None
n_coefs_diff_zero = None


# STEP 0: get the matrix of the coefs
MATRIX = get_matrix('input.csv')
Y_MATRIX = get_y_matrix('y_input.csv')


for k in range(n_iterations):
	print(f'______________>> ITERATION: {k + 1} ___________________')

	# STEP 1.1: Elect the first line as pivot (reference)
	PIVOT = MATRIX[k,:]
	print('----pivot----')	
	print(PIVOT)

	# STEP 1.2: Calculate the multiplicators for the next lines
	# (in this case of this example, for the next two lines)

	MATRIX_WITH_MULTIPLICATORS = calc_multiplicators(MATRIX, PIVOT, k)
	# print('MATRIX_WITH_MULTIPLICATORS: \n\n', MATRIX_WITH_MULTIPLICATORS)
	# break
	# print(matrix_with_multiplicators)

	# STEP2:Calculate the elements (new coeficients)
	MATRIX, Y_MATRIX = calc_elements(MATRIX_WITH_MULTIPLICATORS, MATRIX, Y_MATRIX, PIVOT)
	print('----matrix----')
	print(MATRIX)

	# print(y_matrix)

	# STEP 3: Check if the coefs above the main diagonal are = 0.
	# If True, stop the program
	# If False, back to STEP 1

	n_coefs_diff_zero = calc_num_coefs_bellow_main_diagonal_different_from_zero(MATRIX)
	print(n_coefs_diff_zero)
	# break

	if n_coefs_diff_zero == 0 or k == n_iterations - 1:		
		print('STOP')
