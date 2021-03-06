import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


N_FLOATING_POINTS = 4


def calc_x(m_coef, vet_b, vet_x):		
	
	li_x = []

	for i, line in enumerate(m_coef):		
		arr_a = []
		arr_x = []
		divisor = m_coef[i][i]		

		for j, coef in enumerate(line):			
			if j != i:				
				arr_a.append(m_coef[i][j])
				arr_x.append(vet_x[j])						

		b = vet_b[i]
		arr_a = np.array(arr_a)
		arr_x = np.array(arr_x)

		x = calc_truncate(float((b) - calc_truncate(sum(arr_a * arr_x)))/divisor)

		li_x.append(x)

	return np.array(li_x)


def get_matrix(file_name: str = 'input.csv'):
    """
    Load a matrix from a csv file
    Return a numpy.ndarray (without labels) of the csv file
    - file_name: .csv file which content the matrix

    x1  |   x2  |   x3

    a1  |   a2  |   a3

    a2  |   a2  |   a3
    """
    df = pd.read_csv(file_name)

    matrix = df.values
    # n_lines = df.shape[0]
    # n_columns = df.shape[1]

    return matrix


def get_y_matrix(file_name: str = 'y_input.csv'):
    """
    Load a matrix from a csv file
    Return a numpy.ndarray (without labels) of the csv file
    - file_name: .csv file which content the matrix

    Y is a vector: matrix nx1)    
    """

    df = pd.read_csv(file_name)
    y = df.values

    return y[:, 0]


def get_x_initial(file_name: str = 'x_initial.csv'):
    """
    Load the x initial vector from a csv file
    Return a numpy.ndarray (without labels) of the csv file
    - file_name: .csv file which content the vector

    x⁽⁰⁾

    x1

    x2

    x3
    """
    df = pd.read_csv(file_name)

    x_init = df.values
    # n_lines = df.shape[0]
    # n_columns = df.shape[1]

    return x_init[0]


def calc_truncate(number: float) -> float:
	"""
	Truncate the number to the specified floating points
	"""

	string = str(number)

	if '.' in string:
		for index, elem in enumerate(string):
			if elem == '.':			
				return float(string[:index + 1 + N_FLOATING_POINTS])
	else:
		return float(number)


def calc_error(last_x, current_x):
	"""
	Calculate the error	
	"""

	# this entire array can be returned in future
	x_arr_error_temp = np.zeros_like(current_x)
	i = 0

	for x_past, x_current in zip(last_x, current_x):
		error_x = calc_truncate(abs(x_past - x_current))
		
		x_arr_error_temp[i] = error_x

	return max(x_arr_error_temp)


def check_line_criteria(mat):
	"""
	It is necessary and suficient condition to the algorithm converge
	"""
	_condition_by_line = np.zeros_like(mat[0])

	for i in range(mat.shape[0]):
		sum_line_coefs = 0
		coef_diag_primary = 0
		for j in range(mat.shape[1]):
			if i == j:
				coef_diag_primary = abs(mat[i][j])
			else:
				sum_line_coefs += abs(mat[i][j])

		if calc_truncate(sum_line_coefs) < calc_truncate(coef_diag_primary):
			_condition_by_line[i] = True
		else:
			_condition_by_line[i] = False

	return _condition_by_line


def plot_errors(y_axis, x_axis = None, file_name:str = 'plot_errors.png'):

	if x_axis == None:
		x_axis = list(range(len(y_axis)))

	plt.title('Gauss Jacob\nErrors per iterations')
	plt.scatter(x_axis, y_axis, color="Black")
	plt.plot(x_axis, y_axis, color="Black")
	plt.xlabel('Iteration')
	plt.ylabel('Error')	

	if '.' not in file_name and 'png' not in file_name[-3:]:
		file_name += '.png'

	plt.savefig(file_name, dpi=140)
	plt.close()
