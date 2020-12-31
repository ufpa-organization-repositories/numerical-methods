from modules import *
from sympy import Symbol, diff, init_printing

init_printing(use_unicode=True)

a_point = 0

taylor_serie: list = calc_Taylor_serie(n_serie_terms=4, a_point=a_point)
print('Taylor serie: ', taylor_serie)
l_values_of_the_serie: list = calc_li_values_from_Taylor_serie(tylr_serie=taylor_serie, x_point=5, a_point=a_point)
print('Taylor terms: ', l_values_of_the_serie)
print('f(x) estimated by Taylor serie: ', sum(l_values_of_the_serie))
# value = f(2, calc=True)
# print(value)