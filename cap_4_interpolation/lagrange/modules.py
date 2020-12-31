import numpy as np
from sympy import Symbol, init_printing

x = Symbol('x')

def get_table(file_name: str = 'table.csv'):
    return np.genfromtxt(file_name, delimiter=',')[1:, 1:]

def calc_lagrange_polynomial(tbl = None):
    """
    Calculate the lagrande polynomial
    """
    x_tbl = tbl[:, :-1]
    y_tbl = tbl[:, -1].reshape(tbl.shape[0], 1)
    
    li_a_inv = []
    li_x = []

    for i, line in enumerate(x_tbl):
            
        a = 1       
        a_dividend = 1
        x_products = 1
        for i2, line2 in enumerate(x_tbl):
            for j, elem in enumerate(line2):
                if not i2 == i:                 
                    a_dividend *= (x_tbl[i][0] - x_tbl[i2][0])
                    x_products *= (x - x_tbl[i2][0])

        a = a_dividend
        li_a_inv.append(a)
        
        li_x.append(x_products)

    return calc_f_by_interpolation(l_a=li_a_inv, l_x=li_x, tb_y=y_tbl)

def calc_f_by_interpolation(l_a, l_x: list, tb_y):
    """
    Interpolation the lagrande polynomium with the table
    """
    func = 0
    for a_val, x_expression, y_val in zip(l_a, l_x, tb_y):
        
        p = (x_expression / a_val) * y_val       
        func += p

    return func[0]