import numpy as np
from sympy import Symbol, init_printing
from modules import *

x = Symbol('x')
init_printing(use_unicode=True)

table = get_table(file_name='table.csv')

a,b = calc_coefs_min_squares(table)
print(a,b)

fx = calc_line_equation_by_min_squares_method(coefs=[a,b])
print(fx)
