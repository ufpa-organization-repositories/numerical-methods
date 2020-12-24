import numpy as np
from modules import *

"""
STEP 1: Test lines criteria	until it be satisfied (guarantee the convergecy)
STEP 2: Build equations of the iterative scheme
STEP 3: initial "chute"

(INITIALIZE )

STEP 4: Calculate x⁽k⁺¹⁾
STEP 5: Verify if the stop criteria is reached. If it have been reached, stop. Else, make k = + 1 and come back to STEP 4
"""


ERROR_TRESHOLD = float(10 ** (-2))
STOP_CONDITION = False
N_ITERATIONS = 10

di_plot = {'errors':np.array([])}

matrix = get_matrix('input.csv')

criteria_by_line = check_line_criteria(matrix)
print(criteria_by_line)

if False in criteria_by_line:
	print('Line criteria: False')

else:
	print('Line criteria: OK')

	y_matrix = get_y_matrix('y_input.csv')

	x_initial = get_x_initial('x_initial.csv')	

	print('x_initial\n', x_initial)
	x_new = calc_x(matrix, y_matrix, x_initial)

	error = calc_error(x_initial, x_new)
	print(error)

	di_plot['errors'] = np.append(di_plot['errors'], np.array([error]), axis = 0)

	if error <= ERROR_TRESHOLD:
		print('STOP')
		STOP_CONDITION = True

	else:
		print('CONTINUE')		

		k = 0
		while not STOP_CONDITION:						
			print(f'________Iteration: {k}________')

			x_old = x_new.copy()
			x_new = calc_x(matrix, y_matrix, x_old)
			error = calc_error(x_old, x_new)
			print("ERROR: ", error)
			di_plot['errors'] = np.append(di_plot['errors'], np.array([error]), axis = 0)


			STOP_CONDITION = (error <= ERROR_TRESHOLD) or (k == N_ITERATIONS)
			k += 1			

print(di_plot['errors'])
plot_errors(y_axis=di_plot['errors'])