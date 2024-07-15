# ================================================================================
# ANIMACION PENDULO
#
# Genera una animación a partir de un fichero de datos con las posiciones
# de las masas en diferentes instantes de tiempo.
# 
# El fichero debe estructurarse de la siguiente forma:
# 
#   x1_1, y1_1
#   x2_1, y2_1
#    
#   x1_2, y1_2
#   x2_2, y2_2
#
#   x1_3, y1_3
#   x2_3, y2_3
#   
#   (...)
#
# donde xi_j es la componente x de la masa i-ésima en el instante de
# tiempo j-ésimo, e yi_j lo mismo en la componente y. El programa asume que
# el nº de masas es siempre el mismo.
# ¡OJO! Los datos están separados por comas.
# 
# Si solo se especifica un instante de tiempo, se genera una imagen en pdf
# en lugar de una animación
#
# Se puede configurar la animación cambiando el valor de las variables
# de la sección "Parámetros"
#
# ================================================================================

# Importa los módulos necesarios
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import numpy as np

# Parámetros
# ========================================
file_in1 = "posiciones_pendulo3.dat" # Nombre del primer fichero de datos
file_in2 = "posiciones_pendulo3_prime.dat" # Nombre del segundo fichero de datos
file_out = "pendulo_comparacion" # Nombre del fichero de salida (sin extensión)

# Límites de los ejes X e Y
x_min = -2.5
x_max = 2.5
y_min = -2.5
y_max = 2.5

interval = 1 # Tiempo entre fotogramas en milisegundos
show_trail = True # Muestra la "estela" de la mas
trail_width = 1 # Ancho de la estela
save_to_file = True # False: muestra la animación por pantalla,
                     # True: la guarda en un fichero
dpi = 150 # Calidad del vídeo de salida (dots per inch)

# Radio de la masa, en las mismas unidades que la posición
# Puede ser un número (el radio de las dos masas) o una lista con
# el radio de cada una
masas_radius = 0.02 
#masas_radius = [0.5, 0.7]

# Colores para cada masa del primer péndulo
masas_colors1 = ['green', 'red']

# Colores para cada masa del segundo péndulo
masas_colors2 = ['orange','blue']

# Lectura del fichero de datos
# ========================================
# Función para leer datos del fichero
def leer_datos(file_in):
    with open(file_in, "r") as f:
        data_str = f.read()
    frames_data = list()
    for frame_data_str in data_str.split("\n\n"):
        frame_data = list()
        for masas_pos_str in frame_data_str.split("\n"):
            masas_pos = np.fromstring(masas_pos_str, sep=",")
            if masas_pos.size > 0:
                frame_data.append(np.fromstring(masas_pos_str, sep=","))
        frames_data.append(frame_data)
    return frames_data

# Leer datos del primer y segundo péndulo
frames_data1 = leer_datos(file_in1)
frames_data2 = leer_datos(file_in2)

# El número de masas es el número de líneas en cada bloque
nmasas1 = len(frames_data1[0])
nmasas2 = len(frames_data2[0])

# Verifica que el número de colores coincida con el número de masas
if len(masas_colors1) != nmasas1:
    raise ValueError("El número de colores especificados no coincide con el número de masas del primer péndulo")
if len(masas_colors2) != nmasas2:
    raise ValueError("El número de colores especificados no coincide con el número de masas del segundo péndulo")

# Creación de la animación/gráfico
# ========================================
# Crea los objetos figure y axis
fig, ax = plt.subplots()

# Define el rango de los ejes
ax.axis("equal")  # Misma escala para ejes X e Y
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

# Si solo se ha dado un radio para todas las masas, conviértelo a una
# lista con todos los elementos iguales
if not hasattr(masas_radius, "__iter__"):
    masas_radius = masas_radius*np.ones(nmasas1)
# En caso contrario, comprueba que el nº de radios coincide con el
# nº de masas y devuelve error en caso contrario
else:
    if not nmasas1 == len(masas_radius):
        raise ValueError(
                "El número de radios especificados no coincide con el número "
                "de masas del primer péndulo")

# Representa el primer fotograma
# Pinta un punto en la posición de cada masa y guarda el objeto asociado
# al punto en una lista
masas_points1 = list()
masas_trails1 = list()
for masas_pos, radius, color in zip(frames_data1[0], masas_radius, masas_colors1):
    x, y = masas_pos
    masas_point = Circle((x, y), radius, color=color)
    ax.add_artist(masas_point)
    masas_points1.append(masas_point)

    # Inicializa las estelas (si especificado en los parámetros)
    if show_trail:
        masas_trail, = ax.plot(
                x, y, "-", linewidth=trail_width,
                color=color)
        masas_trails1.append(masas_trail)

# Representa el primer fotograma del segundo péndulo
masas_points2 = list()
masas_trails2 = list()
for masas_pos, radius, color in zip(frames_data2[0], masas_radius, masas_colors2):
    x, y = masas_pos
    masas_point = Circle((x, y), radius, color=color)
    ax.add_artist(masas_point)
    masas_points2.append(masas_point)

    # Inicializa las estelas (si especificado en los parámetros)
    if show_trail:
        masas_trail, = ax.plot(
                x, y, "-", linewidth=trail_width,
                color=color)
        masas_trails2.append(masas_trail)

# Inicializa las líneas
line_origin_to_first1, = ax.plot([], [], 'k-')
line_first_to_second1, = ax.plot([], [], 'k-')
line_origin_to_first2, = ax.plot([], [], 'k-')
line_first_to_second2, = ax.plot([], [], 'k-')

# Función que actualiza la posición de las masas y las líneas en la animación 
def update(j_frame, frames_data1, frames_data2, masas_points1, masas_trails1, masas_points2, masas_trails2, show_trail):
    # Actualiza la posición del correspondiente a cada masa del primer péndulo
    for j_masa, masas_pos in enumerate(frames_data1[j_frame]):
        x, y = masas_pos
        masas_points1[j_masa].center = (x, y)

        if show_trail:
            xs_old, ys_old = masas_trails1[j_masa].get_data()
            xs_new = np.append(xs_old, x)
            ys_new = np.append(ys_old, y)

            masas_trails1[j_masa].set_data(xs_new, ys_new)

    # Actualiza las líneas del primer péndulo
    line_origin_to_first1.set_data([0, frames_data1[j_frame][0][0]], [0, frames_data1[j_frame][0][1]])
    line_first_to_second1.set_data(
        [frames_data1[j_frame][0][0], frames_data1[j_frame][1][0]], 
        [frames_data1[j_frame][0][1], frames_data1[j_frame][1][1]]
    )

    # Actualiza la posición del correspondiente a cada masa del segundo péndulo
    for j_masa, masas_pos in enumerate(frames_data2[j_frame]):
        x, y = masas_pos
        masas_points2[j_masa].center = (x, y)

        if show_trail:
            xs_old, ys_old = masas_trails2[j_masa].get_data()
            xs_new = np.append(xs_old, x)
            ys_new = np.append(ys_old, y)

            masas_trails2[j_masa].set_data(xs_new, ys_new)

    # Actualiza las líneas del segundo péndulo
    line_origin_to_first2.set_data([0, frames_data2[j_frame][0][0]], [0, frames_data2[j_frame][0][1]])
    line_first_to_second2.set_data(
        [frames_data2[j_frame][0][0], frames_data2[j_frame][1][0]], 
        [frames_data2[j_frame][0][1], frames_data2[j_frame][1][1]]
    )

    return masas_points1 + masas_trails1 + [line_origin_to_first1, line_first_to_second1] + masas_points2 + masas_trails2 + [line_origin_to_first2, line_first_to_second2]

def init_anim():
    # Clear trails
    if show_trail:
        for j_masa in range(nmasas1):
            masas_trails1[j_masa].set_data(list(), list())
        for j_masa in range(nmasas2):
            masas_trails2[j_masa].set_data(list(), list())

    # Inicializa las líneas
    line_origin_to_first1.set_data([], [])
    line_first_to_second1.set_data([], [])
    line_origin_to_first2.set_data([], [])
    line_first_to_second2.set_data([], [])

    return masas_points1 + masas_trails1 + [line_origin_to_first1, line_first_to_second1] + masas_points2 + masas_trails2 + [line_origin_to_first2, line_first_to_second2]

# Calcula el nº de frames
nframes = min(len(frames_data1), len(frames_data2))

# Si hay más de un instante de tiempo, genera la animación
if nframes > 1:
    # Info sobre FuncAnimation: https://matplotlib.org/stable/api/animation_api.html
    animation = FuncAnimation(
            fig, update, init_func=init_anim,
            fargs=(frames_data1, frames_data2, masas_points1, masas_trails1, masas_points2, masas_trails2, show_trail),
            frames=nframes, blit=True, interval=interval)

    # Muestra por pantalla o guarda según parámetros
    if save_to_file:
        animation.save("{}.mp4".format(file_out), dpi=dpi)
    else:
        plt.show()
# En caso contrario, muestra o guarda una imagen
else:
    # Muestra por pantalla o guarda según parámetros
    if save_to_file:
        fig.savefig("{}.pdf".format(file_out))
    else:
        plt.show()
