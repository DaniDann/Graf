import glfw
from OpenGL.GL import glClearColor, glEnable, glClear, glLoadIdentity, glTranslatef, glRotatef, glMatrixMode
from OpenGL.GL import glBegin, glColor3f, glVertex3f, glEnd, glFlush, glViewport
from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST,  GL_TRIANGLES, GL_PROJECTION, \
    GL_MODELVIEW
from OpenGL.GLU import gluPerspective
import sys

# Variables globales
window = None
angle = 0


def init():
    # Configuración inicial de OpenGL
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Color de fondo negro
    glEnable(GL_DEPTH_TEST)  # Activar prueba de profundidad para 3D

    # Configuración de proyección
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 0.1, 50.0)

    # Cambiar a la matriz de modelo para los objetos
    glMatrixMode(GL_MODELVIEW)


def draw_pyramid():
    global angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpiar pantalla y buffer de profundidad

    # Configuración de la vista de la pirámide
    glLoadIdentity()
    glTranslatef(0, 0, -7)  # Alejar la pirámide para que sea visible
    glRotatef(angle, 0, 0, 0)  # Rotar la pirámide

    # Vértices de la base
    base1 = (1.0, 0, 0.5)
    base2 = (-1.0, 0, 0.5)
    base3 = (0.0, 0, -1.0)
    punta = (0,1,0)


    # Dibujar las 4 caras triangulares
    glBegin(GL_TRIANGLES)

    # Cara base
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(*base1)
    glVertex3f(*base2)
    glVertex3f(*base3)

   # Cara frontal (colores)
    glVertex3f(*punta)
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(*base1)
    glColor3f(0, 1.0, 1.0)
    glVertex3f(*base2)
    glColor3f(1.0, 1.0, 1.0)


    # Cara izquierda (verde)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(*punta)
    glVertex3f(*base2)
    glVertex3f(*base3)

    # Cara trasera (azul)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(*punta)
    glVertex3f(*base1)
    glVertex3f(*base3)

    glEnd()

    # Dibujar la base (cuadrada)


    glFlush()
    glfw.swap_buffers(window)  # Intercambiar buffers para animación suave
    angle += 1  # Incrementar el ángulo para rotación


def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()

    # Crear ventana de GLFW
    width, height = 500, 500
    window = glfw.create_window(width, height, "piramide rotativa OPENGL", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    # Configurar el contexto de OpenGL en la ventana
    glfw.make_context_current(window)

    # Configuración de viewport y OpenGL
    glViewport(0, 0, width, height)
    init()

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_pyramid()
        glfw.poll_events()

    glfw.terminate()  # Cerrar GLFW al salir


if __name__ == "__main__":
    main()
