import cv2
import numpy as np

# Crear una imagen negra
img = np.zeros((500, 500, 3), dtype=np.uint8)

# Dibujar un círculo para simular un rostro
cv2.circle(img, (250, 250), 100, (255, 255, 255), -1)
cv2.circle(img, (200, 200), 20, (0, 0, 0), -1)  # Ojo izquierdo
cv2.circle(img, (300, 200), 20, (0, 0, 0), -1)  # Ojo derecho
cv2.ellipse(img, (250, 300), (50, 30), 0, 0, 180, (0, 0, 0), 5)  # Boca

# Guardar la imagen
cv2.imwrite('face.jpg', img)
print("Imagen de prueba creada: face.jpg") 