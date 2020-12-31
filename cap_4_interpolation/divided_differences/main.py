
"""
author: Bruno Conde Costa da Silva
"""

import numpy as np
from sympy import init_printing, Symbol
from modules import *

"""
ok STEP 01: Get y0 from table
ok STEP 02: Get the x's of the iteration
ok STEP 03: For each iteration, calculate the products of the x's (symbolycally)
ok STEP 04: For each iteration, calculate the derivate of each derivate column
STEP 05: Calc f(x) by interpolation
STEP 06: Calc f(x) from each table point and see it matches
STEP 07: Calc f(x) from points between the table points and see if the aproximation is ok
STEP 08: Calc f(x) from point outside the table points interval (outside [x0, .. ,xn])
STEP 09: Plot f(x) together with table points
"""


init_printing(use_unicode=True)
x = Symbol('x')
table = get_table(file_name='table.csv')

"""
way 1: given the table and the x point, returning the function value in the x point
"""
x_point = 0.02
fx = calc_finite_differences(table, x_point)
print('fx: ', fx)

print('\n############################################\n')

"""
way 2: given the table only, returning the interpolation function to calculate in wherever x point you want
"""
fx = calc_finite_differences(table)
print('interpolation function: ', fx)
print('fx: ', fx.subs(x, x_point))
