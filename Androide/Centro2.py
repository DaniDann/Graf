import cv2

cap = cv2.VideoCapture(0)

def encontrar_centroides(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    resultado = frame.copy()

    for contorno in contornos:

        area = cv2.contourArea(contorno)
        if area > 500:

            M = cv2.moments(contorno)

            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])


                cv2.drawContours(resultado, [contorno], -1, (0, 0, 255), 2)

                cv2.circle(resultado, (cx, cy), 8, (255, 0, 0), -1)
                cv2.circle(resultado, (cx, cy), 3, (255, 255, 255), -1)

                cv2.putText(resultado,f"({cx},{cy})",(cx - 50, cy - 20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255, 255, 255),1,)

                cv2.putText(resultado,f"Area: {int(area)}",(cx - 50, cy + 30),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0, 255, 255),1,)

    return resultado, thresh

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar video")
        break

    # Voltear horizontalmente para efecto espejo
    frame = cv2.flip(frame, 1)

    # Encontrar y mostrar centroides
    resultado, thresh = encontrar_centroides(frame)

    # Mostrar ventanas
    cv2.imshow("Detector de Centroides", resultado)
    cv2.imshow("Umbralizacion", thresh)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord("q,"):
        break

# Limpiar recursos
cap.release()
cv2.destroyAllWindows()