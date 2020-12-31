import numpy as np
import pandas as pd
from sympy import Symbol, diff, init_printing, euler
from math import e, factorial
# e = 2.7182 # works, too, but is imprecise
import sys


N_FLOATING_POINTS = 4

x = Symbol('x')
a_symbol = Symbol('a')

init_printing(use_unicode=True)

def f(x, calc:bool = False):
	if calc:
		if type(x) not in [float, int]:
			sys.exit(f'Error: x={x} <{type(x)}> should be <float> or <int>')		
			return e**x					
	return e**x

def calc_derivate(order:int = 1, x_point:float = None):
	if order == 0:
		sys.exit('Order of derivate equal 0 is not allowed, cause the derivate will not be calculated')

	if order == 1:
		deriv = f(x).diff(x)
		if x_point == None:
			return deriv
		else:
			return deriv.subs(x, x_point)

	deriv_temp = f(x)
	for _ in range(order):
		# print('derivate: ', _)
		deriv_temp = deriv_temp.diff(x)
		# print(deriv_temp)

	if x_point == None:
		return deriv_temp
	else:
		return deriv_temp.subs(x, x_point)

def calc_Taylor_serie(n_serie_terms: int = 4, a_point: float = None) -> list:

	if n_serie_terms < 1:
		sys.exit(f'Error: n_serie_terms={n_serie_terms} cannot be less than 1')

	if a_point == None:
		sys.exit(f'Error: a_point={a_point} must be float')

	# print(f'i_term: 0: ', f(0))	
	# input('Press')

	# maclaurin_serie: list = [f(0)]
	taylor_serie: list = []	

	for i_term in range(1, n_serie_terms):
		# print(f'i_term: {i_term}')
		symbolic_derivate = calc_derivate(order=i_term)
		# print('symbolic_derivate: ', symbolic_derivate)
		# input('Press')
		numerical_derivate = symbolic_derivate.subs(x, a_point)
		# print('numerical_derivate: ', numerical_derivate)
		# input('Press')
		divisor = factorial(i_term)
		# print('divisor: ', divisor)		
		# input('Press')

		a = numerical_derivate/divisor
		# print('a: ', a)
		term = a*((x - a_symbol)**i_term)
		# print('term: ', term)
		taylor_serie.append(term)

	taylor_serie.insert(0, f(a_point))
	return taylor_serie

def calc_li_values_from_Taylor_serie(tylr_serie:list = None, x_point:float = None, a_point: float = None) -> list:
	if None in [tylr_serie, x_point, a_point]:
		sys.exit(f"Error: tylr_serie={tylr_serie}, x_point={x_point} or a_point={a_point} must be <list>, <float> and <float> respectively")

	li_val_from_tylr_serie: list = [tylr_serie[0]]
	# print('mc_serie[0]: ', mc_serie[0])

	for index_term, term in enumerate(tylr_serie[1:]):

		# print('i_term: ', index_term)
		# print(term)
		term_value = term.subs([(x, x_point), (a_symbol, a_point)])
		# print('term: ', term_value)
		li_val_from_tylr_serie.append(term_value)
		# input('Press')

	return li_val_from_tylr_serie