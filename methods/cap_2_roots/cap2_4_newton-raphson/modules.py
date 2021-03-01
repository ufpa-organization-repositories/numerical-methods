import numpy as np

N_FLOATING_POINTS = 4

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


def f(x:float) -> float:
	"""
	Define and calculate f(x) for a given x value
	"""
	
	return calc_truncate(np.exp(-x) - x)

def d1(x: float) -> float:
	"""
	Define and calculate d1 for a given x value
	d1 is the First Order Derivate in realation to x
	"""

	# Return the d1(x)=e^(-x) for a given x
	return calc_truncate((-np.exp(-x)) -1)

def d2(x: float) -> float:
	"""
	Define and calculate d2 for a given x value
	d1 is the First Order Derivate in realation to x
	"""

	# Return the d2(x)=-e^(-x) for a given x
	return calc_truncate(np.exp(-x))

def g(x: float) -> float:
	"""
	Calculate the aproximation
	Xk+1 = G(x) is a aproximation for the next iteration
	"""

	# Return the aproximation G(x)= x - f(x)/d1(x)
	return calc_truncate(x - (f(x)/d1(x)))


# False
def calc_absolut_error(x1: float, x2: float) -> float:
	"""
	Calculate the absolute error for the
	Linear Iteration Method

	x1 = Last Root
	x2 = Current Root

	Rememeber that in each iteration, ROOT = G(Last_ROOT)
	"""	
	return abs(x2 - x1)

