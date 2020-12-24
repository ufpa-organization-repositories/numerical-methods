import numpy as np
import matplotlib.pyplot as plt
from modules import *


ERROR_THRESHOLD = 0.01
N_MAX_ITERATIONS = 20


# Entrada de valores

# Passo 1: definir [a,b] a partir de análise visual
# a = calc_truncate(0.5)
# b = calc_truncate(0.6)

# Output: Receives the ROOT retrivied for the program
ROOT = None
ERROR = None

# Iteration
i = 0
n_iterations = 0

x_array = np.array([])
y_array = np.array([])
g_array = np.array([])
d1_array = np.array([])
d2_array = np.array([])
error_array = np.array([])
iteration_array = np.array([])

STOP_CONDITION = False

# STEP 1: Choose x0 (initial "chute")
	
x0 = calc_truncate(0.5)
print(f'\nx0={x0}')
print(f'f(x0)={f(x0)}')
print(f'd2(x0)={d2(x0)}')


# Use the Iterative Scheme Xk+1 = Xk - f(Xk)/d1(xK)
"""
Start the iteration
"""

# 1.1 if f(x0)*d2(x0) > 0:
if f(x0)*d2(x0) > 0:
	print('\n__________________\nINITIAL CONDITION SATISFIED')
	print(f'f(x0)*d2(x0) = {f(x0)*d2(x0)} > 0')
	print('x0: ', x0)

	# STEP 2: Calculate f(x0) and f(x0)
	f_x0 = f(x0)
	d1_x0 = d1(x0)

	print(f'f(x0): {f_x0}')
	print(f'd1(x0): {d1_x0}')
	# print('ROOT: ', g(x0))


	# x_array = np.append(x_array, np.array([x0]))
	# y_array = np.append(y_array, np.array([f(x0)]))
	# g_array = np.append(g_array, np.array([g(x0)]))
	# d1_array = np.append(d1_array, np.array([d1(x0)]))
	# d2_array = np.append(d2_array, np.array([d2(x0)]))
	# error_array = np.append(error_array, np.array([calc_absolut_error(x0, g(x0))]))
	# iteration_array = np.append(iteration_array, np.array([0]))

	ROOT = x0
	for k in range(0, N_MAX_ITERATIONS + 1):
		print('\n__________________\nITERATION: ', k)

		print('x: ', ROOT)

		# STEP 2: Calculate f(xk) and d1(xK)				
		print(f'f(x{k}): ', f(ROOT))	
		print(f'd1(x{k}): ', d1(ROOT))


		# STEP 3: Calculate Xk+1 by Xk
		x1 = ROOT
		x2 = g(ROOT)

		print(f'\nx{k}: ', x1)
		print(f'x{k + 1}: ', x2)

		error = calc_absolut_error(x2, x1)
		print(f'|x{k+1} - x{k}| = {error} < {ERROR_THRESHOLD}: {error < ERROR_THRESHOLD}')

		# print('ATUALIZA ROOT')
		ROOT = g(ROOT)
		print('ROOT: ', ROOT)

		x_array = np.append(x_array, np.array([ROOT]))
		y_array = np.append(y_array, np.array([f(ROOT)]))
		g_array = np.append(g_array, np.array([g(ROOT)]))
		d1_array = np.append(d1_array, np.array([d1(ROOT)]))
		d2_array = np.append(d2_array, np.array([d2(ROOT)]))
		error_array = np.append(error_array, np.array([error]))
		iteration_array = np.append(iteration_array, np.array([k]))

		# STEP 4: Check the Stop Condition
		if error < ERROR_THRESHOLD:
			print('Encontrou a solução')
			print('ROOT: ', ROOT)
			print(f'f(x=ROOT)={f(ROOT)}')
			ERROR = error			
			break		

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
plt.plot(iteration_array, error_array, alpha=0.7, label='Error=' + str(ERROR), color="red")
plt.scatter(iteration_array, error_array, marker='.', alpha=0.7, color="red")
plt.legend(loc='best', fancybox=True, framealpha=0.5)
# plt.legend(bbox_to_anchor=(1, 1), loc='best', fancybox=True, framealpha=0.5)



plt.savefig(fname='ROOTs.png', dpi=100)
# ---------------------
plt.close()

# plt.figure(figsize=(12, 10))
# f(x)
x = np.linspace(-1,10,1000)
y = [f(elem) for elem in x]
plt.plot(x, y, label="f(x)", color="green")
plt.legend(loc='best')

plt.scatter(x=ROOT, y=f(ROOT), label="Root=" + str(ROOT), color="black")
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
plt.savefig(fname='function.png', dpi=100)
