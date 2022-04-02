import face_recognition
import numpy as np
import cv2

encodedList = []
for x in ['kalam.jpg', 'jeff.jpeg']:
    img = face_recognition.load_image_file(x)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encd = face_recognition.face_encodings(img)[0]
    encodedList.append(encd)

img = face_recognition.load_image_file('Test.jpeg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
encoed = face_recognition.face_encodings(img)[0]

results = face_recognition.compare_faces(encodedList, encoed)
print(results)
