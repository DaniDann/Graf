import glfw
import cv2
import mediapipe as mp
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

# ============================================================
# Configuración
# ============================================================
# WINDOW_WIDTH
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_TITLE = "Mascara 3D Extendida + Mediapipe"

# Conexiones para dibujar el contorno facial
contorno_cara = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
                 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
                 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]

# Cejas
LEFT_EYEBROW = [70, 63, 105, 66, 107]
RIGHT_EYEBROW = [336, 296, 334, 293, 300]


def init_glfw():
    if not glfw.init():
        raise Exception("No se pudo inicializar GLFW")

    # No especificar version de OpenGL - usar la mejor disponible compatible
    # con fixed-function pipeline (glBegin/glEnd, GL_LIGHTING, etc.)

    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, None, None)

    if not window:
        glfw.terminate()
        raise Exception("No se pudo crear la ventana GLFW")

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    return window


# ============================================================
# Configuracion inicial de OpenGL
# ============================================================
def setup_opengl():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)


def create_video_texture():
    video_tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, video_tex)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    return video_tex


def setup_lights():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)  # Luz adicional
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    # Luz principal frontal
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 2, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1))

    # Luz de relleno lateral
    glLightfv(GL_LIGHT1, GL_POSITION, (1, 1, 1, 0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.5, 0.5, 0.5, 1))


# ============================================================
# Funciones de dibujo
# ============================================================
def draw_sphere(x, y, z, radius, color=(1, 1, 1)):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(*color)
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, 16, 16)
    gluDeleteQuadric(quad)
    glPopMatrix()


def draw_line(p1, p2, color=(1, 1, 1), width=2.0):
    """Dibuja una línea entre dos puntos 3D"""
    glDisable(GL_LIGHTING)
    glLineWidth(width)
    glColor3f(*color)
    glBegin(GL_LINES)
    glVertex3f(*p1)
    glVertex3f(*p2)
    glEnd()
    glEnable(GL_LIGHTING)


def norm_landmark(p):
    return (p.x - 0.5, -(p.y - 0.5), p.z)


# ============================================================
# Renderizado
# ============================================================
def render_video_background(frame_rgb, video_tex):
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1, 0, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glBindTexture(GL_TEXTURE_2D, video_tex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                 frame_rgb.shape[1], frame_rgb.shape[0],
                 0, GL_RGB, GL_UNSIGNED_BYTE, frame_rgb)

    glColor3f(1.0, 1.0, 1.0)

    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1);
    glVertex2f(0, 0)
    glTexCoord2f(1, 1);
    glVertex2f(1, 0)
    glTexCoord2f(1, 0);
    glVertex2f(1, 1)
    glTexCoord2f(0, 0);
    glVertex2f(0, 1)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_face_contour(landmarks, indices, color=(0.3, 0.8, 0.4)):
    glDisable(GL_LIGHTING)
    glLineWidth(1.5)
    glColor3f(*color)

    glBegin(GL_LINE_STRIP)
    for idx in indices:
        p = norm_landmark(landmarks[idx])
        glVertex3f(*p)
    # Cerrar el contorno
    p = norm_landmark(landmarks[indices[0]])
    glVertex3f(*p)
    glEnd()

    glEnable(GL_LIGHTING)


def render_3d_mask_extended(face_landmarks):
    """Renderiza la máscara 3D extendida"""
    glEnable(GL_DEPTH_TEST)
    glClear(GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluPerspective(45, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    gluLookAt(0, 0, 2, 0, 0, 0, 0, 1, 0)

    setup_lights()

    lm = face_landmarks.landmark

    # ============================================================
    # 1. CONTORNO CARA
    # ============================================================
    draw_face_contour(lm, contorno_cara, color=(0.2, 0.6, 0.3))

    # ============================================================
    # 2. OJOS
    # ============================================================
    left_eye = lm[386]
    right_eye = lm[159]
    lx, ly, lz = norm_landmark(left_eye)
    rx, ry, rz = norm_landmark(right_eye)

    # Globos oculares (blancos)
    glColor3f(1.0, 1.0, 1.0)
    draw_sphere(lx, ly, lz, 0.028, (1, 1, 1))
    draw_sphere(rx, ry, rz, 0.028, (1, 1, 1))

    # Pupilas (azul oscuro)
    draw_sphere(lx, ly, lz + 0.012, 0.016, (0.1, 0.1, 0.4))
    draw_sphere(rx, ry, rz + 0.012, 0.016, (0.1, 0.1, 0.4))

    # Brillos en los ojos
    draw_sphere(lx + 0.008, ly + 0.008, lz + 0.018, 0.006, (1, 1, 1))
    draw_sphere(rx + 0.008, ry + 0.008, rz + 0.018, 0.006, (1, 1, 1))

    # ============================================================
    # 3. CEJAS
    # ============================================================
    draw_face_contour(lm, LEFT_EYEBROW, color=(0.3, 0.2, 0.1))
    draw_face_contour(lm, RIGHT_EYEBROW, color=(0.3, 0.2, 0.1))

    # Agregar esferas a las  cejas para hacerlas mas visibles
    for idx in LEFT_EYEBROW[::2]:  # Cada dos puntos
        px, py, pz = norm_landmark(lm[idx])
        draw_sphere(px, py, pz, 0.008, (0.4, 0.3, 0.2))

    for idx in RIGHT_EYEBROW[::2]:
        px, py, pz = norm_landmark(lm[idx])
        draw_sphere(px, py, pz, 0.008, (0.4, 0.3, 0.2))

    # ============================================================
    # 4. NARIZ
    # ============================================================
    nose_tip = lm[1]
    nose_bridge = lm[6]
    nose_left = lm[98]
    nose_right = lm[327]

    nx, ny, nz = norm_landmark(nose_tip)
    nbx, nby, nbz = norm_landmark(nose_bridge)
    nlx, nly, nlz = norm_landmark(nose_left)
    nrx, nry, nrz = norm_landmark(nose_right)

    # Punta de la nariz (roja)
    draw_sphere(nx, ny, nz, 0.022, (1.0, 0.3, 0.3))

    # Fosas
    draw_sphere(nlx, nly, nlz, 0.012, (0.8, 0.4, 0.4))
    draw_sphere(nrx, nry, nrz, 0.012, (0.8, 0.4, 0.4))

    # Puente de la nariz (linea)
    draw_line((nbx, nby, nbz), (nx, ny, nz), color=(1, 0.5, 0.5), width=3)

    # ============================================================
    # 5. BOCA
    # ============================================================
    mouth_left = lm[61]
    mouth_right = lm[291]
    mouth_top = lm[13]
    mouth_bottom = lm[14]

    mlx, mly, mlz = norm_landmark(mouth_left)
    mrx, mry, mrz = norm_landmark(mouth_right)
    mtx, mty, mtz = norm_landmark(mouth_top)
    mbx, mby, mbz = norm_landmark(mouth_bottom)

    # Comisuras (rosas)
    draw_sphere(mlx, mly, mlz, 0.015, (1.0, 0.5, 0.6))
    draw_sphere(mrx, mry, mrz, 0.015, (1.0, 0.5, 0.6))

    # Labio superior e inferior
    draw_sphere(mtx, mty, mtz, 0.012, (1.0, 0.4, 0.5))
    draw_sphere(mbx, mby, mbz, 0.012, (1.0, 0.4, 0.5))

    # Linea de la boca
    draw_line((mlx, mly, mlz), (mrx, mry, mrz), color=(1, 0.3, 0.4), width=3)

    # ============================================================
    # 6. CACHETES
    # ============================================================
    left_cheek = lm[234]
    right_cheek = lm[454]

    lcx, lcy, lcz = norm_landmark(left_cheek)
    rcx, rcy, rcz = norm_landmark(right_cheek)

    # Rubor en las mejillas (rosado suave, más pequeño)
    draw_sphere(lcx, lcy, lcz, 0.025, (1.0, 0.8, 0.85))
    draw_sphere(rcx, rcy, rcz, 0.025, (1.0, 0.8, 0.85))

    # ============================================================
    # 7. FRENTE Y BARBA
    # ============================================================
    forehead = lm[10]
    chin = lm[152]

    fx, fy, fz = norm_landmark(forehead)
    cx, cy, cz = norm_landmark(chin)

    # Punto en la frente (color suave)
    draw_sphere(fx, fy, fz, 0.015, (0.9, 0.9, 0.7))

    # Punto en la barbilla (color suave)
    draw_sphere(cx, cy, cz, 0.015, (0.7, 0.9, 0.8))

    # Restaurar matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


# ============================================================
# Función principal
# ============================================================
def main():
    try:
        window = init_glfw()
    except Exception as e:
        print(f" Error al inicializar GLFW: {e}")
        return

    setup_opengl()
    video_tex = create_video_texture()

    mp_face = mp.solutions.face_mesh
    face_mesh = mp_face.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5,
                                 min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print(" No se pudo abrir la camara")
        glfw.terminate()
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)
    print("Camara inicializada")

    frame_count = 0
    fps_timer = glfw.get_time()

    try:
        while not glfw.window_should_close(window):
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = face_mesh.process(frame_rgb)

            glfw.poll_events()

            if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
                break

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            render_video_background(frame_rgb, video_tex)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    render_3d_mask_extended(face_landmarks)

            glfw.swap_buffers(window)

            frame_count += 1
            current_time = glfw.get_time()
            if current_time - fps_timer >= 1.0:
                fps = frame_count / (current_time - fps_timer)
                glfw.set_window_title(window, f"{WINDOW_TITLE} - FPS: {fps:.1f}")
                frame_count = 0
                fps_timer = current_time

    except Exception as e:
        print(f" Error en el loop principal: {e}")
        import traceback
        traceback.print_exc()

    finally:
        print("\nCerrando aplicación...")
        cap.release()
        face_mesh.close()
        glfw.terminate()


if __name__ == "__main__":
    main()