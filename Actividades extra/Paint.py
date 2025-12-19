import cv2
import numpy as np


class PinturaVirtual:
    def __init__(self, color_hsv_bajo, color_hsv_alto, ancho=640, alto=480):

        self.color_hsv_bajo = np.array(color_hsv_bajo)
        self.color_hsv_alto = np.array(color_hsv_alto)

        # lienzo
        self.lienzo = np.ones((alto, ancho, 3), dtype=np.uint8) * 255

        # trazo
        self.punto_anterior = None
        self.dibujando = False

        # Configuracion del trazo
        self.color_trazo = (0, 0, 255)  # Rojo en BGR
        self.grosor_trazo = 5

    def detectar_landmark(self, frame):
        # BGR a HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # mascara del color
        mascara = cv2.inRange(hsv, self.color_hsv_bajo, self.color_hsv_alto)

        # limpia el ruido
        kernel = np.ones((5, 5), np.uint8)
        mascara = cv2.erode(mascara, kernel, iterations=1)
        mascara = cv2.dilate(mascara, kernel, iterations=2)

        # Encontrar contornos
        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)

        if contornos:
            # contorno mas grande
            contorno_max = max(contornos, key=cv2.contourArea)

            # checa si es suficiente el tamaño
            if cv2.contourArea(contorno_max) > 500:
                # centroide
                M = cv2.moments(contorno_max)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    return (cx, cy)

        return None

    def dibujar_trazo(self, punto_actual):
        """
        Dibuja una línea desde el punto anterior hasta el punto actual
        Args:
        punto actual: tuple (x, y) de la posición actual
        """
        if self.punto_anterior is not None and self.dibujando:
            # Dibujar linea en el lienzo
            cv2.line(self.lienzo, self.punto_anterior, punto_actual,
                     self.color_trazo, self.grosor_trazo)

        self.punto_anterior = punto_actual

    def limpiar_lienzo(self):
        """Limpia el lienzo completamente"""
        self.lienzo.fill(255)
        self.punto_anterior = None

    def cambiar_color_trazo(self, color_bgr):
        """Cambia el color del trazo (formato BGR)"""
        self.color_trazo = color_bgr

    def cambiar_grosor(self, grosor):
        """Cambia el grosor del trazo"""
        self.grosor_trazo = grosor

    def ejecutar(self):
        """Loop principal de captura y procesamiento"""
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: No se pudo abrir la cámara")
            return

        # Configurar resolución de la cámara para que coincida con el lienzo
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.lienzo.shape[1])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.lienzo.shape[0])

        print("Controles:")
        print("  ESPACIO - Alternar dibujo ON/OFF")
        print("  C - Limpiar lienzo")
        print("  R - Color rojo")
        print("  G - Color verde")
        print("  B - Color azul")
        print("  + - Aumentar grosor")
        print("  - - Disminuir grosor")
        print("  Q - Salir")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error al capturar frame")
                break

            # Voltear horizontalmente para efecto espejo
            frame = cv2.flip(frame, 1)

            # Redimensionar frame para que coincida con el lienzo
            frame = cv2.resize(frame, (self.lienzo.shape[1], self.lienzo.shape[0]))

            # Detectar el landmark (objeto de color)
            punto = self.detectar_landmark(frame)

            if punto is not None:
                # Dibujar círculo indicador en el video
                cv2.circle(frame, punto, 10, (0, 255, 0), -1)

                # Dibujar trazo en el lienzo
                if self.dibujando:
                    self.dibujar_trazo(punto)
                    cv2.putText(frame, "DIBUJANDO", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    self.punto_anterior = punto
                    cv2.putText(frame, "PAUSADO", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                # Si no se detecta, resetear punto anterior
                self.punto_anterior = None
                cv2.putText(frame, "NO DETECTADO", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # ventana separadas
            cv2.imshow("Camara", frame)
            cv2.imshow("Lienzo Virtual", self.lienzo)

            # Botones
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break
            elif key == ord(' '):
                self.dibujando = not self.dibujando
                print(f"Dibujo: {'ON' if self.dibujando else 'OFF'}")
            elif key == ord('c'):
                self.limpiar_lienzo()
                print("Lienzo limpiado")
            elif key == ord('r'):
                self.cambiar_color_trazo((0, 0, 255))
                print("Color: ROJO")
            elif key == ord('g'):
                self.cambiar_color_trazo((0, 255, 0))
                print("Color: VERDE")
            elif key == ord('b'):
                self.cambiar_color_trazo((255, 0, 0))
                print("Color: AZUL")
            elif key == ord('+') or key == ord('='):
                self.grosor_trazo = min(self.grosor_trazo + 2, 30)
                print(f"Grosor: {self.grosor_trazo}")
            elif key == ord('-'):
                self.grosor_trazo = max(self.grosor_trazo - 2, 1)
                print(f"Grosor: {self.grosor_trazo}")

        cap.release()
        cv2.destroyAllWindows()


# Ejemplo de uso
if __name__ == "__main__":
    #  AZUL:
    color_bajo = (100, 50, 50)
    color_alto = (130, 255, 255)

    #  VERDE:
    # color_bajo = (40, 50, 50)
    # color_alto = (80, 255, 255)

    # ROJO a naranja:
    # color_bajo = (0, 50, 50)
    # color_alto = (10, 255, 255)

    # ROJO a violeta:
    # color_bajo = (170, 50, 50)
    # color_alto = (180, 255, 255)

    pintura = PinturaVirtual(color_bajo, color_alto, ancho=640, alto=480)
    pintura.ejecutar()