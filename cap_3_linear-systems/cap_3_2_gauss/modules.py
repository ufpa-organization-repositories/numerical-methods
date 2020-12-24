import pandas as pd
import numpy as np


N_FLOATING_POINTS = 4


def get_matrix(file_name: str):
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

# TODO: typehint of matrix (ndarray)
def get_y_matrix(file_name: str):
    """
    Load a matrix from a csv file
    Return a numpy.ndarray (without labels) of the csv file
    - file_name: .csv file which content the matrix

    Y is a vector: matrix nx1)    
    """

    df = pd.read_csv(file_name)
    y = df.values

    return y

def calc_determinant(matrix) -> float:

    """
    axis 0 = linha
    axis 1 = column
    """
    DETERMINANT = 0
    
    diagonal = matrix.diagonal()
    # print('primary diagonal: (+)', diagonal)
    DETERMINANT += diagonal.prod()

    seconday_diagonal = np.flipud(matrix).diagonal()[::-1]
    # print('secondary diagonal: (-)', seconday_diagonal)
    DETERMINANT -= seconday_diagonal.prod()    

    for signal in [1, -1]:
        # print(' _____________________________({})'.format(['+' if signal > 0 else '-'][0]))

        matrix_aux = np.zeros_like(matrix)
        col_aux = []
        # n_diagonals = [matrix.shape[1] - 1 if matrix.shape[0] == matrix.shape[1] else matrix.shape[1]][0]

        n_diagonals = [matrix.shape[1] - 1 if not matrix.shape[0]==matrix.shape[1]==2 else 0][0]

        # print('n_diagonals ', n_diagonals, end='\n\n')

        
        if signal == 1 and n_diagonals != 0:        

            for c in [i for i in range(0, matrix.shape[1])[::signal]][:n_diagonals]:

                # print(c)
                col_aux.append(c)

                a = matrix[:,col_aux]   
                matrix_aux = np.delete(matrix, col_aux, axis=1)
                matrix_aux = np.append(matrix_aux, a, axis=1)
                # print(matrix_aux)

                diagonal = matrix_aux.diagonal()
                # print('primary diagonal: ', diagonal)

                DETERMINANT += diagonal.prod()



        elif signal == -1 and n_diagonals != 0:

            for c in [i for i in range(0, matrix.shape[1])[::signal]][:n_diagonals]:

                # print(c)
                col_aux.append(c)

                a = matrix[...,col_aux[-1]:]
                # print('->>>a')
                # print(a)
                matrix_aux = np.delete(matrix, col_aux[::signal], axis=1)
                # print(matrix_aux)
                matrix_aux = np.append(a, matrix_aux, axis=1)
                # print(matrix_aux)

                seconday_diagonal = np.flipud(matrix_aux).diagonal()[::-1]
                # print('secondary diagonal: ', seconday_diagonal)

                DETERMINANT -= seconday_diagonal.prod()


    # print(f'\n>>> DETERMINANT: {DETERMINANT}\n')
    return DETERMINANT

def calc_dets(x, y) -> list:
    """
    Calc the dets (1 to n)
    """
        # n_diagonals = [matrix.shape[1] - 1 if not matrix.shape[0]==matrix.shape[1]==2 else 0][0]

    # li_dets = np.array([])
    li_dets = []    

    # if n_diagonals > 0:
    for i in range(x.shape[1]):

        x_temp = x.copy()
        x_temp[:,[i]] = y

        det = calc_determinant(x_temp)
        print(det)
        # np.append(li_dets, det, axis=0)
        li_dets.append(det)

    return li_dets

def calc_x(DET, dets: list) -> list:
    """
    Calculate the x
    DET - is the Determinant of tha coeficient matrix
    dets - is a list of determinants

    return the list of the calculated x values
    """
    li_x = []

    for det in dets:
        x_value = calc_truncate(det/DET)
        li_x.append(x_value)

    return li_x

def calc_multiplicators(matrix, pivot):
    """
    Calculate the multiplicators of a matrix
    - matrix: is the matrix of the coeficients
    - pivot: is the first line of the matrix of the coeficients

    RETURN: matrix with multiplicators
    """

    matrix_with_multiplicators = matrix.copy()

    new_column_1 = matrix[:,0].copy().reshape(matrix.shape[0], 1)


    for i, coef in enumerate(matrix[1:,0]):        
                         
        m = calc_truncate(coef/pivot[0])
        # print(m)
        matrix_with_multiplicators[i + 1,0] = m

    return matrix_with_multiplicators

def calc_elements(matrix_with_multiplicators, matrix, y_matrix, pivot):
    """
    calculate the elements (new coeficients)
    RERTURN -> new matrix
    """
    matrix_aux = matrix.copy()
    y_matrix_aux = y_matrix.copy()

    i_piv = 0
    pivot_b = y_matrix[i_piv]

    i_line = 1
    for line_0, line_1, b_0 in zip(matrix[1:,], matrix_with_multiplicators[1:,], y_matrix[1:,]):        
        
        m = line_1[0]

        arr_a = np.array([])        

        for coef_0, coef_1, piv in zip(line_0, line_1, pivot):
            a = coef_0 - m * piv
            arr_a = np.append(arr_a, a)
        
        b = b_0 - m * pivot_b

        # print(arr_a, b)                

        matrix_aux[i_line] = arr_a
        y_matrix_aux[i_line] = b

        i_line += 1

    return matrix_aux, y_matrix_aux

def calc_num_coefs_bellow_main_diagonal_different_from_zero(matrix) -> int:
    n_zero_coefs = 0
    
    i = 1

    for line in matrix[1:,]:
        for j in range(i):
            # print(line[j])
            if line[j] != 0:
                # print('>0')
                n_zero_coefs += 1

        i += 1

    return n_zero_coefs

        

        

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
