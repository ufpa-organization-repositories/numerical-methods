import numpy as np
import matplotlib.pyplot as plt
from imethod import IMethod


class Method(IMethod):
	def __init__(self):
		super().__init__(params=['x0', 'ERROR_THRESHOLD', 'N_MAX_ITERATIONS', 'N_FLOATING_POINTS'])
		self.ROOT: float = None
		self.ERROR: float = None
		self.x_array = np.array([])
		self.y_array = np.array([])
		self.g_array = np.array([])
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
		self.parameters['x0'] = self.calc_truncate(0.5)
		self.log.append(f"\nx0={self.parameters['x0']}")
		self.log.append(f"g(x0)={self.g(self.parameters['x0'])}")
		# STEP 2: Choose G(x) OK

		# 2.1 Define f(x) OK
		# 2.2 Isolate x in f(x) OK(manulally)
		# 2.3 For each form, check the Theorem
		# 	2.4 x = G(x) (one of the forms)
		# 	2.5 G(x) "contínua" em [a,b] AND 2.6 |G'(x)| < 1
		# 2.7 Choose G(x) like the function that satisfies the Theorem above


		# STEP 3: Use the Iterative Scheme Xk+1=  G(Xk)
		"""
		Start the iteration
		"""

		if abs(self.g(self.parameters['x0'])) < 1:
			self.log.append('\n__________________\nINITIAL CONDITION SATISFIED')
			self.log.append('f(x): e^(-x) -x')
			self.log.append(f"x0: {self.parameters['x0']}")
			self.log.append('Making f(x) = 0 and x = G(x)')
			self.log.append('\tG(x): e^-x')
			self.log.append(f"\tG(x0): {self.g(self.parameters['x0'])}")
			self.log.append('\t>>> |G(x0)| < 1 OK <<<')

			self.x_array = np.append(self.x_array, np.array([self.parameters['x0']]))
			self.y_array = np.append(self.y_array, np.array([self.f(self.parameters['x0'])]))
			self.g_array = np.append(self.g_array, np.array([self.g(self.parameters['x0'])]))
			self.error_array = np.append(self.error_array, np.array([self.calc_absolut_error(x1=self.parameters['x0'], x2=self.g(self.parameters['x0']))]))
			self.iteration_array = np.append(self.iteration_array, np.array([0]))

			self.ROOT = self.parameters['x0']
			for k in range(1, self.parameters['N_MAX_ITERATIONS'] + 1):
				self.log.append(f"\n__________________\nITERATION: {k}")

				self.log.append(f"x: {self.ROOT}")
				self.log.append(f"f(x): {self.f(self.ROOT)}")	
				self.log.append(f"G(x): {self.g(self.ROOT)}")

				x1 = self.ROOT
				x2 = self.g(self.ROOT)

				self.log.append(f"\nx{k - 1}: {x1}")
				self.log.append(f"x{k}: {x2}")

				error = self.calc_absolut_error(x1, x2)
				self.log.append(f"|x{k} - x{k - 1}| = {error} < {self.parameters['ERROR_THRESHOLD']}: {error < self.parameters['ERROR_THRESHOLD']}")

				# self.log.append('ATUALIZA ROOT')
				self.ROOT = self.g(self.ROOT)
				self.log.append(f"ROOT: {self.ROOT}")

				self.x_array = np.append(self.x_array, np.array([self.ROOT]))
				self.y_array = np.append(self.y_array, np.array([self.f(self.ROOT)]))
				self.g_array = np.append(self.g_array, np.array([self.g(self.ROOT)]))
				self.error_array = np.append(self.error_array, np.array([error]))
				self.iteration_array = np.append(self.iteration_array, np.array([k]))

				# STEP 4: Check the Stop Condition
				if error < self.parameters['ERROR_THRESHOLD']:
					self.log.append('Encontrou a solução')
					self.log.append(f"ROOT: {self.ROOT}")
					self.log.append(f"f(x=ROOT): {self.f(self.ROOT)}")
					self.ERROR = error			
					break

	def hook_export_graph(self):

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
		plt.plot(self.iteration_array, self.error_array, alpha=0.7, label='Error=' + str(self.ERROR), color="red")
		plt.scatter(self.iteration_array, self.error_array, marker='.', alpha=0.7, color="red")
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
					return float(string[:index + 1 + self.parameters['N_FLOATING_POINTS']])
		else:
			return float(number)

	def f(self, x:float) -> float:
		"""
		Define and calculate f(x) for a given x value
		"""
		
		return self.calc_truncate(np.exp(-x) - x)

	def g(self, x: float) -> float:
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
		return self.calc_truncate(np.exp(-x))
	
	def calc_absolut_error(self, x1: float, x2: float) -> float:
		"""
		Calculate the absolute error for the
		Linear Iteration Method

		x1 = Last Root
		x2 = Current Root

		Rememeber that in each iteration, ROOT = G(Last_ROOT)
		"""	
		return abs(x2 - x1)
