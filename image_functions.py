import os
import cv2
import face_recognition as FR
import numpy as np
import voice_functions

LOGOUT_AFTER_SEC = 10 
PATH = "auto_logout_system/images"
unique_ids = []
encodings_known = []

def find_encodings(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encode = FR.face_encodings(img)[0]
    return encode

def load_data():
    """Loads all the saved images to be used by the program"""
    images = os.listdir(PATH)
    for img in images:
        curr_img = FR.load_image_file(PATH+'/'+img)
        unique_ids.append(int(img.split('.')[0]))
        encodings = find_encodings(curr_img)
        encodings_known.append(encodings)

def compare_face(face_encodings):
    matches = FR.compare_faces(encodings_known, face_encodings, 0.6)
    faceDis = FR.face_distance(encodings_known, face_encodings)
    if True not in matches:
        return "Unknown"
    matchIndex = np.argmin(faceDis)
    return(unique_ids[matchIndex])
    
def capture_image():
    cam = cv2.VideoCapture(0)
    success, image = cam.read()
    cv2.imshow("web cam", image)
    cv2.waitKey(1)
    detect_face = FR.face_locations(image)
    if(detect_face):
        return image
    else:
        return None

def update_image(user):
    cv2.imwrite(f"auto_logout_system/images/{user.uniqueId}.jpg", user.image)

def current_status(user):
    curr_image = capture_image()
    if curr_image is not None:
        curr_face_encodings = find_encodings(curr_image)
        if compare_face(curr_face_encodings) == user.uniqueId:
            return True
    return False

def check_presence(window, user):
    if user.is_login:
        if current_status(user) == True:
            user.absence_count = 0
        else:
            user.absence_count += 1

        print(user.absence_count)
        
        if user.absence_count != LOGOUT_AFTER_SEC:
            # window.after(10, check_presence(window, user))  
            pass
        else:
            user.logout_linkedin()
            cv2.destroyAllWindows()
    