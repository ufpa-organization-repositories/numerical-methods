import numpy as np
import matplotlib.pyplot as plt
from modules import *


ERROR_THRESHOLD = 0.01
N_MAX_ITERATIONS = 10


# Entrada de valores

# Passo 1: definir [a,b] a partir de análise visual
a = calc_truncate(0)
b = calc_truncate(1)

# Output: Receives the ROOT retrivied for the program
ROOT = None
ERROR = None

# Iteration
i = -1
a_b_array = np.array([])
x_array = np.array([])
y_array = np.array([])
error_array = np.array([])
iteration_array = np.array([])

breakpoint_array = np.array([])


STOP_CONDITION = False

BOLZANO = calc_Bolzano_Theorem(a=a, b=b)
if not BOLZANO:
	print(f'There is no ROOT in [a,b]=[{a},{b}]')
	print('>>> CHOOSE ANOTHER [a,b] INTERVAL <<<')

else:
	while not STOP_CONDITION:
		i = i + 1
		print('\n__________________________\nITERATION: ', i)
		iteration_array = np.append(iteration_array, [i])

		BOLZANO = calc_Bolzano_Theorem(a=a, b=b)

		if BOLZANO:
			# Passo 2.1: Calcular o ponto de quebra (interseção)
			break_point = calc_break_point(a, b)
			y_array = np.append(y_array, [f(break_point)])
			print('break_point: ', break_point)
			breakpoint_array = np.append(breakpoint_array, break_point)


			# Passo 2.2: Calcular f(break_point)
			f_break_point = f(break_point)
			print('f_break_point: ', f_break_point)

		
		# Passo 3.1: Checar f(break_point) == 0, então break_point é a raiz
		# Caso raiz, parar  processo
		# Caso não for raiz, continuar o processo

		if f_break_point == 0:
			print('f_break_point == 0\nStop the program')
		else:
			print('f_break_point != 0\nContinue the program')

			# Passo 3.2: Checar o teorema de bolzano

			if calc_Bolzano_Theorem(a, break_point):
				print('Bolzano: OK\n[a, f_break_point]')	
				a, b = a, break_point				
			
			elif calc_Bolzano_Theorem(break_point, b):
				print('Bolzano: OK\n[f_break_point, b]')		
				a, b = break_point, b

			else:
				print('Bolzano: NOT OK\nTHERE IS NO ROOT IN THE INTERVAL')
				STOP_CONDITION = True
				break

			print(f'[a={a},b={b}]')

			# Passo 4: Check the conditions to stop the program
			# input("STEP 4: press t continue ...")
			# Do not check for the first iteration (i=0)

			x_array = np.append(x_array, [calc_truncate((a + b)/2)])			
			a_b_array = np.append(a_b_array, np.array([(a, b)]))			

			
			print('ITERATION: ', i)
			print('INTERVAL: [{},{}]'.format(str(a), str(b)))
			print('ROOT: ', break_point)

			if i > 0:

				print(breakpoint_array[-1], breakpoint_array[-2])
				error = calc_absolut_error(x0=breakpoint_array[-1], x1=breakpoint_array[-2])
				error_array = np.append(error_array, [error])

				print('ERROR: ', error)

				if error < ERROR_THRESHOLD or i == N_MAX_ITERATIONS:
					print('Stop the program')
					ROOT = breakpoint_array[-1]
					ERROR = error
					STOP_CONDITION = True		
					break
				else:
					print('Continue the program')

	print('\n\n\n >>> RESULT <<<')

	print('ITERATION: ', i)
	print('INTERVAL: [{},{}]'.format(a, b))
	print('ROOT: ', ROOT)
	print('ERROR: ', ERROR)
	print

	# print(x_array)
	# print(y_array)
	print(error_array)

	# Visualization
	# plt.figure(figsize=(20, 10))
	"""
	https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.savefig.html
	https://matplotlib.org/3.3.2/gallery/lines_bars_and_markers/scatter_symbol.html#sphx-glr-gallery-lines-bars-and-markers-scatter-symbol-py
	https://matplotlib.org/2.1.1/api/_as_gen/matplotlib.pyplot.plot.html
	https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.legend.html
	https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
	https://matplotlib.org/gallery/recipes/transparent_legends.html
	"""

	x = np.linspace(-1,10,1000)
	y = [f(elem) for elem in x]
	# plt.figure(figsize=(12, 10))

	# fontP = FontProperties()
	# fontP.set_size('xx-small')

	# x: ROOTs - calculted along the iterations
	plt.plot(iteration_array, x_array, label="Root=" + str(ROOT), color="black")
	plt.scatter(iteration_array, x_array, marker='.', color="black")
	plt.xlabel("Iterations")
	plt.title("Roots/f(x)/Error per iteration")
	plt.legend(loc='best', fancybox=True, framealpha=0.5)

	# f(x) - calculated along the iterations
	plt.plot(iteration_array, y_array, label='f(x)={}'.format(y_array[-1]), color="green")
	plt.scatter(iteration_array, y_array, marker='.', color="green")
	plt.legend(loc='best', fancybox=True, framealpha=0.5)

	# Error - calculated along the iterations
	print('-*-*-*-*-*-*-\nshape: ', iteration_array.shape)
	print(iteration_array[1:,], iteration_array[1:,].shape)
	print(error_array, error_array.shape)
	plt.plot(iteration_array[1:,], error_array, alpha=0.7, label='Error=' + str(ERROR), color="red")
	plt.scatter(iteration_array[1:,], error_array, marker='.', alpha=0.7, color="red")
	plt.legend(loc='best', fancybox=True, framealpha=0.5)
	# plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)



	plt.savefig(fname='ROOTs.png', dpi=140)
	# ---------------------
	plt.close()

	# plt.figure(figsize=(12, 10))
	# f(x)
	plt.plot(x, y, label="f(x)", color="green")
	plt.legend(loc='best')

	plt.scatter(x=ROOT, y=f(ROOT), label="Root=" + str(ROOT), color="black")
	plt.legend(loc='best', fancybox=True, framealpha=0.5)


	# plt.ylabel("Roots")
	plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)
	plt.savefig(fname='function.png', dpi=140)