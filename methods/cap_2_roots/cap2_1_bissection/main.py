import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from modules import *

from abc import ABC, abstractmethod
from typing import List, Dict

ERROR_THRESHOLD = 0.01
N_MAX_ITERATIONS = 10

class IMethod(ABC):
	def execute(self):
		self.parameters: Dict = {}
		self.log: Dict = {'log': []}
		self.hook_show_information_method()
		self.get_parameters()
		self.run()
		self.export_graph()
		self.export_log()		
	
	def hook_show_information_method(self): pass

	@abstractmethod
	def get_parameters(self): pass

	@abstractmethod
	def run(self): pass

	@abstractmethod
	def run(self): pass


class Bissection(IMethod):

	def get_parameters(self) -> None:
		# Entry of values		
		self.parameters['a'] = calc_truncate(number=0)
		self.parameters['b'] = calc_truncate(number=1)

	def run(self):

		# Parameters
		a, b = self.parameters['a'], self.parameters['b']

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

		STOP_CONDITION = False

		while not STOP_CONDITION:
			i = i + 1
			self.log['log'].append(f'\n________________________\nITERATION: {i}')
			print('\n________________________\nITERATION: ', i)
			iteration_array = np.append(iteration_array, [i])

			# STEP 1: Test the Theorem of Bolzano
			self.log['log'].append('# STEP 1: Test the Theorem of Bolzano')			
			# input("STEP 1: press t continue ...")
			BOLZANO = calc_Bolzano_Theorem(a=a, b=b)

			if BOLZANO:
				self.log['log'].append(f'a: {a}\tf(a): {calc_function(a)}')
				self.log['log'].append(f'b: {b}\tf(b): {calc_function(b)}')
				self.log['log'].append('BOLZANO: OK')
				print(f'a: {a}\tf(a): {calc_function(a)}')
				print(f'b: {b}\tf(b): {calc_function(b)}')		
				print('BOLZANO: OK')

				# STEP 2: Calculate break point
				# input("STEP 2: press t continue ...")

				break_point = calc_break_point(a=a, b=b)
				self.log['log'].append(f'break_point: {break_point}')
				print('break_point: ', break_point)
				
				# STEP 3: Reduce previous [a,b] interval
				# Choose between [a, x] or [x, b] by testing Theorem of Bolzano

				# if calc_Bolzano_Theorem(a, break_point):
				# 	a,b = a,break_point
				# 	# print(a, break_point)
				# else:
				# 	a,b = break_point,b
				# 	# print(break_point, b)

				x_array = np.append(x_array, [calc_truncate((a + b)/2)])
				y_array = np.append(y_array, [calc_function(calc_truncate((a + b)/2))])
				error_array = np.append(error_array, [calc_absolut_error(a=a, b=b)])

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

					print('\nSUMMARY')
					print('. . . . . .')
					print(f'ITERATION: {i}')
					print(f'INTERVAL: [{a},{b}]')
					print(f'ROOT (breakpoint): {break_point}')
					print(f'ERROR: {error}')
					print('. . . . . .')			

					if (error < ERROR_THRESHOLD) or (i == N_MAX_ITERATIONS):
						
						self.log['log'].append('\nStop the program')
						self.log['log'].append(f'< ERROR_THRESHOLD={ERROR_THRESHOLD} REACHED == {error < ERROR_THRESHOLD}')
						self.log['log'].append('OR')
						self.log['log'].append(f'N_MAX_ITERATIONS={N_MAX_ITERATIONS} REACHED == {i == N_MAX_ITERATIONS}')						

						print('\nStop the program')
						print(f'< ERROR_THRESHOLD={ERROR_THRESHOLD} REACHED == {error < ERROR_THRESHOLD}')
						print('OR')
						print(f'N_MAX_ITERATIONS={N_MAX_ITERATIONS} REACHED == {i == N_MAX_ITERATIONS}')
						ROOT = calc_truncate((a + b)/2)
						ERROR = error
						STOP_CONDITION = True		
						break
					else:
						self.log['log'].append('\nContinue the program')
						print('\nContinue the program')

				if calc_Bolzano_Theorem(a, break_point):
					a,b = a,break_point
					# print(a, break_point)
				else:
					a,b = break_point,b
					# print(break_point, b)
				self.log['log'].append(f'NEW INTERVAL:\n[a={a}, b={b}]')
				print(f'NEW INTERVAL:\n[a={a}, b={b}]')

			else:
				self.log['log'].append(f'There is no ROOT in [a,b]=[{a},{b}]')
				self.log['log'].append('>>> CHOOSE ANOTHER [a,b] INTERVAL <<<')
				print('There is no ROOT in [a,b]=[{},{}]',format(str(a), str(b)))
				print('>>> CHOOSE ANOTHER [a,b] INTERVAL <<<')
				break

		self.log['log'].append('\n\n\n >>> RESULT <<<')
		self.log['log'].append(f'ITERATION: {i}')
		self.log['log'].append('INTERVAL: [{},{}]'.format(a, b))
		self.log['log'].append(f'ROOT: {ROOT}')
		self.log['log'].append(f'ERROR: {ERROR}')

		print('\n\n\n >>> RESULT <<<')

		print('ITERATION: ', i)
		print('INTERVAL: [{},{}]'.format(a, b))
		print('ROOT: ', ROOT)
		print('ERROR: ', ERROR)

		# print(x_array)
		# print(y_array)
		# print(error_array)

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
		"""
		x = np.linspace(-1,10,1000)
		y = [calc_function(elem) for elem in x]
		# plt.figure(figsize=(12, 10))

		# fontP = FontProperties()
		# fontP.set_size('xx-small')

		# x: ROOTs - calculted along the iterations
		plt.scatter(iteration_array, x_array, marker='.', label="Root=" + str(ROOT), color="black")
		plt.xlabel("Iterations")
		plt.title("Roots/f(x)/Error per iteration")
		plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)

		# f(x) - calculated along the iterations
		plt.scatter(iteration_array, y_array, label='f(x)={}'.format(y_array[-1]), color="green")
		plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)

		# Error - calculated along the iterations
		plt.scatter(iteration_array, error_array, marker='s', alpha=0.7, label='Error=' + str(ERROR), color="red")
		plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)



		plt.savefig(fname='ROOTs.png', dpi=140)
		# ---------------------
		plt.close()

		# plt.figure(figsize=(12, 10))
		# f(x)
		plt.plot(x, y, label="f(x)", color="green")
		plt.legend(bbox_to_anchor=(1, 1), loc='best')

		plt.scatter(x=ROOT, y=calc_function(ROOT), label="Root=" + str(ROOT), color="black")
		plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)


		# plt.ylabel("Roots")
		plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)
		plt.savefig(fname='function.png', dpi=140)
		"""
		#################################################################################	
	def export_log(self):
		with open('log.txt', 'w') as f:
			for line in self.log['log']:
				f.write(line + '\n')
		# return self.log['log']

method = Bissection()
method.execute()
	
# # Entry of values
# a = calc_truncate(number=0)
# b = calc_truncate(number=1)

# # Output: Receives the ROOT retrivied for the program
# ROOT = None
# ERROR = None

# # Iteration
# i = -1
# a_b_array = np.array([])
# x_array = np.array([])
# y_array = np.array([])
# error_array = np.array([])
# iteration_array = np.array([])

# STOP_CONDITION = False

# while not STOP_CONDITION:
# 	i = i + 1
# 	print('\n________________________\nITERATION: ', i)
# 	iteration_array = np.append(iteration_array, [i])

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

# 		x_array = np.append(x_array, [calc_truncate((a + b)/2)])
# 		y_array = np.append(y_array, [calc_function(calc_truncate((a + b)/2))])
# 		error_array = np.append(error_array, [calc_absolut_error(a=a, b=b)])

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

# print(x_array)
# print(y_array)
# print(error_array)

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
# plt.scatter(iteration_array, x_array, marker='.', label="Root=" + str(ROOT), color="black")
# plt.xlabel("Iterations")
# plt.title("Roots/f(x)/Error per iteration")
# plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)

# # f(x) - calculated along the iterations
# plt.scatter(iteration_array, y_array, label='f(x)={}'.format(y_array[-1]), color="green")
# plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)

# # Error - calculated along the iterations
# plt.scatter(iteration_array, error_array, marker='s', alpha=0.7, label='Error=' + str(ERROR), color="red")
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
