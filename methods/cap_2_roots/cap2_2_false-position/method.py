import numpy as np
import matplotlib.pyplot as plt
from modules import *

from imethod import IMethod


class Method(IMethod):

	def __init__(self):
		super().__init__(params=['a', 'b', 'N_MAX_ITERATIONS', 'ERROR_THRESHOLD', 'N_FLOATING_POINTS'])
		self.a_b_array = np.array([])
		self.x_array = np.array([])
		self.y_array = np.array([])
		self.error_array = np.array([])
		self.iteration_array = np.array([])
		self.breakpoint_array = np.array([])
		self.ROOT: float = None
		self.ERROR: float = None

		self.N_FLOATING_POINTS: int = None		

	def run(self):		

		# Entrada de valores		
		ERROR_THRESHOLD = self.parameters['ERROR_THRESHOLD']
		N_MAX_ITERATIONS = self.parameters['N_MAX_ITERATIONS']

		# Passo 1: definir [a,b] a partir de análise visual
		a = self.parameters['a']
		b = self.parameters['b']

		# Output: Receives the ROOT retrivied for the program
		self.ROOT = None
		self.ERROR = None
		self.N_FLOATING_POINTS = int(self.parameters['N_FLOATING_POINTS'])

		# Iteration
		i = -1		

		STOP_CONDITION = False

		BOLZANO = self.calc_Bolzano_Theorem(a=a, b=b)
		if not BOLZANO:			
			self.log.append(f'There is no ROOT in [a,b]=[{a},{b}]')
			self.log.append('>>> CHOOSE ANOTHER [a,b] INTERVAL <<<')

		else:
			while not STOP_CONDITION:
				i = i + 1
				self.log.append(f'\n__________________________\nITERATION: {i}')
				self.iteration_array = np.append(self.iteration_array, [i])

				BOLZANO = self.calc_Bolzano_Theorem(a=a, b=b)

				if BOLZANO:
					# Passo 2.1: Calcular o ponto de quebra (interseção)
					break_point = self.calc_break_point(a, b)
					self.y_array = np.append(self.y_array, [self.f(break_point)])
					self.log.append(f'break_point: {break_point}')					
					self.breakpoint_array = np.append(self.breakpoint_array, break_point)


					# Passo 2.2: Calcular self.f(break_point)
					f_break_point = self.f(break_point)
					self.log.append(f'f_break_point: {f_break_point}')

				
				# Passo 3.1: Checar self.f(break_point) == 0, então break_point é a raiz
				# Caso raiz, parar  processo
				# Caso não for raiz, continuar o processo

				if f_break_point == 0:
					self.log.append('f_break_point == 0\nStop the program')
				else:
					self.log.append('f_break_point != 0\nContinue the program')

					# Passo 3.2: Checar o teorema de bolzano

					if self.calc_Bolzano_Theorem(a, break_point):
						self.log.append('Bolzano: OK\n[a, f_break_point]')						
						a, b = a, break_point				
					
					elif self.calc_Bolzano_Theorem(break_point, b):
						self.log.append('Bolzano: OK\n[f_break_point, b]')						
						a, b = break_point, b

					else:
						self.log.append('Bolzano: NOT OK\nTHERE IS NO ROOT IN THE INTERVAL')
						STOP_CONDITION = True
						break

					self.log.append(f'[a={a},b={b}]')

					# Passo 4: Check the conditions to stop the program
					# input("STEP 4: press t continue ...")
					# Do not check for the first iteration (i=0)

					self.x_array = np.append(self.x_array, [self.calc_truncate((a + b)/2)])			
					self.a_b_array = np.append(self.a_b_array, np.array([(a, b)]))			

					
					self.log.append(f'ITERATION: {i}')
					self.log.append('INTERVAL: [{},{}]'.format(str(a), str(b)))
					self.log.append(f'ROOT: {break_point}')

					if i > 0:

						self.log.append(f'current break_point: {self.breakpoint_array[-1]}')
						self.log.append(f'last break_point: {self.breakpoint_array[-2]}')
						error = self.calc_absolut_error(x0=self.breakpoint_array[-1], x1=self.breakpoint_array[-2])
						self.error_array = np.append(self.error_array, [error])

						self.log.append(f'ERROR: {error}')

						if error < ERROR_THRESHOLD or i == N_MAX_ITERATIONS:
							self.log.append('Stop the program')
							self.ROOT = self.breakpoint_array[-1]
							self.ERROR = error
							STOP_CONDITION = True		
							break
						else:
							self.log.append('Continue the program')

			self.log.append('\n\n\n >>> RESULT <<<')

			self.log.append(f'ITERATION: {i}')
			self.log.append('INTERVAL: [{},{}]'.format(a, b))
			self.log.append(f'ROOT: {self.ROOT}')
			self.log.append(f'ERROR: {self.ERROR}')

			# print(self.x_array)
			# print(self.y_array)
			# print(self.error_array)

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

		x = np.linspace(-1,10,1000)
		y = [self.f(elem) for elem in x]
		# plt.figure(figsize=(12, 10))

		# fontP = FontProperties()
		# fontP.set_size('xx-small')

		# x: ROOTs - calculted along the iterations
		plt.plot(self.iteration_array, self.x_array, label="Root=" + str(self.ROOT), color="black")
		plt.scatter(self.iteration_array, self.x_array, marker='.', color="black")
		plt.xlabel("Iterations")
		plt.title("Roots/f(x)/Error per iteration")
		plt.legend(loc='best', fancybox=True, framealpha=0.5)

		# f(x) - calculated along the iterations
		plt.plot(self.iteration_array, self.y_array, label='f(x)={}'.format(self.y_array[-1]), color="green")
		plt.scatter(self.iteration_array, self.y_array, marker='.', color="green")
		plt.legend(loc='best', fancybox=True, framealpha=0.5)

		# Error - calculated along the iterations
		print('-*-*-*-*-*-*-\nshape: ', self.iteration_array.shape)
		print(self.iteration_array[1:,], self.iteration_array[1:,].shape)
		print(self.error_array, self.error_array.shape)
		plt.plot(self.iteration_array[1:,], self.error_array, alpha=0.7, label='Error=' + str(self.ERROR), color="red")
		plt.scatter(self.iteration_array[1:,], self.error_array, marker='.', alpha=0.7, color="red")
		plt.legend(loc='best', fancybox=True, framealpha=0.5)
		# plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)


		plt.savefig(fname='ROOTs.png', dpi=140)
		# ---------------------
		plt.close()

		# plt.figure(figsize=(12, 10))
		# f(x)
		plt.plot(x, y, label="f(x)", color="green")
		plt.legend(loc='best')

		plt.scatter(x=self.ROOT, y=self.f(self.ROOT), label="Root=" + str(self.ROOT), color="black")
		plt.legend(loc='best', fancybox=True, framealpha=0.5)


		# plt.ylabel("Roots")
		plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)
		plt.savefig(fname='function.png', dpi=140)

	def calc_truncate(self, number: float) -> float:
		"""
		Truncate the number to the specified floating points
		"""
		
		string = str(number)
		if '.' in string:
			for index, elem in enumerate(string):
				if elem == '.':			
					return float(string[:index + 1 + self.N_FLOATING_POINTS])
		else:
			return float(number)

	def f(self, x:float) -> float:
		"""
		Define and calculate f(x) for a given x value
		"""
		
		return self.calc_truncate(np.exp(-x) - x)

	def calc_Bolzano_Theorem(self, a: float, b: float) -> bool:
		"""
		Verify the Bolzano Theorem from a given a and b values
		Return True if Bolzano Theorem is ok
		"""
		# Calculate f(a) and f(b)
		f_a = self.f(a)
		f_b = self.f(b)

		return f_a*f_b < 0

	def calc_break_point(self, a: float, b: float):
		a, f_a = self.calc_truncate(a), self.calc_truncate(self.f(a))
		b, f_b = self.calc_truncate(b), self.calc_truncate(self.f(b))

		# print(a, f_a)
		# print(b, f_b)

		return self.calc_truncate((a*self.f(b) - b*self.f(a)/(self.f(b) - self.f(a))))

	def calc_absolut_error(self, x1: float, x0: float) -> float:
		"""
		Calculate the absolute error
		"""		
		return abs(abs(x1) - abs(x0))