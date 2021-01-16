import cv2
import os
import numpy as np
import face as fr

test_img = cv2.imread('D:/Akash Chatterjee/Final Year Project/FaceRecognition/test_imgs/Obama_test2.jpg')

BASE_DIR = os.path.dirname(__file__)
TRAINING_DIR = os.path.join(BASE_DIR,"training_imgs")


faces,faceID = fr.labels_for_training_data(TRAINING_DIR)

face_recognizer = fr.train_classifier(faces,faceID)
name = {1:"Obama",2:"Akash"}


faces_detected,gray_img = fr.face_detection(test_img)



for face in faces_detected:
    (x,y,w,h) = face
    roi_gray = gray_img[y:y+h,x:x+w]
    label, confidence = face_recognizer.predict(roi_gray) #confidence value 0 means exact match
    print("confidence:",confidence,"label:",label)
    fr.draw_rect(test_img,face)
    predicted_name = name[label]
    fr.put_text(test_img,predicted_name,x,y)

resized_img = cv2.resize(test_img,(1000,700))
cv2.imshow("faces",resized_img)
cv2.waitKey(0)
cv2.destroyAllWindows()