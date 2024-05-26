import numpy as np
import matplotlib.pyplot as plt

# Lee el archivo .dat con pandas

energia = np.loadtxt("hamiltoniano.dat")

plt.plot(energia)

plt.xlabel('Iteración')
plt.ylabel('H´')
plt.title('Conservacion H´')

plt.show()




