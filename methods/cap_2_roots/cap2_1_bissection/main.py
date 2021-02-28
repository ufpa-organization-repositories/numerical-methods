import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from modules import *

from abc import ABC, abstractmethod
from typing import List, Dict

class Method(IMethod):
	
	def __init__(self):
		super().__init__(params=['a', 'b', 'ERROR_THRESHOLD', 'N_MAX_ITERATIONS', 'N_FLOATING_POINTS'])
		self.a_b_array = np.array([])
		self.x_array = np.array([])
		self.y_array = np.array([])
		self.error_array = np.array([])
		self.iteration_array = np.array([])
		self.ROOT: float = None
		self.ERROR: float = None

	def run(self):

		# Parameters
		a = self.parameters['a']
		b = self.parameters['b']
		ERROR_THRESHOLD = self.parameters['ERROR_THRESHOLD']
		N_MAX_ITERATIONS = self.parameters['N_MAX_ITERATIONS']

		# Output: Receives the ROOT retrivied for the program
		ROOT = None
		ERROR = None

		# Iteration
		i = -1

		STOP_CONDITION = False

		while not STOP_CONDITION:
			i = i + 1
			self.log['log'].append(f'\n________________________\nITERATION: {i}')			
			self.iteration_array = np.append(self.iteration_array, [i])

			# STEP 1: Test the Theorem of Bolzano
			self.log['log'].append('# STEP 1: Test the Theorem of Bolzano')			
			# input("STEP 1: press t continue ...")
			BOLZANO = calc_Bolzano_Theorem(a=a, b=b)

			if BOLZANO:
				self.log['log'].append(f'a: {a}\tf(a): {calc_function(a)}')
				self.log['log'].append(f'b: {b}\tf(b): {calc_function(b)}')
				self.log['log'].append('BOLZANO: OK')

				# STEP 2: Calculate break point
				self.log['log'].append('# STEP 2: Calculate break point')
				# input("STEP 2: press t continue ...")

				break_point = calc_break_point(a=a, b=b)
				self.log['log'].append(f'break_point: {break_point}')
				
				# STEP 3: Reduce previous [a,b] interval
				# Choose between [a, x] or [x, b] by testing Theorem of Bolzano

				# if calc_Bolzano_Theorem(a, break_point):
				# 	a,b = a,break_point
				# 	# print(a, break_point)
				# else:
				# 	a,b = break_point,b
				# 	# print(break_point, b)

				self.x_array = np.append(self.x_array, [calc_truncate((a + b)/2, 4)])
				self.y_array = np.append(self.y_array, [calc_function(calc_truncate((a + b)/2, 4))])
				self.error_array = np.append(self.error_array, [calc_absolut_error(a=a, b=b)])

				# STEP 4: Check the conditions to stop the program
				# Do not check for the first iteration (i=0)

				if i > 0:
					error =  calc_absolut_error(a=a, b=b)
					self.log['log'].append('\nSUMMARY')
					self.log['log'].append('. . . . . .')
					self.log['log'].append(f'ITERATION: {i}')
					self.log['log'].append(f'INTERVAL: [{a},{b}]')
					self.log['log'].append(f'ROOT (breakpoint): {break_point}')
					self.log['log'].append(f'ERROR: {error}')
					self.log['log'].append('. . . . . .')			

					if (error < ERROR_THRESHOLD) or (i == N_MAX_ITERATIONS):
						
						self.log['log'].append('\nStop the program')
						self.log['log'].append(f'< ERROR_THRESHOLD={ERROR_THRESHOLD} REACHED == {error < ERROR_THRESHOLD}')
						self.log['log'].append('OR')
						self.log['log'].append(f'N_MAX_ITERATIONS={N_MAX_ITERATIONS} REACHED == {i == N_MAX_ITERATIONS}')						

						ROOT = calc_truncate((a + b)/2, 4)
						ERROR = error
						STOP_CONDITION = True		
						break
					else:
						self.log['log'].append('\nContinue the program')

				if calc_Bolzano_Theorem(a, break_point):
					a,b = a,break_point
					# print(a, break_point)
				else:
					a,b = break_point,b
					# print(break_point, b)
				self.log['log'].append(f'NEW INTERVAL:\n[a={a}, b={b}]')

			else:
				self.log['log'].append(f'There is no ROOT in [a,b]=[{a},{b}]')
				self.log['log'].append('>>> CHOOSE ANOTHER [a,b] INTERVAL <<<')
				break

		self.log['log'].append('\n\n\n >>> RESULT <<<')
		self.log['log'].append(f'ITERATION: {i}')
		self.log['log'].append('INTERVAL: [{},{}]'.format(a, b))
		self.log['log'].append(f'ROOT: {ROOT}')
		self.log['log'].append(f'ERROR: {ERROR}')

		# print(self.x_array)
		# print(self.y_array)
		# print(self.error_array)

		self.parameters['a'] = a
		self.parameters['b'] = b
		self.ROOT = ROOT
		self.ERROR = ERROR

	def export_graph(self):

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

		#################################################################################		
		
		distance: float = np.diff([self.parameters['a'], self.parameters['b']])[0]
		n_points = int(distance * 100)
		x = np.linspace(self.parameters['a'], self.parameters['b'], n_points)
		y = [calc_function(elem) for elem in x]
		# plt.figure(figsize=(12, 10))

		# fontP = FontProperties()
		# fontP.set_size('xx-small')

		# x: ROOTs - calculted along the iterations
		plt.scatter(self.iteration_array, self.x_array, marker='.', label="Root=" + str(self.ROOT), color="black")
		plt.xlabel("Iterations")
		plt.title("Roots/f(x)/Error per iteration")
		plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)

		# f(x) - calculated along the iterations
		plt.scatter(self.iteration_array, self.y_array, label='f(x)={}'.format(self.y_array[-1]), color="green")
		plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)

		# Error - calculated along the iterations
		plt.scatter(self.iteration_array, self.error_array, marker='s', alpha=0.7, label='Error=' + str(self.ERROR), color="red")
		plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)



		plt.savefig(fname='ROOTs.png', dpi=140)
		# ---------------------
		plt.close()

		# plt.figure(figsize=(12, 10))
		# f(x)
		plt.plot(x, y, label="f(x)", color="green")
		plt.legend(bbox_to_anchor=(1, 1), loc='best')

		plt.scatter(x=self.ROOT, y=calc_function(self.ROOT), label="Root=" + str(self.ROOT), color="black")
		plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)


		# plt.ylabel("Roots")
		plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)
		plt.savefig(fname='function.png', dpi=140)
		
		#################################################################################				

	
# # Entry of values
# a = calc_truncate(number=0)
# b = calc_truncate(number=1)

# # Output: Receives the ROOT retrivied for the program
# ROOT = None
# ERROR = None

# # Iteration
# i = -1
# a_b_array = np.array([])
# self.x_array = np.array([])
# self.y_array = np.array([])
# self.error_array = np.array([])
# self.iteration_array = np.array([])

# STOP_CONDITION = False

# while not STOP_CONDITION:
# 	i = i + 1
# 	print('\n________________________\nITERATION: ', i)
# 	self.iteration_array = np.append(self.iteration_array, [i])

# 	# STEP 1: Test the Theorem of Bolzano
# 	# input("STEP 1: press t continue ...")
# 	BOLZANO = calc_Bolzano_Theorem(a=a, b=b)

# 	if BOLZANO:
# 		print(f'a: {a}\tf(a): {calc_function(a)}')
# 		print(f'b: {b}\tf(b): {calc_function(b)}')		
# 		print('BOLZANO: OK')

# 		# STEP 2: Calculate break point
# 		# input("STEP 2: press t continue ...")

# 		break_point = calc_break_point(a=a, b=b)
# 		print('break_point: ', break_point)
		
# 		# STEP 3: Reduce previous [a,b] interval
# 		# Choose between [a, x] or [x, b] by testing Theorem of Bolzano

# 		# if calc_Bolzano_Theorem(a, break_point):
# 		# 	a,b = a,break_point
# 		# 	# print(a, break_point)
# 		# else:
# 		# 	a,b = break_point,b
# 		# 	# print(break_point, b)

# 		self.x_array = np.append(self.x_array, [calc_truncate((a + b)/2)])
# 		self.y_array = np.append(self.y_array, [calc_function(calc_truncate((a + b)/2))])
# 		self.error_array = np.append(self.error_array, [calc_absolut_error(a=a, b=b)])

# 		# STEP 4: Check the conditions to stop the program
# 		# Do not check for the first iteration (i=0)

# 		if i > 0:
# 			error =  calc_absolut_error(a=a, b=b)
# 			print('\nSUMMARY')
# 			print('. . . . . .')
# 			print('ITERATION: ', i)
# 			print('INTERVAL: [{},{}]'.format(str(a), str(b)))
# 			print(f'ROOT (breakpoint): ', break_point)
# 			print('ERROR: ', error)
# 			print('. . . . . .')			

# 			if (error < ERROR_THRESHOLD) or (i == N_MAX_ITERATIONS):
# 				print('\nStop the program')
# 				print(f'< ERROR_THRESHOLD={ERROR_THRESHOLD} REACHED == {error < ERROR_THRESHOLD}')
# 				print('OR')
# 				print(f'N_MAX_ITERATIONS={N_MAX_ITERATIONS} REACHED == {i == N_MAX_ITERATIONS}')
# 				ROOT = calc_truncate((a + b)/2)
# 				ERROR = error
# 				STOP_CONDITION = True		
# 				break
# 			else:
# 				print('\nContinue the program')

# 		if calc_Bolzano_Theorem(a, break_point):
# 			a,b = a,break_point
# 			# print(a, break_point)
# 		else:
# 			a,b = break_point,b
# 			# print(break_point, b)
# 		print(f'NEW INTERVAL:\n[a={a}, b={b}]')

# 	else:
# 		print('There is no ROOT in [a,b]=[{},{}]',format(str(a), str(b)))
# 		print('>>> CHOOSE ANOTHER [a,b] INTERVAL <<<')
# 		break

# print('\n\n\n >>> RESULT <<<')

# print('ITERATION: ', i)
# print('INTERVAL: [{},{}]'.format(a, b))
# print('ROOT: ', ROOT)
# print('ERROR: ', ERROR)

# print(self.x_array)
# print(self.y_array)
# print(self.error_array)

# # Visualization
# # plt.figure(figsize=(20, 10))
# """
# https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.savefig.html
# https://matplotlib.org/3.3.2/gallery/lines_bars_and_markers/scatter_symbol.html#sphx-glr-gallery-lines-bars-and-markers-scatter-symbol-py
# https://matplotlib.org/2.1.1/api/_as_gen/matplotlib.pyplot.plot.html
# https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.legend.html
# https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
# https://matplotlib.org/gallery/recipes/transparent_legends.html
# """

# x = np.linspace(-1,10,1000)
# y = [calc_function(elem) for elem in x]
# # plt.figure(figsize=(12, 10))

# # fontP = FontProperties()
# # fontP.set_size('xx-small')

# # x: ROOTs - calculted along the iterations
# plt.scatter(self.iteration_array, self.x_array, marker='.', label="Root=" + str(ROOT), color="black")
# plt.xlabel("Iterations")
# plt.title("Roots/f(x)/Error per iteration")
# plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)

# # f(x) - calculated along the iterations
# plt.scatter(self.iteration_array, self.y_array, label='f(x)={}'.format(self.y_array[-1]), color="green")
# plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)

# # Error - calculated along the iterations
# plt.scatter(self.iteration_array, self.error_array, marker='s', alpha=0.7, label='Error=' + str(ERROR), color="red")
# plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)



# plt.savefig(fname='ROOTs.png', dpi=140)
# # ---------------------
# plt.close()

# # plt.figure(figsize=(12, 10))
# # f(x)
# plt.plot(x, y, label="f(x)", color="green")
# plt.legend(bbox_to_anchor=(1, 1), loc='best')

# plt.scatter(x=ROOT, y=calc_function(ROOT), label="Root=" + str(ROOT), color="black")
# plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)


# # plt.ylabel("Roots")
# plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)
# plt.savefig(fname='function.png', dpi=140)
