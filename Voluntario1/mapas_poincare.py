import numpy as np
import matplotlib.pyplot as plt

# Leer los datos del archivo .dat
data1 = np.loadtxt('mapa_poincare_angulos1.dat', delimiter=',')
data3 = np.loadtxt('mapa_poincare_angulos3.dat', delimiter=',')
data5 = np.loadtxt('mapa_poincare_angulos5.dat', delimiter=',')
data10 = np.loadtxt('mapa_poincare_angulos10.dat', delimiter=',')
data15 = np.loadtxt('mapa_poincare_angulos15.dat', delimiter=',')

# Separar las columnas
x1 = data1[:, 0]
y1 = data1[:, 1]

x3 = data3[:, 0]
y3 = data3[:, 1]

x5 = data5[:, 0]
y5 = data5[:, 1]

x10 = data10[:, 0]
y10 = data10[:, 1]

x15 = data15[:, 0]
y15 = data15[:, 1]

# Crear la gráfica
plt.figure()
plt.plot(x1, y1, linewidth=1, label="E=1")
plt.plot(x3, y3, linewidth=1, label="E=3")
plt.plot(x5, y5, linewidth=1, label="E=5")
plt.plot(x10, y10, linewidth=1, label="E=10")
plt.plot(x15, y15, linewidth=1, label="E=15")


# Añadir títulos y etiquetas
plt.title(r'Mapa de Poincaré para los ángulos')
plt.xlabel(r'$\phi \, (\mathrm{rad})$', fontsize=14)
plt.ylabel(r'$\psi \, (\mathrm{rad})$', fontsize=14)

# Añadir la leyenda
plt.legend()

# Mostrar la gráfica
plt.grid()
plt.show()
