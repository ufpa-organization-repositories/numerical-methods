from modules import *
from sympy import Symbol, diff, init_printing

init_printing(use_unicode=True)

maclaurin_serie: list = calc_Maclaurin_serie(n_serie_terms=4)
print('Maclaurin serie: ', maclaurin_serie)
l_values_of_the_serie: list = calc_li_values_from_Maclaurin_serie(mc_serie=maclaurin_serie, x_point=5)
print('Maclaurin terms: ', l_values_of_the_serie)
print('f(x) estimated by Maclaurin serie: ', sum(l_values_of_the_serie))
# value = f(2, calc=True)
# print(value)