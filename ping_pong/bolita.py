import cv2 as cv
import numpy as np
import math

# Canvas
img = np.ones((500, 500, 3), np.uint8) * 255

# Pelota
pos_x, pos_y = 250, 250
vel_x, vel_y = 5, 5
radio = 6

# Barra
obs_x = 200
obs_y = 200
obs_w = 10
obs_h = 100
obs_vel = 10

while True:
    img[:] = 255

    # DIBUJAR PELOTA
    cv.circle(img, (pos_x, pos_y), radio, (0, 0, 255), -1)

    # BARRA
    cv.rectangle(
        img,
        (obs_x, obs_y),
        (obs_x + obs_w, obs_y + obs_h),
        (0, 0, 0),
        -1
    )

    #DISTANCIA EUCLIDIANA
    centro_obs_y = obs_y + obs_h // 2
    distancia = math.sqrt((pos_x - obs_x) ** 2 + (pos_y - centro_obs_y) ** 2)

    # BARRA SIGUE A LA PELOTA
    if distancia < 320:
        if pos_y < centro_obs_y:
            obs_y -= obs_vel
        elif pos_y > centro_obs_y:
            obs_y += obs_vel


    obs_y = max(0, min(obs_y, img.shape[0] - obs_h))

    #ACTUALIZAR PELOTA
    pos_x += vel_x
    pos_y += vel_y

    #REBOTE EN BORDES
    if pos_x - radio <= 0 or pos_x + radio >= img.shape[1]:
        vel_x = -vel_x
    if pos_y - radio <= 0 or pos_y + radio >= img.shape[0]:
        vel_y = -vel_y

    #REBOTE
    if (obs_x <= pos_x + radio <= obs_x + obs_w and
        obs_y <= pos_y <= obs_y + obs_h):
        vel_x = -vel_x  # rebote horizontal

    cv.imshow("Pong con obstaculo que sigue a la pelota", img)
    if cv.waitKey(30) == 27:
        break

cv.destroyAllWindows()