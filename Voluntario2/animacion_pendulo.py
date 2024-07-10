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
file_in = "posiciones_pendulo.dat" # Nombre del fichero de datos
file_out = "pendulo_animacion" # Nombre del fichero de salida (sin extensión)

# Límites de los ejes X e Y
x_min = -2.0
x_max = 2.0
y_min = -2.1
y_max = 0.5

interval = 10 # Tiempo entre fotogramas en milisegundos
show_trail = True # Muestra la "estela" de la mas
trail_width = 1 # Ancho de la estela
save_to_file = False # False: muestra la animación por pantalla,
                     # True: la guarda en un fichero
dpi = 150 # Calidad del vídeo de salida (dots per inch)

# Radio de la masa, en las mismas unidades que la posición
# Puede ser un número (el radio de las dos masas) o una lista con
# el radio de cada una
masas_radius = 0.02 
#masas_radius = [0.5, 0.7]

# Colores para cada masa
masas_colors = ['green', 'red']

# Lectura del fichero de datos
# ========================================
# Lee el fichero a una cadena de texto
with open(file_in, "r") as f:
    data_str = f.read()

# Inicializa la lista con los datos de cada fotograma.
# frames_data[j] contiene los datos del fotograma j-ésimo
frames_data = list()

# Itera sobre los bloques de texto separados por líneas vacías
# (cada bloque corresponde a un instante de tiempo)
for frame_data_str in data_str.split("\n\n"):
    # Inicializa la lista con la posición de cada masa
    frame_data = list()

    # Itera sobre las líneas del bloque
    # (cada línea da la posición de una masa)
    for masas_pos_str in frame_data_str.split("\n"):
        # Lee la componente x e y de la línea
        masas_pos = np.fromstring(masas_pos_str, sep=",")
        # Si la línea no está vacía, añade masas_pos a la lista de 
        # posiciones del fotograma
        if masas_pos.size > 0:
            frame_data.append(np.fromstring(masas_pos_str, sep=","))

    # Añade los datos de este fotograma a la lista
    frames_data.append(frame_data)

# El número de masas es el número de líneas en cada bloque
# Lo calculamos del primer bloque
nmasas = len(frames_data[0])

# Verifica que el número de colores coincida con el número de masas
if len(masas_colors) != nmasas:
    raise ValueError("El número de colores especificados no coincide con el número de planetas")

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
    masas_radius = masas_radius*np.ones(nmasas)
# En caso contrario, comprueba que el nº de radios coincide con el
# nº de masas y devuelve error en caso contrario
else:
    if not nmasas == len(masas_radius):
        raise ValueError(
                "El número de radios especificados no coincide con el número "
                "de planetas")

# Representa el primer fotograma
# Pinta un punto en la posición de cada masa y guarda el objeto asociado
# al punto en una lista
masas_points = list()
masas_trails = list()
for masas_pos, radius, color in zip(frames_data[0], masas_radius, masas_colors):
    x, y = masas_pos
    masas_point = Circle((x, y), radius, color=color)
    ax.add_artist(masas_point)
    masas_points.append(masas_point)

    # Inicializa las estelas (si especificado en los parámetros)
    if show_trail:
        masas_trail, = ax.plot(
                x, y, "-", linewidth=trail_width,
                color=color)
        masas_trails.append(masas_trail)

# Inicializa las líneas
line_origin_to_first, = ax.plot([], [], 'k-')
line_first_to_second, = ax.plot([], [], 'k-')

# Función que actualiza la posición de las masas y las líneas en la animación 
def update(j_frame, frames_data, masas_points, masas_trails, show_trail):
    # Actualiza la posición del correspondiente a cada planeta
    for j_masa, masas_pos in enumerate(frames_data[j_frame]):
        x, y = masas_pos
        masas_points[j_masa].center = (x, y)

        if show_trail:
            xs_old, ys_old = masas_trails[j_masa].get_data()
            xs_new = np.append(xs_old, x)
            ys_new = np.append(ys_old, y)

            masas_trails[j_masa].set_data(xs_new, ys_new)

    # Actualiza las líneas
    line_origin_to_first.set_data([0, frames_data[j_frame][0][0]], [0, frames_data[j_frame][0][1]])
    line_first_to_second.set_data(
        [frames_data[j_frame][0][0], frames_data[j_frame][1][0]], 
        [frames_data[j_frame][0][1], frames_data[j_frame][1][1]]
    )

    return masas_points + masas_trails + [line_origin_to_first, line_first_to_second]

def init_anim():
    # Clear trails
    if show_trail:
        for j_masa in range(nmasas):
            masas_trails[j_masa].set_data(list(), list())

    # Inicializa las líneas
    line_origin_to_first.set_data([], [])
    line_first_to_second.set_data([], [])

    return masas_points + masas_trails + [line_origin_to_first, line_first_to_second]

# Calcula el nº de frames
nframes = len(frames_data)

# Si hay más de un instante de tiempo, genera la animación
if nframes > 1:
    # Info sobre FuncAnimation: https://matplotlib.org/stable/api/animation_api.html
    animation = FuncAnimation(
            fig, update, init_func=init_anim,
            fargs=(frames_data, masas_points, masas_trails, show_trail),
            frames=len(frames_data), blit=True, interval=interval)

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
        plt.show
