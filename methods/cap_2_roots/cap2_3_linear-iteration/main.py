import numpy as np
import matplotlib.pyplot as plt
from modules import *


ERROR_THRESHOLD = 0.01
N_MAX_ITERATIONS = 20


# Entrada de valores

# Passo 1: definir [a,b] a partir de análise visual
a = calc_truncate(0)
b = calc_truncate(1)

# Output: Receives the ROOT retrivied for the program
ROOT = None
ERROR = None

# Iteration
i = 0
n_iterations = 0

x_array = np.array([])
y_array = np.array([])
g_array = np.array([])
error_array = np.array([])
iteration_array = np.array([])

STOP_CONDITION = False

# STEP 1: Choose x0 (initial "chute")
x0 = calc_truncate(0.5)
print(f'\nx0={x0}')
print(f'g(x0)={g(x0)}')
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

if abs(g(x0)) < 1:
	print('\n__________________\nINITIAL CONDITION SATISFIED')
	print('f(x): e^(-x) -x')
	print('x0: ', x0)
	print('Making f(x) = 0 and x = G(x)')
	print('\tG(x): e^-x')
	print('\tG(x0): ', g(x0))
	print('\t>>> |G(x0)| < 1 OK <<<')

	x_array = np.append(x_array, np.array([x0]))
	y_array = np.append(y_array, np.array([f(x0)]))
	g_array = np.append(g_array, np.array([g(x0)]))
	error_array = np.append(error_array, np.array([calc_absolut_error(x1=x0, x2=g(x0))]))
	iteration_array = np.append(iteration_array, np.array([0]))

	ROOT = x0
	for k in range(1, N_MAX_ITERATIONS + 1):
		print('\n__________________\nITERATION: ', k)

		print('x: ', ROOT)
		print('f(x): ', f(ROOT))	
		print('G(x): ', g(ROOT))

		x1 = ROOT
		x2 = g(ROOT)

		print(f'\nx{k - 1}: ', x1)
		print(f'x{k}: ', x2)

		error = calc_absolut_error(x1, x2)
		print(f'|x{k} - x{k - 1}| = {error} < {ERROR_THRESHOLD}: {error < ERROR_THRESHOLD}')

		# print('ATUALIZA ROOT')
		ROOT = g(ROOT)
		print('ROOT: ', ROOT)

		x_array = np.append(x_array, np.array([ROOT]))
		y_array = np.append(y_array, np.array([f(ROOT)]))
		g_array = np.append(g_array, np.array([g(ROOT)]))
		error_array = np.append(error_array, np.array([error]))
		iteration_array = np.append(iteration_array, np.array([k]))

		# STEP 4: Check the Stop Condition
		if error < ERROR_THRESHOLD:
			print('Encontrou a solução')
			print('ROOT: ', ROOT)
			print(f'f(x=ROOT): {f(ROOT)}')
			ERROR = error			
			break		

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
plt.plot(iteration_array, error_array, alpha=0.7, label='Error=' + str(ERROR), color="red")
plt.scatter(iteration_array, error_array, marker='.', alpha=0.7, color="red")
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