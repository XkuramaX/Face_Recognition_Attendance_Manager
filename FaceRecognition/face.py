import os
import cv2
import numpy as np

#face detection function
def face_detection(test_img):
    gray_img = cv2.cvtColor(test_img,cv2.COLOR_BGR2GRAY)
    face_haar_cascade = cv2.CascadeClassifier('D:/Akash Chatterjee/Final Year Project/FaceRecognition/haar_face.xml')
    #image processing


    
    faces = face_haar_cascade.detectMultiScale(gray_img,scaleFactor=1.3,minNeighbors=5)
    return faces,gray_img

def labels_for_training_data(directory):
    faces = []
    faceID = []

    for path,subdirnames,filenames in os.walk(directory):
        for filename in filenames:
            if filename.startswith("."):
                continue
            ID = os.path.basename(path)
            img_path = os.path.join(path,filename)
            test_img = cv2.imread(img_path)
            if test_img is None:
                print("Image not loaded properly:",img_path)
                continue
            faces_rect,gray_img = face_detection(test_img)
            if len(faces_rect)!=1:
                print("Face not recognized or more than 1 face")
                continue #Skipping images with more  than 1 face detected in the training data
            (x,y,w,h) = faces_rect[0]
            #extracting only the face of the person
            roi_gray = gray_img[y:y+h,x:x+w]
            faces.append(roi_gray)
            faceID.append(int(ID))
    return faces,faceID

def train_classifier(faces,faceID):
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces,np.array(faceID))
    return face_recognizer

def draw_rect(test_img,face):
    (x,y,w,h) = face
    cv2.rectangle(test_img,(x,y),(x+w,y+h),(0,0,255),thickness=5)

def put_text(test_img,text,x,y):
    cv2.putText(test_img,text,(x,y),cv2.FONT_HERSHEY_SIMPLEX,5,(0,255,0),6)






