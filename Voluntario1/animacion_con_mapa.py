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
# Se añaden animaciones de la trayectoria en el espacio de fases en subplots,
# el formato de estos ficheros se estructura de igual forma
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
file_in1 = "posiciones_pendulo15.dat" # Nombre del fichero de datos para el péndulo
file_in2 = "mapa_poincare_angulos15.dat" # Nombre del fichero de datos para el espacio de fases de los ángulos
file_in3 = "mapa_poincare_phi15.dat" # Nombre del fichero de datos para el espacio de fases de phi
file_in4 = "mapa_poincare_psi15.dat" # Nombre del fichero de datos para el espacio de fases de psi

file_out = "animacion_con_mapa_15" # Nombre del fichero de salida (sin extensión)

# Límites de los ejes X e Y para el péndulo 1
x_min1 = -3.0
x_max1 = 3.0
y_min1 = -3.0
y_max1 = 3.0

# Límites de los ejes X e Y para el mapa de Poincaré 2
x_min2 = -4.0
x_max2 = 120.0
y_min2 = -10.0
y_max2 = 120.0

# Límites de los ejes X e Y para el mapa de Poincaré 3
x_min3 = -4.0
x_max3 = 120.0
y_min3 = -1.0
y_max3 = 4.0

# Límites de los ejes X e Y para el mapa de Poincaré 4
x_min4 = -10.0
x_max4 = 120.0
y_min4 = -4.0
y_max4 = 5.0

interval =  0.1  # Tiempo entre fotogramas en milisegundos
show_trail = True  # Muestra la "estela" de la masa
trail_width = 1  # Ancho de la estela
save_to_file = False  # False: muestra la animación por pantalla, True: la guarda en un fichero
dpi = 150  # Calidad del vídeo de salida (dots per inch)

# Radio de la masa, en las mismas unidades que la posición
masas_radius = 0.02

# Colores para cada masa
masas_colors = ['green', 'red']
angulo_color = 'blue'
phi_color = 'green'
psi_color = 'red'

# Lectura del fichero de datos
# ========================================
def read_data(file_in):
    with open(file_in, "r") as f:
        data_str = f.read()
    
    frames_data = []
    for frame_data_str in data_str.strip().split("\n\n"):
        frame_data = [list(map(float, line.split(','))) for line in frame_data_str.split("\n") if line]
        frames_data.append(frame_data)
    
    return frames_data

frames_data1 = read_data(file_in1)
frames_data2 = read_data(file_in2)
frames_data3 = read_data(file_in3)
frames_data4 = read_data(file_in4)

# Verifica que los datos no estén vacíos
if not frames_data1 or not frames_data2 or not frames_data3 or not frames_data4:
    raise ValueError("Uno o más archivos de datos están vacíos o no tienen el formato correcto.")

# Número de masas
nmasas1 = len(frames_data1[0])
nmasas2 = len(frames_data2[0])
nmasas3 = len(frames_data3[0])
nmasas4 = len(frames_data4[0])

# Verifica que el número de colores coincida con el número de masas
if len(masas_colors) != nmasas1:
    raise ValueError("El número de colores especificados no coincide con el número de masas")

# Creación de la animación/gráfico
# ========================================
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

# Primer Subplot
ax1.axis("equal")
ax1.set_xlim(x_min1, x_max1)
ax1.set_ylim(y_min1, y_max1)
ax1.set_title('Trayectoria del Péndulo')
ax1.set_xlabel(r'$x$')
ax1.set_ylabel(r'$y$')

# Segundo Subplot
ax2.set_xlim(x_min2, x_max2)
ax2.set_ylim(y_min2, y_max2)
ax2.set_title('Mapas de Poincaré')
ax2.set_xlabel(r'$\phi \, (\mathrm{rad})$')
ax2.set_ylabel(r'$\psi \, (\mathrm{rad})$')

# Tercer Subplot
ax3.set_xlim(x_min3, x_max3)
ax3.set_ylim(y_min3, y_max3)
ax3.set_xlabel(r'$\phi \, (\mathrm{rad})$')
ax3.set_ylabel(r'$\dot\phi\, (\mathrm{rad/s})$')

# Cuarto Subplot
ax4.set_xlim(x_min4, x_max4)
ax4.set_ylim(y_min4, y_max4)
ax4.set_xlabel(r'$\psi \, (\mathrm{rad})$')
ax4.set_ylabel(r'$\dot\psi\, (\mathrm{rad/s})$')


# Puntos de las masas en el primer subplot
masas_points1 = [Circle((0, 0), masas_radius, color=color) for color in masas_colors]
for point in masas_points1:
    ax1.add_artist(point)

# Estelas de las masas en el primer subplot
masas_trails1 = [ax1.plot([], [], "-", linewidth=trail_width, color=color)[0] for color in masas_colors]

# Líneas de conexión entre el origen, la masa 1 y la masa 2
line_origen_masa1, = ax1.plot([], [], color='black', linewidth=1)
line_masa1_masa2, = ax1.plot([], [], color='black', linewidth=1)

# Líneas de los mapas de Poincaré
lines2 = ax2.plot([], [], '-', color=angulo_color, markersize=1)[0]
lines3 = ax3.plot([], [], '-', color=phi_color, markersize=1)[0]
lines4 = ax4.plot([], [], '-', color=psi_color, markersize=1)[0]

def update(j_frame):
    # Actualiza las posiciones de las masas y sus estelas
    for i, (masas_pos, masas_point) in enumerate(zip(frames_data1[j_frame], masas_points1)):
        x, y = masas_pos
        masas_point.set_center((x, y))

        if show_trail:
            trail_data = np.array([frame[i] for frame in frames_data1[:j_frame+1]])
            masas_trails1[i].set_data(trail_data[:, 0], trail_data[:, 1])

    # Actualiza las líneas de conexión
    masa1_pos = frames_data1[j_frame][0]
    masa2_pos = frames_data1[j_frame][1]
    line_origen_masa1.set_data([0, masa1_pos[0]], [0, masa1_pos[1]])
    line_masa1_masa2.set_data([masa1_pos[0], masa2_pos[0]], [masa1_pos[1], masa2_pos[1]])

    # Actualiza los mapas de Poincaré
    lines2.set_data(*zip(*[frame[0] for frame in frames_data2[:j_frame+1]]))
    lines3.set_data(*zip(*[frame[0] for frame in frames_data3[:j_frame+1]]))
    lines4.set_data(*zip(*[frame[0] for frame in frames_data4[:j_frame+1]]))

    return masas_points1 + masas_trails1 + [line_origen_masa1, line_masa1_masa2, lines2, lines3, lines4]


# Añade un título principal encima de los subplots
fig.suptitle('Energía = 15', fontsize=16)

# Crea la animación
anim = FuncAnimation(fig, update, frames=len(frames_data1), interval=interval, blit=True)

if save_to_file:
    anim.save(file_out + ".mp4", dpi=dpi)
else:
    plt.show()