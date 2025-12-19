import glfw
import cv2
import mediapipe as mp
import numpy as np
import math
from OpenGL.GL import *
from OpenGL.GLU import *

# ============================================================
# Configuración
# ============================================================
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_TITLE = "Filtro AR: Máscara Iron Man"

# Variables globales para animaciones
animation_time = 0.0

# Colores Iron Man
GOLD = (0.85, 0.65, 0.13)
DARK_RED = (0.6, 0.0, 0.0)
BRIGHT_RED = (0.9, 0.1, 0.1)
LIGHT_BLUE = (0.5, 0.8, 1.0)
WHITE = (1.0, 1.0, 1.0)

# Landmarks clave
FACE_OVAL = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
             397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
             172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]


def setup_opengl():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_POLYGON_SMOOTH)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)


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
    glEnable(GL_LIGHT1)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    # Luz principal
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 1, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1))

    # Luz de relleno
    glLightfv(GL_LIGHT1, GL_POSITION, (0.5, 0.5, 0.5, 0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.7, 0.7, 0.7, 1))

    # Material especular para brillo metálico
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (1, 1, 1, 1))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 100)


def norm_landmark(p):
    """Normaliza las coordenadas del landmark"""
    return (p.x - 0.5, 0.5 - p.y, -p.z * 0.5)


def draw_sphere(x, y, z, radius, color=(1, 1, 1)):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(*color)
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, 24, 24)
    gluDeleteQuadric(quad)
    glPopMatrix()


def draw_quad(p1, p2, p3, p4, color=(1, 1, 1)):
    """Dibuja un cuadrilátero con iluminación"""
    glColor3f(*color)
    glBegin(GL_QUADS)

    # Calcular normal
    v1 = np.array([p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]])
    v2 = np.array([p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]])
    normal = np.cross(v1, v2)
    norm_mag = np.linalg.norm(normal)
    if norm_mag > 0:
        normal = normal / norm_mag

    glNormal3f(normal[0], normal[1], normal[2])
    glVertex3f(*p1)
    glVertex3f(*p2)
    glVertex3f(*p3)
    glVertex3f(*p4)
    glEnd()


def draw_triangle(p1, p2, p3, color=(1, 1, 1)):
    """Dibuja un triángulo con iluminación"""
    glColor3f(*color)
    glBegin(GL_TRIANGLES)

    # Calcular normal
    v1 = np.array([p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]])
    v2 = np.array([p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]])
    normal = np.cross(v1, v2)
    norm_mag = np.linalg.norm(normal)
    if norm_mag > 0:
        normal = normal / norm_mag

    glNormal3f(normal[0], normal[1], normal[2])
    glVertex3f(*p1)
    glVertex3f(*p2)
    glVertex3f(*p3)
    glEnd()


def draw_glowing_eyes(lm):
    """Dibuja los ojos brillantes de Iron Man"""
    global animation_time

    # Posiciones de los ojos
    left_eye_center = norm_landmark(lm[159])
    right_eye_center = norm_landmark(lm[386])

    # Pulso de brillo
    pulse = 0.85 + 0.15 * math.sin(animation_time * 3)
    glow_pulse = 0.7 + 0.3 * math.sin(animation_time * 2.5)

    for eye_pos in [left_eye_center, right_eye_center]:
        ex, ey, ez = eye_pos

        # Núcleo brillante blanco
        glDisable(GL_LIGHTING)
        draw_sphere(ex, ey, ez + 0.015, 0.018 * pulse, (1, 1, 1))

        # Resplandor azul
        glColor4f(LIGHT_BLUE[0], LIGHT_BLUE[1], LIGHT_BLUE[2], 0.6 * glow_pulse)
        draw_sphere(ex, ey, ez + 0.014, 0.025 * pulse, LIGHT_BLUE)

        glEnable(GL_LIGHTING)


def draw_forehead_piece(lm):
    """Dibuja la pieza de la frente (dorada)"""
    # Puntos clave de la frente
    forehead_top = norm_landmark(lm[10])
    forehead_left = norm_landmark(lm[103])
    forehead_right = norm_landmark(lm[332])
    nose_bridge = norm_landmark(lm[6])
    left_eyebrow = norm_landmark(lm[70])
    right_eyebrow = norm_landmark(lm[300])

    offset = 0.02

    # Pieza central de la frente (dorada)
    ft_top = (forehead_top[0], forehead_top[1], forehead_top[2] + offset)
    nb = (nose_bridge[0], nose_bridge[1], nose_bridge[2] + offset)
    leb = (left_eyebrow[0], left_eyebrow[1], left_eyebrow[2] + offset)
    reb = (right_eyebrow[0], right_eyebrow[1], right_eyebrow[2] + offset)

    # Triángulo central dorado
    center_top = (forehead_top[0], forehead_top[1] + 0.03, forehead_top[2] + offset)
    draw_triangle(center_top, leb, reb, GOLD)
    draw_quad(leb, reb, nb, nb, GOLD)


def draw_face_plate(lm):
    """Dibuja la placa facial principal (dorada)"""
    # Puntos del contorno facial
    offset = 0.018

    # Región de mejillas (dorada)
    left_cheek = norm_landmark(lm[234])
    right_cheek = norm_landmark(lm[454])
    left_jaw = norm_landmark(lm[172])
    right_jaw = norm_landmark(lm[397])
    chin = norm_landmark(lm[152])
    nose_tip = norm_landmark(lm[1])

    # Placa dorada izquierda
    lc = (left_cheek[0], left_cheek[1], left_cheek[2] + offset)
    lj = (left_jaw[0], left_jaw[1], left_jaw[2] + offset)
    ch = (chin[0], chin[1], chin[2] + offset)
    nt = (nose_tip[0], nose_tip[1], nose_tip[2] + offset)

    draw_quad(lc, lj, ch, nt, GOLD)

    # Placa dorada derecha
    rc = (right_cheek[0], right_cheek[1], right_cheek[2] + offset)
    rj = (right_jaw[0], right_jaw[1], right_jaw[2] + offset)

    draw_quad(rc, rj, ch, nt, GOLD)


def draw_side_panels(lm):
    """Dibuja los paneles laterales rojos"""
    offset = 0.025

    # Panel izquierdo (rojo oscuro)
    left_temple = norm_landmark(lm[234])
    left_ear = norm_landmark(lm[127])
    left_jaw_upper = norm_landmark(lm[93])
    left_jaw_lower = norm_landmark(lm[172])

    lt = (left_temple[0] - 0.05, left_temple[1] + 0.02, left_temple[2] + offset)
    le = (left_ear[0] - 0.08, left_ear[1], left_ear[2] + offset)
    lju = (left_jaw_upper[0] - 0.03, left_jaw_upper[1] - 0.02, left_jaw_upper[2] + offset)
    ljl = (left_jaw_lower[0] - 0.02, left_jaw_lower[1] - 0.05, left_jaw_lower[2] + offset)

    draw_quad(lt, le, lju, ljl, DARK_RED)

    # Panel derecho (rojo oscuro)
    right_temple = norm_landmark(lm[454])
    right_ear = norm_landmark(lm[356])
    right_jaw_upper = norm_landmark(lm[323])
    right_jaw_lower = norm_landmark(lm[397])

    rt = (right_temple[0] + 0.05, right_temple[1] + 0.02, right_temple[2] + offset)
    re = (right_ear[0] + 0.08, right_ear[1], right_ear[2] + offset)
    rju = (right_jaw_upper[0] + 0.03, right_jaw_upper[1] - 0.02, right_jaw_upper[2] + offset)
    rjl = (right_jaw_lower[0] + 0.02, right_jaw_lower[1] - 0.05, right_jaw_lower[2] + offset)

    draw_quad(rt, re, rju, rjl, DARK_RED)


def draw_top_helmet(lm):
    """Dibuja la parte superior del casco (rojo)"""
    offset = 0.022

    forehead = norm_landmark(lm[10])
    left_forehead = norm_landmark(lm[103])
    right_forehead = norm_landmark(lm[332])
    left_temple = norm_landmark(lm[234])
    right_temple = norm_landmark(lm[454])

    # Cúpula superior roja
    ft = (forehead[0], forehead[1] + 0.08, forehead[2] + offset)
    lf = (left_forehead[0] - 0.04, left_forehead[1] + 0.05, left_forehead[2] + offset)
    rf = (right_forehead[0] + 0.04, right_forehead[1] + 0.05, right_forehead[2] + offset)
    lt = (left_temple[0] - 0.05, left_temple[1] + 0.02, left_temple[2] + offset)
    rt = (right_temple[0] + 0.05, right_temple[1] + 0.02, right_temple[2] + offset)

    # Sección superior roja
    draw_triangle(ft, lf, rf, BRIGHT_RED)
    draw_quad(lf, lt, rt, rf, BRIGHT_RED)


def draw_chin_piece(lm):
    """Dibuja la pieza del mentón (dorada)"""
    offset = 0.02

    chin = norm_landmark(lm[152])
    left_jaw = norm_landmark(lm[172])
    right_jaw = norm_landmark(lm[397])
    mouth_left = norm_landmark(lm[61])
    mouth_right = norm_landmark(lm[291])

    ch = (chin[0], chin[1] - 0.03, chin[2] + offset)
    lj = (left_jaw[0], left_jaw[1] - 0.02, left_jaw[2] + offset)
    rj = (right_jaw[0], right_jaw[1] - 0.02, right_jaw[2] + offset)
    ml = (mouth_left[0], mouth_left[1], mouth_left[2] + offset)
    mr = (mouth_right[0], mouth_right[1], mouth_right[2] + offset)

    # Pieza triangular del mentón
    draw_triangle(ch, lj, ml, GOLD)
    draw_triangle(ch, rj, mr, GOLD)
    draw_quad(ml, mr, rj, lj, GOLD)


def draw_mouth_vent(lm):
    """Dibuja la rejilla de ventilación de la boca"""
    global animation_time

    mouth_left = norm_landmark(lm[61])
    mouth_right = norm_landmark(lm[291])
    mouth_top = norm_landmark(lm[13])
    mouth_bottom = norm_landmark(lm[14])

    offset = 0.022

    # Líneas horizontales de ventilación
    glDisable(GL_LIGHTING)
    glLineWidth(2.0)

    num_lines = 5
    for i in range(num_lines):
        t = i / (num_lines - 1)
        y = mouth_top[1] * (1 - t) + mouth_bottom[1] * t

        # Pulso de brillo
        brightness = 0.3 + 0.2 * math.sin(animation_time * 2 + i)
        glColor3f(brightness, brightness, brightness)

        glBegin(GL_LINES)
        glVertex3f(mouth_left[0], y, mouth_left[2] + offset)
        glVertex3f(mouth_right[0], y, mouth_right[2] + offset)
        glEnd()

    glEnable(GL_LIGHTING)


def draw_edge_highlights(lm):
    """Dibuja los bordes brillantes de la máscara"""
    offset = 0.023

    # Bordes principales
    glDisable(GL_LIGHTING)
    glLineWidth(1.5)
    glColor4f(0.9, 0.9, 0.9, 0.5)

    # Borde entre dorado y rojo (izquierdo)
    left_cheek = norm_landmark(lm[234])
    left_jaw = norm_landmark(lm[172])

    glBegin(GL_LINE_STRIP)
    glVertex3f(left_cheek[0], left_cheek[1], left_cheek[2] + offset)
    glVertex3f(left_jaw[0], left_jaw[1], left_jaw[2] + offset)
    glEnd()

    # Borde entre dorado y rojo (derecho)
    right_cheek = norm_landmark(lm[454])
    right_jaw = norm_landmark(lm[397])

    glBegin(GL_LINE_STRIP)
    glVertex3f(right_cheek[0], right_cheek[1], right_cheek[2] + offset)
    glVertex3f(right_jaw[0], right_jaw[1], right_jaw[2] + offset)
    glEnd()

    glEnable(GL_LIGHTING)


def draw_arc_reactor_glow(lm):
    """Dibuja efecto de resplandor adicional desde el pecho (opcional)"""
    global animation_time

    chin = norm_landmark(lm[152])

    # Resplandor sutil desde abajo
    pulse = 0.3 + 0.1 * math.sin(animation_time * 1.5)

    glDisable(GL_LIGHTING)
    glColor4f(LIGHT_BLUE[0], LIGHT_BLUE[1], LIGHT_BLUE[2], pulse * 0.2)

    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(chin[0], chin[1] - 0.15, chin[2])
    for i in range(13):
        angle = i * 2 * math.pi / 12
        x = chin[0] + 0.1 * math.cos(angle)
        y = chin[1] - 0.08 + 0.02 * math.sin(angle)
        glVertex3f(x, y, chin[2])
    glEnd()

    glEnable(GL_LIGHTING)


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


def render_iron_man_mask(face_landmarks):
    """Renderiza la máscara completa de Iron Man"""
    global animation_time

    glEnable(GL_DEPTH_TEST)
    glClear(GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    aspect = WINDOW_WIDTH / WINDOW_HEIGHT
    glOrtho(-0.5 * aspect, 0.5 * aspect, -0.5, 0.5, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    setup_lights()

    lm = face_landmarks.landmark

    # Renderizar de atrás hacia adelante
    draw_arc_reactor_glow(lm)
    draw_top_helmet(lm)
    draw_side_panels(lm)
    draw_face_plate(lm)
    draw_forehead_piece(lm)
    draw_chin_piece(lm)
    draw_mouth_vent(lm)
    draw_glowing_eyes(lm)
    draw_edge_highlights(lm)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def main():
    global animation_time

    try:
        window = glfw.init()
    except Exception as e:
        print(f"Error al inicializar GLFW: {e}")
        return

    setup_opengl()
    video_tex = create_video_texture()

    mp_face = mp.solutions.face_mesh
    face_mesh = mp_face.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        glfw.terminate()
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)
    print("=" * 50)
    print("  FILTRO AR: MÁSCARA DE IRON MAN")
    print("=" * 50)
    print("🎭 Cámara inicializada")
    print("🦾 Activando protocolo J.A.R.V.I.S...")
    print("⚡ Presiona ESC para salir")
    print("=" * 50)

    frame_count = 0
    fps_timer = glfw.get_time()
    start_time = glfw.get_time()

    try:
        while not glfw.window_should_close(window):
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = face_mesh.process(frame_rgb)

            animation_time = glfw.get_time() - start_time

            glfw.poll_events()

            if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
                break

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            render_video_background(frame_rgb, video_tex)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    render_iron_man_mask(face_landmarks)

            glfw.swap_buffers(window)

            frame_count += 1
            current_time = glfw.get_time()
            if current_time - fps_timer >= 1.0:
                fps = frame_count / (current_time - fps_timer)
                glfw.set_window_title(window, f"{WINDOW_TITLE} - FPS: {fps:.1f}")
                frame_count = 0
                fps_timer = current_time

    except Exception as e:
        print(f"Error en el loop principal: {e}")
        import traceback
        traceback.print_exc()

    finally:
        print("\n🔴 Desactivando protocolo J.A.R.V.I.S...")
        print("Cerrando aplicación...")
        cap.release()
        face_mesh.close()
        glfw.terminate()


if __name__ == "__main__":
    main()

