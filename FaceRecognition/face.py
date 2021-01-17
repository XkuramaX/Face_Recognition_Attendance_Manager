import os
import cv2
import numpy as np

BASE_DIR = os.path.dirname(__file__)
cascade_file_location = os.path.join(BASE_DIR,"haar_face.xml")

#face detection function
def face_detection(test_img):
    gray_img = cv2.cvtColor(test_img,cv2.COLOR_BGR2GRAY)
    face_haar_cascade = cv2.CascadeClassifier(cascade_file_location)
    #image processing


    
    faces = face_haar_cascade.detectMultiScale(gray_img,scaleFactor=1.2,minNeighbors=5,minSize=(30, 30))
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

def create_model():
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    return face_recognizer

def train_classifier(faces,faceID):
    face_recognizer = create_model()
    face_recognizer.train(faces,np.array(faceID))
    face_recognizer.save('trained_model.yml')
    return face_recognizer


def draw_rect(test_img,face):
    (x,y,w,h) = face
    cv2.rectangle(test_img,(x,y),(x+w,y+h),(0,0,255),thickness=5)

def put_text(test_img,text,x,y):
    cv2.putText(test_img,text,(x,y),cv2.FONT_HERSHEY_SIMPLEX,5,(0,255,0),6)






