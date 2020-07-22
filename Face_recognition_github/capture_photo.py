# Webcamden foto almak için yazılmıştır.

import cv2
import keyboard
import time

vco = cv2.VideoCapture(0)
result = True

while(result):
	ret, frame = vco.read()
	cv2.imwrite("Captured.jpg", frame)

	if keyboard.is_pressed("p"):
		print("bitti")
		result = False

vco.release()
cv2.destroyAllWindows()


