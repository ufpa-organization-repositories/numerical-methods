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


def calc_function(x:float) -> float:
	"""
	Define and calculate f(x) for a given x value
	"""
	
	return calc_truncate(np.exp(-x) - x)


def calc_Bolzano_Theorem(a: float, b: float) -> bool:
	"""
	Verify the Bolzano Theorem from a given a and b values
	Return True if Bolzano Theorem is ok
	"""
	# Calculate f(a) and f(b)
	f_a = calc_function(a)
	f_b = calc_function(b)

	return f_a*f_b < 0


def calc_break_point(a: float, b: float) -> float:
	"""
	Calculate the brak point
	It is important that a and b had already been truncated
	"""
	# a_trunc = calc_truncate(a)
	# b_trunc = calc_truncate(b)
	return calc_truncate((a + b)/2)


def calc_absolut_error(a: float, b: float) -> float:
	"""
	Calculate the absolute error
	"""
	# Calculate f(a) and f(b)
	f_a = calc_function(a)
	f_b = calc_function(b)
	return calc_truncate(f_a - f_b)

