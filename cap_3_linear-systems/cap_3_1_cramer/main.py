import pandas as pd
import numpy as np
from modules import *


matrix = get_matrix(file_name='input.csv')
print(matrix)

y_matrix = get_y_matrix(file_name='y_input.csv')

DETERMINANT = calc_determinant(matrix=matrix)
print(f'\n>>> DETERMINANT: {DETERMINANT}\n')

print(y_matrix)

determinants = calc_dets(x=matrix, y=y_matrix)
print(determinants)

li_x = calc_x(DET=DETERMINANT, dets=determinants)
print(li_x)
