import numpy as np
import matplotlib.pyplot as plt
from numba import njit

i = complex(0,1)                    ## Unidad imaginaria

## PARAMTEROS

N = 1000                            # Numero divisiones en el reticulo espacial
nciclos = 180                       # Numero oscilaciones completas
lamb = 0.5                         # Altura potencial
T = 5000                            # Iteraciones temporales
h = 1                               # Precision espacial
x0 = N*h/4                          # Posicion inicial de la onda (media)
sigma = N*h/16                      # Desviacion del paquete gaussiano

##################

## VARIABLES

j = np.array(range(0,N))            # Reticulo espacial
alpha = np.zeros(N-1,dtype=complex) # alpha 
beta = np.zeros(N-1,dtype=complex)  # beta
gamma = np.zeros(N-1,dtype=complex) # gamma
ji = np.zeros(N,dtype=complex)      # ji
Vprim = np.zeros(N)                 # Potencial
Norm = np.array(range(0,T))         # Norma de la funcion de onda

##################

## CALCULOS INICIALES

x=j*h
k0prim = 2*np.pi*nciclos/N
sprim = 1/(4*k0prim**2)

## Potencial
for k in range(N):
    if  2/5*N <= k <= 3/5*N:                            # Añade valores solo en el intervalo seleccionado
        Vprim[k] = lamb*k0prim**2

## Funcion de onda inicial
phi = np.array(np.exp(i*k0prim*j)*np.exp(-(j*h-x0)**2/(2*sigma**2)),
               dtype=complex)
phi[0]=phi[N-1]=0                                       # Condiciones de contorno

## alpha y gamma (solo llega hasta N-1 en j)
A0 = -2+2*i/sprim-Vprim
for k in range(N-2,0,-1):                               #range(inicio, final, paso) decreciente
    alpha[k-1] = -1/(A0[k]+alpha[k])
for k in range(N-1,0,-1):
    gamma[k-1] = 1/(A0[k-1]+alpha[k-1])


##################

## FUNCIONES

## Calculos iteraciones
@njit                                                   # Optimiza la funcion
def calculos(phi,beta,ji):

    for k in range(N-2,0,-1):                           # Calculo beta para un instante n                       
        beta[k-1] = gamma[k]*(4*i*phi[k]/sprim-beta[k])

    ji[0]=ji[N-1]=0                                     # Calculo ji para un instante n
    for k in range(N-2):
        ji[k+1] = alpha[k]*ji[k]+beta[k]

    phi = ji-phi                                        # Calculo phi para instante posterior

    return phi                                          # Devuelve el nuevo valor de phi 


## Escribir en el fichero
def escribir():
    Prob = abs(phi)**2                                  # Probabilidad (modulo cuadrado)
    datos = np.column_stack((x, Prob, Vprim))           # Agrupa los vectores en columnas de una matriz

    # Guardar cada fila de la matriz en el archivo
    for fila in datos:
        fila_str = ",\t".join(map(str, fila))           # Convierte la fila a una cadena separada por comas
        f.write(fila_str + "\n")                        # Escribe la fila en el archivo
    f.write("\n")                                       # Linea vacia despues de cada paso temporal

##################

## ESCRITURA EN ARCHIVO

with open("schrodinger_data.dat", "w") as f:            # Abre el archivo de escritura
    escribir()                                          # Escribe en el fichero el primer instante

    n=0
    ## Instantes posteriores
    while n<T:
        
        Norm[n] = sum(abs(phi)**2)                      # Calculo la norma de phi^2
        phi = calculos(phi,beta,ji)                     # Actualiza el vector phi
        escribir()                                      # Escribe en el fichero cada instante n

        n+=1
f.close()                                               # Cierra el fichero

##################

# Grafica conservacion de la norma
plt.plot(Norm)
plt.xlabel('Iteración')
plt.ylabel(r'Suma del Módulo cuadrado de $\phi$')
plt.title('Conservación de la Norma')
plt.show()