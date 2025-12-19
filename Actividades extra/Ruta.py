import cv2 as cv
import os

print("Ruta de cascadas:", cv.data.haarcascades)
print("\nArchivos disponibles:")
for archivo in os.listdir(cv.data.haarcascades):
    if archivo.endswith('.xml'):
        print(f"  - {archivo}")