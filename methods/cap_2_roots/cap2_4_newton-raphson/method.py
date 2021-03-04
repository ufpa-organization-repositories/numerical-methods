import numpy as np
import matplotlib.pyplot as plt
from modules import *
from imethod import IMethod

ERROR_THRESHOLD = 0.01
N_MAX_ITERATIONS = 20


class Method(IMethod):
	def __init__(self):
		super().__init__(params=['x0', 'ERROR_THRESHOLD', 'N_MAX_ITERATIONS', 'N_FLOATING_POINTS'])
		self.ROOT: float = None
		self.ERROR: float = None
		self.x_array = np.array([])
		self.y_array = np.array([])
		self.g_array = np.array([])
		self.d1_array = np.array([])
		self.d2_array = np.array([])
		self.error_array = np.array([])
		self.iteration_array = np.array([])

	def run(self):
		self.parameters['x0'] = float(self.parameters['x0'])
		self.parameters['ERROR_THRESHOLD'] = float(self.parameters['ERROR_THRESHOLD'])
		self.parameters['N_MAX_ITERATIONS'] = int(self.parameters['N_MAX_ITERATIONS'])
		self.parameters['N_FLOATING_POINTS'] = int(self.parameters['N_FLOATING_POINTS'])

		# Iteration
		i = 0
		n_iterations = 0

		STOP_CONDITION = False

		# STEP 1: Choose x0 (initial "chute")
			
		self.log.append(f"\nx0={self.parameters['x0']}")
		self.log.append(f"f(x0)={self.f(self.parameters['x0'])}")
		self.log.append(f"d2(x0)={self.d2(self.parameters['x0'])}")


		# Use the Iterative Scheme Xk+1 = Xk - f(Xk)/d1(xK)
		"""
		Start the iteration
		"""

		# 1.1 if f(x0)*d2(x0) > 0:
		if self.f(self.parameters['x0'])*self.d2(self.parameters['x0']) > 0:
			self.log.append('\n__________________\nINITIAL CONDITION SATISFIED')
			self.log.append(f"f(x0)*d2(x0) = {self.f(self.parameters['x0'])*self.d2(self.parameters['x0'])} > 0")
			self.log.append(f"x0: {self.parameters['x0']}")

			# STEP 2: Calculate f(x0) and f(x0)
			f_x0 = self.f(self.parameters['x0'])
			d1_x0 = self.d1(self.parameters['x0'])

			self.log.append(f"f(x0): {f_x0}")
			self.log.append(f"d1(x0): {d1_x0}")
			# self.log.append('ROOT: ', g(x0))


			# x_array = np.append(x_array, np.array([x0]))
			# y_array = np.append(y_array, np.array([f(x0)]))
			# g_array = np.append(g_array, np.array([g(x0)]))
			# d1_array = np.append(d1_array, np.array([d1(x0)]))
			# d2_array = np.append(d2_array, np.array([d2(x0)]))
			# error_array = np.append(error_array, np.array([calc_absolut_error(x0, g(x0))]))
			# iteration_array = np.append(iteration_array, np.array([0]))

			self.ROOT = self.parameters['x0']
			for k in range(0, self.parameters['N_MAX_ITERATIONS'] + 1):
				self.log.append(f"\n__________________\nITERATION: {k}")

				self.log.append(f"x: {self.ROOT}")

				# STEP 2: Calculate f(xk) and d1(xK)				
				self.log.append(f"f(x{k}): {self.f(self.ROOT)}")	
				self.log.append(f"d1(x{k}): {self.d1(self.ROOT)}")


				# STEP 3: Calculate Xk+1 by Xk
				x1 = self.ROOT
				x2 = self.g(self.ROOT)

				self.log.append(f'\nx{k}: {x1}')
				self.log.append(f'x{k + 1}: {x2}')

				error = self.calc_absolut_error(x2, x1)
				self.log.append(f"|x{k+1} - x{k}| = {error} < {self.parameters['ERROR_THRESHOLD']}: {error < self.parameters['ERROR_THRESHOLD']}")

				# self.log.append('ATUALIZA ROOT')
				self.ROOT = self.g(self.ROOT)
				self.log.append(f'ROOT: {self.ROOT}')

				self.x_array = np.append(self.x_array, np.array([self.ROOT]))
				self.y_array = np.append(self.y_array, np.array([self.f(self.ROOT)]))
				self.g_array = np.append(self.g_array, np.array([self.g(self.ROOT)]))
				self.d1_array = np.append(self.d1_array, np.array([self.d1(self.ROOT)]))
				self.d2_array = np.append(self.d2_array, np.array([self.d2(self.ROOT)]))
				self.error_array = np.append(self.error_array, np.array([error]))
				self.iteration_array = np.append(self.iteration_array, np.array([k]))

				# STEP 4: Check the Stop Condition
				if error < self.parameters['ERROR_THRESHOLD']:
					self.log.append('Encontrou a solução')
					self.log.append(f"ROOT: {self.ROOT}")
					self.log.append(f'f(x=ROOT)={self.f(self.ROOT)}')
					self.ERROR = error			
					break		

	def export_graph(self):
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
		plt.scatter(iteration_array, y_array, marker='.', color="green")
		plt.legend(loc='best', fancybox=True, framealpha=0.5)

		# Error - calculated along the iterations
		plt.plot(self.iteration_array, self.error_array, alpha=0.7, label='Error=' + str(self.ERROR), color="red")
		plt.scatter(self.iteration_array, self.error_array, marker='.', alpha=0.7, color="red")
		plt.legend(loc='best', fancybox=True, framealpha=0.5)
		# plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)



		plt.savefig(fname='ROOTs.png', dpi=140)
		# ---------------------
		plt.close()

		# plt.figure(figsize=(12, 10))
		# f(x)
		x = np.linspace(-1,10,1000)
		y = [f(elem) for elem in x]
		plt.plot(x, y, label="f(x)", color="green")
		plt.legend(loc='best')

		plt.scatter(x=self.ROOT, y=self.f(self.ROOT), label="Root=" + str(self.ROOT), color="black")
		plt.legend(loc='best', fancybox=True, framealpha=0.5)

		# f'(x)
		x = np.linspace(-1,6,600)
		y = [d1(elem) for elem in x]
		plt.plot(x, y, label="f⁽¹⁾(x)", color="blue")
		plt.legend(loc='best')


		# f''(x)
		x = np.linspace(-1,6,600)
		y = [d2(elem) for elem in x]
		plt.plot(x, y, label="f⁽²⁾(x)", color="purple")
		plt.legend(loc='best')

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
					return float(string[:index + 1 + self.parameters['N_FLOATING_POINTS']])
		else:
			return float(number)

	def f(self, x:float) -> float:
		"""
		Define and calculate f(x) for a given x value
		"""
		
		return self.calc_truncate(np.exp(-x) - x)

	def d1(self, x: float) -> float:
		"""
		Define and calculate d1 for a given x value
		d1 is the First Order Derivate in realation to x
		"""

		# Return the d1(x)=e^(-x) for a given x
		return self.calc_truncate((-np.exp(-x)) -1)

	def d2(self, x: float) -> float:
		"""
		Define and calculate d2 for a given x value
		d1 is the First Order Derivate in realation to x
		"""

		# Return the d2(x)=-e^(-x) for a given x
		return self.calc_truncate(np.exp(-x))

	def g(self, x: float) -> float:
		"""
		Calculate the aproximation
		Xk+1 = G(x) is a aproximation for the next iteration
		"""

		# Return the aproximation G(x)= x - f(x)/d1(x)
		return self.calc_truncate(x - (self.f(x)/self.d1(x)))

	def calc_absolut_error(self, x1: float, x2: float) -> float:
		"""
		Calculate the absolute error for the
		Linear Iteration Method

		x1 = Last Root
		x2 = Current Root

		Rememeber that in each iteration, ROOT = G(Last_ROOT)
		"""	
		return abs(x2 - x1)
