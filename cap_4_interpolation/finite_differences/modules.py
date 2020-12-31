import numpy as np
from sympy import Symbol, init_printing
"""
ok STEP 01: calculate h <- x1 - x0 (the same for entire algorithm)
ok STEP 02: calculate z <- (x - x0) / h (calculated for the x of the desired f(x))
ok STEP 03: calculate factorials
ok STEP 04: calculate derivates
STEP 05: term = (derivative / factorial) * z
"""
x = Symbol('x')

def get_table(file_name: str = 'table.csv'):
    return np.genfromtxt(file_name, delimiter=',')[1:, 1:]

def calc_finite_differences(table, x_point = x, debug=False):
    """
    Calculate the finite differences
    if x_point is x symbol (default), then return the expression
    if x_point is a number, then reuturn the function value at the given x_point
    """

    # read y0 from table
    interpolation_function_definition_or_value: float = 0 
    y_tbl = table[:, -1].reshape(table.shape[0], 1)
    y0 = y_tbl[0][0]

    # initialize the value    
    interpolation_function_definition_or_value = y0

    # initialize the algorithm
    li_terms: list = []    

    li_d1: list = []

    h = table[1][0] - table[0][0]    
    z = (x_point - table[0][0]) / h
    
    z_expression = z    
    for iteration in range(table.shape[0] - 1):

        if debug == True:
            print(f'\n---->>>iteration: {iteration}')
        """
        term = (derivative / factorial) * z_expression
        """
        term = 0
        derivative = 0
        factorial = calc_factorial(iteration + 1)
        # print('factorial: ', factorial)

        if iteration > 0:                    
            z_expression *= (z - (iteration))            
        # print('z_expression: ', z_expression)

        d1 = table[iteration + 1][1] - table[iteration][1]
        li_d1.append(d1)        

        derivative = li_d1[-1]
        for d in li_d1[:-1]:
            derivative -= d
        # print('derivative: ', derivative)

        term = (derivative / factorial) * z_expression

        if debug == True:
            print(f'term: ({derivative} / {factorial}) * {z_expression}')

        interpolation_function_definition_or_value += term

    return interpolation_function_definition_or_value


def calc_factorial(number: int):
    factorial = 1
    if not number == 0:        
        for _i in range(number):                
            factorial *= (_i + 1)
    return factorial
