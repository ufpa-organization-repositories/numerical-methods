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

def g(x: float) -> float:
	"""
	Define and calculate g(x) for a given x value
	1. Define f(x)
	2. Isolate x in f(x)
	3. Make x = G(x)
	4. if G(x) is continuous in [a,b] AND |G'(x)| < 1
		5. Choose G(x)
	5. else:
		Isolate x again and Choose another G(x) that satisfies the conditions above
	"""

	# Return the G(x)=e^(-x) for a given x
	return calc_truncate(np.exp(-x))


def calc_Bolzano_Theorem(a: float, b: float) -> bool:
	"""
	Verify the Bolzano Theorem from a given a and b values
	Return True if Bolzano Theorem is ok
	"""
	# Calculate f(a) and f(b)
	f_a = f(a)
	f_b = f(b)

	return f_a*f_b < 0


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

