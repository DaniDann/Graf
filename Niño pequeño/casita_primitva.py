import glfw
from OpenGL.GL import *
from OpenGL.GLU import *


def casita():

    # Cuerpo de la casa usando GL_QUADS
    glBegin(GL_QUADS)
    # Pared principal - amarillo
    glColor3f(1.0, 1, 0.3)
    glVertex2f(-0.4, -0.6)  # Inferior izquierda
    glVertex2f(0.4, -0.6)  # Inferior derecha
    glVertex2f(0.4, 0.1)  # Superior derecha
    glVertex2f(-0.4, 0.1)  # Superior izquierda
    glEnd()

    # Techo usando GL_TRIANGLES
    glBegin(GL_TRIANGLES)
    # Techo - rojo
    glColor3f(0.8, 0.2, 0.2)
    glVertex2f(-0.5, 0.1)  # Izquierda
    glColor3f(1.0, 0.3, 0.3)
    glVertex2f(0.5, 0.1)  # Derecha
    glColor3f(0.9, 0.1, 0.1)
    glVertex2f(0.0, 0.5)  # Punta del techo
    glEnd()

    # Detalles adicionales con las mismas primitivas
    # Puerta usando GL_QUADS
    glBegin(GL_QUADS)
    glColor3f(0.4, 0.2, 0.1)
    glVertex2f(-0.1, -0.6)
    glVertex2f(0.1, -0.6)
    glVertex2f(0.1, -0.2)
    glVertex2f(-0.1, -0.2)
    glEnd()

    # Ventanas usando GL_QUADS
    glBegin(GL_QUADS)
    # Ventana izquierda
    glColor3f(0.6, 0.8, 1.0)
    glVertex2f(-0.3, -0.1)
    glVertex2f(-0.15, -0.1)
    glVertex2f(-0.15, 0.0)
    glVertex2f(-0.3, 0.0)

    # Ventana derecha
    glVertex2f(0.15, -0.1)
    glVertex2f(0.3, -0.1)
    glVertex2f(0.3, 0.0)
    glVertex2f(0.15, 0.0)
    glEnd()


def main():
    # Inicializa GLFW
    if not glfw.init():
        return

    # Crear ventana
    window = glfw.create_window(800, 600, "Casa - GL_QUADS + GL_TRIANGLES", None, None)
    if not window:
        glfw.terminate()
        return

    # Hacer el contexto de OpenGL actual
    glfw.make_context_current(window)

    # Configurar color de fondo (cielo azul)
    glClearColor(0.5, 0.7, 1.0, 1.0)

    # Bucle principal
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        # Configurar proyección
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Dibujar la casa
        casita()

        glfw.swap_buffers(window)
        glfw.poll_events()

    # Finalizar GLFW
    glfw.terminate()


if __name__ == "__main__":
    main()