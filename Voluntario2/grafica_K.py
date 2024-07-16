import matplotlib.pyplot as plt
import numpy as np

N = np.array([500,1000,2000,5000,10000,20000])
nciclos = N/10
KN = np.array([0.467,0.467,0.733,0.133,0.933,0.968])

lam_value = np.array([0.1, 0.3, 0.5, 1.0, 5.0, 10.0])
Klam = np.array([1, 0.333, 0.467, 0.067, 0, 0])

#K teórica
def Kteor(lam, nciclos):
    if lam < 1:
        return 4*(1-lam)/(4 * (1 - lam) + lam ** 2 * np.sin(2 * np.pi * nciclos * np.sqrt(1 - lam) / 5) ** 2)
    elif lam > 1:
        return 4*(lam-1)/(4 * (lam - 1) + lam ** 2 * np.sin(2 * np.pi * nciclos * np.sqrt(lam - 1) / 5) ** 2)
    else:
        return np.nan 
    
# Parámetros
nciclos = 10000
lambda_values = np.linspace(0.1, 10.0, 400)
K_values = []

for lam in lambda_values:
    try:
        K_values.append(Kteor(lam, nciclos))
    except ValueError as e:
        print(e)

# Graficar
plt.plot(lambda_values, K_values, label=r"K($\lambda$) teórica", color='blue')
plt.plot(lam_value, Klam, label=r'K($\lambda$) simulado', color='red')
plt.title('Coeficiente de transmisión K(λ), con N=1000')
plt.xlabel('λ')
plt.ylabel('K(λ)')
plt.legend()
plt.grid(True)
plt.show()




#plt.plot(N,K,label="K(N) simulado")

