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
# TODO: typehint of matrix (ndarray)
def old_calc_determinant(matrix):
    """
    Calculate the determinant
    (problem. It is imprecise)

    matrix -- the matrix which will be used to calculate the determinant
    Return: return the determinant
    """        

    return round(np.linalg.det(matrix))


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
