import cv2
import os
import numpy as np
import face as fr
import server as app


BASE_DIR = os.path.dirname(__file__)
TRAINING_DIR = os.path.join(BASE_DIR,"training_imgs")
TEST_DIR = os.path.join(BASE_DIR,"test_imgs")
print(BASE_DIR)

test_img = cv2.imread(os.path.join(TEST_DIR,"AkashTest4.jpg"))



try:
    trained_model = os.path.join(os.path.dirname(BASE_DIR),'trained_model.yml')
    print(trained_model)
    face_recognizer = fr.create_model()
    face_recognizer.read(trained_model)
except Exception:
    print("Training the model")
    faces,faceID = fr.labels_for_training_data(TRAINING_DIR)

    face_recognizer = fr.train_classifier(faces,faceID)

name = {1:"Obama",2:"Akash",5:"Amarty",6:"Ben",4:"sashi",3:"kalam"}


faces_detected,gray_img = fr.face_detection(test_img)

print(len(faces_detected))



for face in faces_detected:
    (x,y,w,h) = face
    roi_gray = gray_img[y:y+h,x:x+w]
    label, confidence = face_recognizer.predict(roi_gray) #confidence value 0 means exact match
    print("confidence:",confidence,"label:",label)
    fr.draw_rect(test_img,face)
    resp = app.give_attendance(label)
    print(resp)
    fr.put_text(test_img,x,y)

resized_img = cv2.resize(test_img,(1000,700))
cv2.imshow("faces",resized_img)
cv2.waitKey(0)
cv2.destroyAllWindows()