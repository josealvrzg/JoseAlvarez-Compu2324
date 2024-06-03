import pandas as pd
import matplotlib.pyplot as plt

# Lee el archivo .dat con pandas

data = pd.read_csv('datos_salida.dat', delimiter='\s+')

data = pd.read_csv('energias.dat', delimiter='\s+')

# Accede a la columna 
energia = data['ETotal:']
epotencial = data['EPotencial:']
ecinetica = data['ECinetica:']
momento= data['Momento_Angular:']

#plt.plot(energia,label="Energía Total")
#plt.plot(epotencial, label="Energía Potencial")
#plt.plot(ecinetica,label="Energía Cinética")

plt.plot(momento)

plt.xlabel('Iteración')
plt.ylabel('Momento Angular')
plt.title('Momento Angular Sistema Solar')

plt.plot(energia,label="Energía Total")
plt.plot(epotencial, label="Energía Potencial")
plt.plot(ecinetica,label="Energía Cinética")

plt.xlabel('Iteración')
plt.ylabel('Energía')
plt.title('Energías Sistema Solar')


plt.legend()
plt.show()




