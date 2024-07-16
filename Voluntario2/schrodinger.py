import numpy as np
import time
import matplotlib.pyplot as plt
from numba import njit

# Registro del tiempo de inicio
inicio = time.time()

i = complex(0.0,1.0)                    ## Unidad imaginaria

## PARAMTEROS

N = 20000                            # Numero divisiones en el reticulo espacial
nciclos = N/10                       # Numero oscilaciones completas
lamb = 0.5                          # Altura potencial

T = 5000                            # Iteraciones temporales
h = 1                               # Precision espacial
x0 = N*h/4                          # Posicion inicial de la onda (media)
sigma = N*h/16                      # Desviacion del paquete gaussiano

m = 10^5                           # Numero de lanzamientos

##################

## VARIABLES

j = np.array(range(0,N))            # Reticulo espacial
alpha = np.zeros(N-1,dtype=complex) # alpha 
beta = np.zeros(N-1,dtype=complex)  # beta
gamma = np.zeros(N-1,dtype=complex) # gamma
ji = np.zeros(N,dtype=complex)      # ji
Vprim = np.zeros(N)                 # Potencial
Pd = np.zeros(T)                    # Probabilidad de encontrarlo a la derecha
mt = 0                              # Nº de veces que se detecta a la derecha
##################

## CALCULOS INICIALES

x=j*h
k0prim = 2*np.pi*nciclos/N
sprim = 1.0/(4.0*k0prim**2)

## Potencial
for k in range(N):
    if  2/5*N <= k <= 3/5*N:                            # Añade valores solo en el intervalo seleccionado
        Vprim[k] = lamb*k0prim**2


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

## Calculo probabilidad a la derecha (entre 3N/5 y N)

def probderecha(phi):

    Pd = np.sum(np.abs(phi[3*N//5:])**2)/np.sum(np.abs(phi)**2) # Dividido entre la norma para normalizar
    return Pd


##################

## Varios lanzamientos
lanz = 0

while lanz<m:

    ## CALCULOS INSTANTE INICIAL

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

    ## Calculo Pd(t)
    for t in range(T):
        Pd[t] = probderecha(phi)                            # Calcula Pd para un instante t
        phi = calculos(phi, beta, ji)                       # Actualiza la funcion de onda

    ## Calculo maximo de Pd(t)
    nd = np.argmax(Pd)                            # t que hace maximo Pd(t)               

    ##################

    ## CALCULOS INSTANTES POSTERIORES

    # Actualizacion del vector phi
    n = 0
    while n<=(nd):
            
        phi = calculos(phi,beta,ji)                     
        n+=1

    ## Calculo Pd(nd)
    Pd_nd = probderecha(phi)                           

    ## Proceso de medicion
    p = np.random.random()                                  # Número aleatorio uniforme entre 0 y 1

    if p < Pd_nd:                                           # Si Pd(nd) es mayor que el numero aleatorio
        mt += 1                                             # Se detecta la partícula

    lanz += 1
##################

## COEFICIENTE DE TRANSMISION
K = mt/m

plt.axvline(x=3*N//5, color='r', linestyle='--')
print(nd)

plt.plot(np.abs(phi)**2)
plt.show()

print(r"El coficiente de Transmisión K=", K ,r"para un valor de Pd(nd)=",Pd_nd)

print(r"El coficiente de Transmisión K=", K ,r"para un valor de N=",N, r"y un valor de $\lambda=$",lamb)

