import numpy as np
from numba import njit
import matplotlib.pyplot as plt

## PARAMETROS

N = 60                 # Dimension de la red
T = 0.1                 # Temperatura
Pasos = 1000            # Numero de pasos montecarlo

##################

## VARIABLES

s = np.zeros((N,N))     # Red de spines
snew = np.zeros((N,N))  # Red de spines actualizada
M = np.array([])        # Vector de magnetizacion

##################

## CALCULOS INICIALES

## Valor inicial aleatorio
for i in range(N):
  for j in range(N):
    spin=int(np.random.choice([-1,1]))       #spin up o down
    s[i][j] = spin
s[0, :] = 1  # Primera fila fija con +1
s[N-1, :] = -1  # Última fila fija con -1

snew[:] = s  # Copiar la configuración actual

##################

## FUNCIONES
@njit
def calculo_energia(red):
  E=0
  for i in range(N):
    for j in range(N):
        iant = (i - 1) % N                        # Posicion anterior, ajustado para condiciones de contorno periódicas
        jant = (j - 1) % N  
        isig = (i + 1) % N                        # Y siguiente
        jsig = (j + 1) % N 

        E -= red[i][j]*(red[isig][j]+red[iant][j]+red[i][jsig]+red[i][jant])    # Energia 
        return E/2
    
    
## Pasos de Ising
@njit                            # Optimiza la funcion
def ising(s, snew, N, T):
  ising=0
  while ising<N*N :
    DE = 0
    n = np.random.randint(1, N-1 )            # Coordenadas aleatorias de la matriz
    m = np.random.randint(0, N )

    if n==1:                                  # No cuenta el vecino de arriba
        vecinos = [
            ((n + 1), m),      # Abajo
            (n, (m - 1) % N),      # Izquierda
            (n, (m + 1) % N)       # Derecha
        ]
          
    elif n==N-1:                              # No cuenta el vecino de abajo
        vecinos = [
            ((n - 1), m),          # Arriba
            (n, (m - 1) % N),      # Izquierda
            (n, (m + 1) % N)       # Derecha
        ]
    else:
        vecinos = [
            ((n - 1), m),          # Arriba
            ((n + 1), m),          # Abajo
            (n, (m - 1) % N),           # Izquierda
            (n, (m + 1) % N)       # Derecha
        ]
        
    # Seleccionar una posición vecina al azar
    vecino = vecinos[np.random.randint(0, len(vecinos))]
    
    i, j = vecino

    snew[n][m], snew[i][j]= s[i][j], s[n][m]    # Intercambiar los espines

    DE = calculo_energia(snew) - calculo_energia(s)

    p = min(1,np.exp(-DE/T))                  # Probalidad de cambiar

    x = np.random.random()                    # Número aleatorio uniforme entre 0 y 1

    if x<p:                                   # Cambia el spin 
      s[n, m], s[i, j] = snew[n, m], snew[i, j]  
      
    ising+=1

## Magnetizacion

def magnetizacion(s,N):
    M = 0
    for i in range(N):
        for j in range(N):
           M += s[i, j]
    return M

## Escribir en fichero
def escribir():
  for fila in s:                              # Escribir en el fichero de salida
    fila_str = ",\t ".join(map(str, fila))    # Convierte la fila a una cadena separada por comas 
    f.write(fila_str + "\n")                  # Escribe la fila en el archivo
  f.write("\n")                               # Linea vacia despues de cada paso de montecarlo

##################

## ESCRITURA EN ARCHIVO

ising(s, snew, N, T)                                  # Actualiza la matriz de spines (Pasos de Ising)

with open("ising_data.dat", "w") as f:

  t=0
  ## Pasos de Montecarlo
  while t<Pasos:

    ising(s, snew, N, T)                                  # Actualiza la matriz de spines (Pasos de Ising)
    escribir()                                # Escribe en el fichero cada instante t
    M = np.append(M,magnetizacion(s,N))
    t+=1
f.close()

##################
plt.plot(M)
plt.show()
