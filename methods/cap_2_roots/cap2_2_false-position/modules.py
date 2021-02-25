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


def calc_Bolzano_Theorem(a: float, b: float) -> bool:
	"""
	Verify the Bolzano Theorem from a given a and b values
	Return True if Bolzano Theorem is ok
	"""
	# Calculate f(a) and f(b)
	f_a = f(a)
	f_b = f(b)

	return f_a*f_b < 0

# Bissection
# def calc_break_point(a: float, b: float) -> float:
# 	"""
# 	Calculate the brak point
# 	It is important that a and b had already been truncated
# 	"""
# 	# a_trunc = calc_truncate(a)
# 	# b_trunc = calc_truncate(b)
# 	return calc_truncate((a + b)/2)

# False position
def calc_break_point(a: float, b: float):
	a, f_a = calc_truncate(a), calc_truncate(f(a))
	b, f_b = calc_truncate(b), calc_truncate(f(b))

	# print(a, f_a)
	# print(b, f_b)

	return calc_truncate((a*f(b) - b*f(a)/(f(b) - f(a))))

def calc_absolut_error(x1: float, x0: float) -> float:
	"""
	Calculate the absolute error
	"""		
	return abs(abs(x1) - abs(x0))

