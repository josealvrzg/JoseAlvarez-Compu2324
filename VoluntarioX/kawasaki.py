import numpy as np
from numba import njit
import matplotlib.pyplot as plt

## PARAMETROS

N = 32                # Dimension de la red
T = 1.3                # Temperatura
Pasos = 1000000            # Numero de pasos montecarlo

##################

## VARIABLES

s = np.zeros((N,N))     # Red de spines
snew = np.zeros((N,N))  # Red de spines actualizada
M  = np.array([])       # Magneticacion en funcion del tiempo
Mup = np.array([])      # Vector de magnetizacion arriba
Mdown = np.array([])    # Vector de magnetizacion abajo


##################

## CALCULOS INICIALES

s[0, :] = -1  # Primera fila fija con -1
s[N-1, :] = 1  # Última fila fija con +1

# Aseguramos una magnetizacion nula
vector = np.concatenate((np.ones(N*(N-2) // 2), np.full(N*(N-2) // 2, -1))) # Vector con mitad de 1 y mitad de -1
np.random.shuffle(vector) # Valor inicial aleatorio

s_intermedia_mezclada = vector.reshape((N-2, N))  # Matriz con mitad de 1 y mitad de -1

s[1:(N-1), :] = s_intermedia_mezclada # Resto de filas aleatorias 

snew[:] = s  # Copiar la configuración actual

##################

## FUNCIONES

## Energia
@njit
def calculo_energia(red):
  E=0.0
  for i in range(N):
    for j in range(N):
      iant = (i - 1) % N                        # Posicion anterior, ajustado para condiciones de contorno periódicas
      jant = (j - 1) % N  
      isig = (i + 1) % N                        # Y siguiente
      jsig = (j + 1) % N 

      E += red[i][j]*(red[isig][j]+red[iant][j]+red[i][jsig]+red[i][jant])    # Energia 
      return -E/2
    
    
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
        ((n + 1), m),          # Abajo
        (n, (m - 1) % N),      # Izquierda
        (n, (m + 1) % N)       # Derecha
        ]
          
    elif n==N-2:                              # No cuenta el vecino de abajo
      vecinos = [
        ((n - 1), m),          # Arriba
        (n, (m - 1) % N),      # Izquierda
        (n, (m + 1) % N)       # Derecha
        ]
    else:
      vecinos = [
        ((n - 1), m),          # Arriba
        ((n + 1), m),          # Abajo
        (n, (m - 1) % N),      # Izquierda
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

def magnetizacion(s):
  M = 0
  M = np.sum(s)/(N^2)
  return M

## Escribir en fichero
def escribir():
  for fila in s:                              # Escribir en el fichero de salida
    fila_str = ",\t ".join(map(str, fila))    # Convierte la fila a una cadena separada por comas 
    f.write(fila_str + "\n")                  # Escribe la fila en el archivo
  f.write("\n")                               # Linea vacia despues de cada paso de montecarlo

##################

## ESCRITURA EN ARCHIVO

with open("kawasaki_data.dat", "w") as f:

  t=0
  ## Pasos de Montecarlo
  while t<Pasos:

    ising(s, snew, N, T)                                  # Actualiza la matriz de spines (Pasos de Ising)
    escribir()                                # Escribe en el fichero cada instante t
    M = np.append(M,magnetizacion(s))
    Mup = np.append(Mup,magnetizacion(s[:N//2]))
    Mdown = np.append(Mdown,magnetizacion(s[N//2+1:]))
    t+=1
f.close()


##################
plt.plot(M, label = "Magnetización Total")
plt.plot(Mup, label = "Magnetización Arriba")
plt.plot(Mdown, label = "Magnetización Abajo")
plt.legend()
plt.show()

