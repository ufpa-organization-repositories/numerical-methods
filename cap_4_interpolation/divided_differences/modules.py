import numpy as np
from sympy import Symbol, init_printing

x = Symbol('x')

def get_table(file_name: str = 'table.csv'):
    return np.genfromtxt(file_name, delimiter=',')[1:, 1:]

def calc_divided_differences(table):
    li_derivatives: list = []
    li_x_expressions: list = []

    x0 = table[0][0]    
    for iteration in range(table.shape[0] - 1):
        # print(f'iteration: {iteration}')

        x_expression = 1
        derivative = 0        
        derivative_dividend = 0
        derivative_divisor = 0

        # detivatives of first order
        li_derivative_first_order: list = []
        for i in range(iteration + 1):
            x_val = table[i][0] # 02        
            x_expression *= (x - x_val) # 03

            fa = table[i][1]
            fb = table[i + 1][1]
            a = x_val
            b = table[i + 1][0]

            deriv = (fa - fb)/(a - b)
            # print(iteration, i, deriv)            
            li_derivative_first_order.append(deriv)
            if li_derivatives == []:
                li_derivatives.append(deriv)

        li_x_expressions.append(x_expression)

        # other derivatives
        derivative_dividend = li_derivative_first_order[-1]

        for d in li_derivative_first_order[:-1]:            
            derivative_dividend -= d

        x_iteration = table[iteration + 1][0]
        derivative_divisor = x_iteration - x0
        derivative = derivative_dividend/(x_iteration - x0)
        # print(derivative)

        if not iteration == 0:
            li_derivatives.append(derivative)

    # print(len(li_derivatives), li_derivatives)
    # print(len(li_x_expressions), li_x_expressions)

    y_tbl = table[:, -1].reshape(table.shape[0], 1)
    y0 = y_tbl[0][0]

    return calc_interpolation_function(y0, li_derivatives, li_x_expressions)

def calc_interpolation_function(y0, l_derivatives, l_x_expressions):
    # print('calc interpolation')
    f = y0
    for derivative, x_expression in zip(l_derivatives, l_x_expressions):
        term = derivative * x_expression
        f += term
            
    return f

