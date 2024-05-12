import random 
import numpy as np
from numba import njit

## PARAMETROS

N = 100                 # Dimension de la red
T = 0.1                 # Temperatura
Pasos = 1000           # Numero de pasos montecarlo

##################

## VARIABLES

s = np.zeros((N,N))     # Red de spines

##################

## CALCULOS INICIALES

## Valor inicial aleatorio
for i in range(N):
  for j in range(N):
    spin=int(random.choice(seq=(-1,1)))       #spin up o down
    s[i][j] = spin

##################

## FUNCIONES

## Pasos de Ising
@njit                                         # Optimiza la funcion
def ising(s):
  ising=0
  while ising<N*N :
    DE = 0

    n = random.randint(0, N - 1)              # Coordenadas aleatorias de la matriz
    m = random.randint(0, N - 1)

    mant = (m - 1) % N                        # Posicion anterior, ajustado para condiciones de contorno periódicas
    nant = (n - 1) % N  
    msig = (m + 1) % N                        # Y siguiente
    nsig = (n + 1) % N 

    DE = 2*s[n][m]*(s[nsig][m]+s[nant][m]+s[n][msig]+s[n][mant])    # Energia

    p = min(1,np.exp(-DE/T))                  # Probalidad de cambiar

    x = random.random()                       # Número aleatorio uniforme entre 0 y 1

    if x<p:                                   # Cambia el spin 
      s[n][m] = -s[n][m]  

    ising+=1

## Escribir en fichero
def escribir():
  for fila in s:                              # Escribir en el fichero de salida
    fila_str = ",\t ".join(map(str, fila))    # Convierte la fila a una cadena separada por comas 
    f.write(fila_str + "\n")                  # Escribe la fila en el archivo
  f.write("\n")                               # Linea vacia despues de cada paso de montecarlo

##################

## ESCRITURA EN ARCHIVO

with open("ising_data.dat", "w") as f:

  t=0
  ## Pasos de Montecarlo
  while t<Pasos:

    ising(s)                                  # Actualiza la matriz de spines (Pasos de Ising)
    escribir()                                # Escribe en el fichero cada instante t

    t+=1
f.close()

##################
