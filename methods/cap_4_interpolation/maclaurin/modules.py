import numpy as np
import pandas as pd
from sympy import Symbol, diff, init_printing, euler
from math import e, factorial
# e = 2.7182 # works, too, but is imprecise
import sys


N_FLOATING_POINTS = 4

x = Symbol('x')
init_printing(use_unicode=True)

def _f(x, calc:bool = False, truncate_e:bool = True):
	if calc:
		if type(x) not in [float, int]:
			sys.exit(f'Error: x={x} <{type(x)}> should be <float> or <int>')
		if truncate_e:
			return calc_truncate(calc_truncate(e)**x)
		return calc_truncate(e**x)
	if truncate_e:
		return calc_truncate(e)**x
	return e**x

def f(x, calc:bool = False):
	if calc:
		if type(x) not in [float, int]:
			sys.exit(f'Error: x={x} <{type(x)}> should be <float> or <int>')		
			return e**x					
	return e**x

def _calc_derivate(order:int = 1, x_point:float = None):
	if order == 0:
		sys.exit('Order of derivate equal 0 is not allowed, cause the derivate will not be calculated')

	if order == 1:
		deriv = f(x).diff(x)
		if x_point == None:
			return deriv
		else:
			return calc_truncate(deriv.subs(x, x_point))

	deriv_temp = f(x)
	for _ in range(order):
		# print('derivate: ', _)
		deriv_temp = deriv_temp.diff(x)
		# print(deriv_temp)

	if x_point == None:
		return deriv_temp
	else:
		return calc_truncate(deriv_temp.subs(x, x_point))

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

def _calc_Maclaurin_serie(n_serie_terms: int = 4) -> list:

	if n_serie_terms < 1:
		sys.exit(f'Error: n_serie_terms={n_serie_terms} cannot be less than 1')

	print(f'i_term: 0: ', f(0))	
	input('Press')

	# maclaurin_serie: list = [f(0)]
	maclaurin_serie: list = []	

	for i_term in range(1, n_serie_terms):
		print(f'i_term: {i_term}')
		symbolic_derivate = calc_derivate(order=i_term)
		print('symbolic_derivate: ', symbolic_derivate)
		input('Press')
		numerical_derivate = calc_truncate(symbolic_derivate.subs(x, 0))
		print('numerical_derivate: ', numerical_derivate)
		input('Press')
		divisor = factorial(i_term)
		print('divisor: ', divisor)		
		input('Press')

		a = calc_truncate(numerical_derivate/divisor)
		print('a: ', a)
		term = a*(x**i_term)
		print('term: ', term)
		maclaurin_serie.append(term)

	maclaurin_serie.insert(0, f(0))
	return maclaurin_serie

def calc_Maclaurin_serie(n_serie_terms: int = 4) -> list:

	if n_serie_terms < 1:
		sys.exit(f'Error: n_serie_terms={n_serie_terms} cannot be less than 1')

	# print(f'i_term: 0: ', f(0))	
	# input('Press')

	# maclaurin_serie: list = [f(0)]
	maclaurin_serie: list = []	

	for i_term in range(1, n_serie_terms):
		# print(f'i_term: {i_term}')
		symbolic_derivate = calc_derivate(order=i_term)
		# print('symbolic_derivate: ', symbolic_derivate)
		# input('Press')
		numerical_derivate = symbolic_derivate.subs(x, 0)
		# print('numerical_derivate: ', numerical_derivate)
		# input('Press')
		divisor = factorial(i_term)
		# print('divisor: ', divisor)		
		# input('Press')

		a = numerical_derivate/divisor
		# print('a: ', a)
		term = a*(x**i_term)
		# print('term: ', term)
		maclaurin_serie.append(term)

	maclaurin_serie.insert(0, f(0))
	return maclaurin_serie
	
def _calc_li_values_from_Maclaurin_serie(mc_serie:list = None, x_point:float = None) -> list:
	if None in [mc_serie, x_point]:
		sys.exit(f"Error: mc_serie={mc_serie} or x_point={x_point} mustn't be <list> and <float> respectively")

	li_val_from_mc_serie: list = [mc_serie[0]]
	print('mc_serie[0]: ', mc_serie[0])

	for index_term, term in enumerate(mc_serie[1:]):

		print('i_term: ', index_term)
		print(term)
		term_value = calc_truncate(term.subs(x, x_point))
		print('term: ', term_value)
		li_val_from_mc_serie.append(term_value)
		input('Press')

	return li_val_from_mc_serie

def calc_li_values_from_Maclaurin_serie(mc_serie:list = None, x_point:float = None) -> list:
	if None in [mc_serie, x_point]:
		sys.exit(f"Error: mc_serie={mc_serie} or x_point={x_point} mustn't be <list> and <float> respectively")

	li_val_from_mc_serie: list = [mc_serie[0]]
	# print('mc_serie[0]: ', mc_serie[0])

	for index_term, term in enumerate(mc_serie[1:]):

		# print('i_term: ', index_term)
		# print(term)
		term_value = term.subs(x, x_point)
		# print('term: ', term_value)
		li_val_from_mc_serie.append(term_value)
		# input('Press')

	return li_val_from_mc_serie

def calc_truncate(number: float) -> float:
	"""
	Truncate the number to the specified floating points
	"""

	string = str(number)

	if '.' in string:
		for index, elem in enumerate(string):
			if elem == '.':			
				return float(string[:index + 1 + N_FLOATING_POINTS])
	else:
		return float(number)