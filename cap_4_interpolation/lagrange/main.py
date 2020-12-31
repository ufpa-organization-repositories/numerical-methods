import numpy as np
from sympy import init_printing, Symbol
from modules import *

init_printing(use_unicode=True)
# x = Symbol('x') # works without this line

table = get_table(file_name='table.csv')
fx = calc_lagrange_polynomial(tbl=table)

print(fx)
print(fx.subs(x, 2))

fx.subs(x, 2)