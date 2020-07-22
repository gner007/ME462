
import face_recognition
import argparse
import pickle
import cv2
import time

start = time.time()
print("Loading Encodings")
data = pickle.loads(open("model_rev.pickle", "rb").read())


image = cv2.imread("test2.jpeg")
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

print("Face Detection using HoG")
boxes = face_recognition.face_locations(rgb, model="hog")

end1 = time.time()

detection_time = end1-start
print(detection_time)

print("Let's encode faces")
encodings = face_recognition.face_encodings(rgb, boxes)

names = []

for encoding in encodings:
	matches = face_recognition.compare_faces(data["encodings"], encoding)

	name = "Unknown"
	counts = {"Mehmet":0,"Omer":0}
	flag = False
	marker=0

	for match in matches:
		
		if match == True:

			name = data["names"][marker]
			counts[name] = counts.get(name) + 1
			flag = True

		marker+=1


	if flag:
		name = max(counts, key=counts.get)

	names.append(name)


for ((top, right, bottom, left), name) in zip(boxes, names):
	# draw the predicted face name on the image
	cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
	y = top - 15 if top - 15 > 15 else top + 15
	cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

end2 = time.time()
process_time = end2-start
print(process_time)

cv2.imshow("Image", image)
cv2.waitKey(0)
