import os
import cv2
import numpy as np

BASE_DIR = os.path.dirname(__file__)
cascade_file_location = os.path.join(BASE_DIR,"frontal_face.xml")

#checking file
def file_check(s):
    l=["png","jpg","jpeg"]
    s2=s.split('.')[-1]
    if s2 in l:
        return True
    else:
        return False
def erode(img):
    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(img,kernel,iterations = 1)
    return erosion

def dilate(img):
    kernel = np.ones((5,5),np.uint8)
    dilation = cv2.dilate(img,kernel,iterations = 1)
    return dilation
def openimg(img):
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    return opening
def closeimg(img):
    kernel = np.ones((5,5),np.uint8)
    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return closing




#face detection function
def face_detection(test_img):
    gray_img = cv2.cvtColor(test_img,cv2.COLOR_BGR2GRAY)
    face_haar_cascade = cv2.CascadeClassifier(cascade_file_location)
    #image processing


    
    faces = face_haar_cascade.detectMultiScale( gray_img, scaleFactor= 1.2,minNeighbors= 3)
    return faces,gray_img

def labels_for_training_data(directory):
    faces = []
    faceID = []
    count = 1

    for path,subdirnames,filenames in os.walk(directory):

        for filename in filenames:
            if filename.startswith("."):
                continue
            if not file_check(filename):
                continue
            ID = os.path.basename(path)
            img_path = os.path.join(path,filename)
            test_img = cv2.imread(img_path)
            if test_img is None:
                print("Image not loaded properly:",img_path)
                continue
            faces_rect,gray_img = face_detection(test_img)
            if len(faces_rect)!= 1:
                
                print("Face not recognized NORMALLY",filename,count)
            #image prosessing operations : dilation, erosion, opening, closing.
                dimg = dilate(test_img)
                faces_rect,gray_img = face_detection(dimg)
                if len(faces_rect)!= 1:
                    print("Face not recognized after dilation",filename,count)
                    oimg = openimg(test_img)
                    faces_rect,gray_img = face_detection(oimg)
                    if len(faces_rect)!= 1:
                        print("Face not recognized after opening",filename,count)
                        cimg = closeimg(test_img)
                        faces_rect,gray_img = face_detection(cimg)
                        if len(faces_rect)!= 1:
                            print("Face not recognized after closing",filename,count)
                            eimg = erode(test_img)
                            faces_rect,gray_img = face_detection(eimg)
                            if len(faces_rect)!= 1:
                                print("Face not recognized after erosion",filename,count)

                                count+= 1
                                continue #Skipping images with more  than 1 face detected in the training data
                


                # for testing purpose , do not required for the exeqution.
                #             else:
                #                 draw_rect(test_img,faces_rect[0])
                #                 cv2.imshow("erosion",test_img)
                #         else:
                #             draw_rect(test_img,faces_rect[0])
                #             cv2.imshow("closing",test_img)
                #     else:
                #         draw_rect(test_img,faces_rect[0])
                #         cv2.imshow("opening",test_img)
                # else:
                #     draw_rect(test_img,faces_rect[0])
                #     cv2.imshow("dilation",test_img)
            
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






