# method modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
# from modules import * # modules module is imported from app

from abc import ABC, abstractmethod
from typing import List, Dict

# dependency modules
from imethod import IMethod # imethod module is imported from app (at global level app works)


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
		self.N_FLOATING_POINTS: int = None

	def run(self):

		# Parameters
		a = self.parameters['a']
		b = self.parameters['b']
		ERROR_THRESHOLD = self.parameters['ERROR_THRESHOLD']
		N_MAX_ITERATIONS = self.parameters['N_MAX_ITERATIONS']
		self.N_FLOATING_POINTS = int(self.parameters['N_FLOATING_POINTS'])

		# Output: Receives the ROOT retrivied for the program
		ROOT = None
		ERROR = None

		# Iteration
		i = -1

		STOP_CONDITION = False

		while not STOP_CONDITION:
			i = i + 1
			self.log.append(f'\n________________________\nITERATION: {i}')			
			self.iteration_array = np.append(self.iteration_array, [i])

			# STEP 1: Test the Theorem of Bolzano
			self.log.append('# STEP 1: Test the Theorem of Bolzano')			
			# input("STEP 1: press t continue ...")
			BOLZANO = self.calc_Bolzano_Theorem(a=a, b=b)

			if BOLZANO:
				self.log.append(f'a: {a}\tf(a): {self.calc_function(a)}')
				self.log.append(f'b: {b}\tf(b): {self.calc_function(b)}')
				self.log.append('BOLZANO: OK')

				# STEP 2: Calculate break point
				self.log.append('# STEP 2: Calculate break point')
				# input("STEP 2: press t continue ...")

				break_point = self.calc_break_point(a=a, b=b)
				self.log.append(f'break_point: {break_point}')
				
				# STEP 3: Reduce previous [a,b] interval
				# Choose between [a, x] or [x, b] by testing Theorem of Bolzano

				# if self.calc_Bolzano_Theorem(a, break_point):
				# 	a,b = a,break_point
				# 	# print(a, break_point)
				# else:
				# 	a,b = break_point,b
				# 	# print(break_point, b)

				self.x_array = np.append(self.x_array, [self.calc_truncate((a + b)/2, self.N_FLOATING_POINTS)])
				self.y_array = np.append(self.y_array, [self.calc_function(self.calc_truncate((a + b)/2, self.N_FLOATING_POINTS))])
				self.error_array = np.append(self.error_array, [self.calc_absolut_error(a=a, b=b)])

				# STEP 4: Check the conditions to stop the program
				# Do not check for the first iteration (i=0)

				if i > 0:
					error =  self.calc_absolut_error(a=a, b=b)
					self.log.append('\nSUMMARY')
					self.log.append('. . . . . .')
					self.log.append(f'ITERATION: {i}')
					self.log.append(f'INTERVAL: [{a},{b}]')
					self.log.append(f'ROOT (breakpoint): {break_point}')
					self.log.append(f'ERROR: {error}')
					self.log.append('. . . . . .')			

					if (error < ERROR_THRESHOLD) or (i == N_MAX_ITERATIONS):
						
						self.log.append('\nStop the program')
						self.log.append(f'< ERROR_THRESHOLD={ERROR_THRESHOLD} REACHED == {error < ERROR_THRESHOLD}')
						self.log.append('OR')
						self.log.append(f'N_MAX_ITERATIONS={N_MAX_ITERATIONS} REACHED == {i == N_MAX_ITERATIONS}')						

						ROOT = self.calc_truncate((a + b)/2, self.N_FLOATING_POINTS)
						ERROR = error
						STOP_CONDITION = True		
						break
					else:
						self.log.append('\nContinue the program')

				if self.calc_Bolzano_Theorem(a, break_point):
					a,b = a,break_point
					# print(a, break_point)
				else:
					a,b = break_point,b
					# print(break_point, b)
				self.log.append(f'NEW INTERVAL:\n[a={a}, b={b}]')

			else:
				self.log.append(f'There is no ROOT in [a,b]=[{a},{b}]')
				self.log.append('>>> CHOOSE ANOTHER [a,b] INTERVAL <<<')
				break

		self.log.append('\n\n\n >>> RESULT <<<')
		self.log.append(f'ITERATION: {i}')
		self.log.append('INTERVAL: [{},{}]'.format(a, b))
		self.log.append(f'ROOT: {ROOT}')
		self.log.append(f'ERROR: {ERROR}')

		# print(self.x_array)
		# print(self.y_array)
		# print(self.error_array)

		self.parameters['a'] = a
		self.parameters['b'] = b
		self.ROOT = ROOT
		self.ERROR = ERROR

	def hook_export_graph(self):

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
		y = [self.calc_function(elem) for elem in x]
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

		plt.scatter(x=self.ROOT, y=self.calc_function(self.ROOT), label="Root=" + str(self.ROOT), color="black")
		plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)


		# plt.ylabel("Roots")
		plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)
		plt.savefig(fname='function.png', dpi=140)
		
		#################################################################################				

	def calc_truncate(self, number: float, N_FLOATING_POINTS: int) -> float:
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

	def calc_function(self, x:float) -> float:
		"""
		Define and calculate f(x) for a given x value
		"""
		
		return self.calc_truncate(np.exp(-x) - x, self.N_FLOATING_POINTS)

	def calc_Bolzano_Theorem(self, a: float, b: float) -> bool:
		"""
		Verify the Bolzano Theorem from a given a and b values
		Return True if Bolzano Theorem is ok
		"""
		# Calculate f(a) and f(b)
		f_a = self.calc_function(a)
		f_b = self.calc_function(b)

		return f_a*f_b < 0

	def calc_break_point(self, a: float, b: float) -> float:
		"""
		Calculate the brak point
		It is important that a and b had already been truncated
		"""
		# a_trunc = self.calc_truncate(a)
		# b_trunc = self.calc_truncate(b)
		return self.calc_truncate((a + b)/2, self.N_FLOATING_POINTS)

	def calc_absolut_error(self, a: float, b: float) -> float:
		"""
		Calculate the absolute error
		"""
		# Calculate f(a) and f(b)
		f_a = self.calc_function(a)
		f_b = self.calc_function(b)
		return self.calc_truncate(f_a - f_b, self.N_FLOATING_POINTS)
