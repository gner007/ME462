# Webcamden gelen fotoları kontrol ederek kameradaki kişileri söyler.

import face_function as ft 
import time
import keyboard

flag=True
while(flag):
	try:
		start= time.time()
		names, boxes = ft.find_them("Captured.jpg")
		end = time.time()
		print(names)
		print(end-start)

		if keyboard.is_pressed("q"):
			print("bitti")
			flag = False
	except:
		print("SORUNN")
		continue

