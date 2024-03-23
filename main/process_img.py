
from scipy.spatial import distance as dist
from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2


#Funcțiile de calcul pentru distanțele 
# dintre reperele buzelor și a ochilor 
# au fost preluate din sursa: https://github.com/Arijit1080/Drowsiness-and-Yawn-Detection-with-voice-alert-using-Dlib

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)

    return ear

def final_ear(shape):
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]

    leftEAR = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)

    ear = (leftEAR + rightEAR) / 2.0
    return (ear, leftEye, rightEye)

def lip_distance(shape):
    top_lip = shape[50:53]
    top_lip = np.concatenate((top_lip, shape[61:64]))

    low_lip = shape[56:59]
    low_lip = np.concatenate((low_lip, shape[65:68]))

    top_mean = np.mean(top_lip, axis=0)
    low_mean = np.mean(low_lip, axis=0)

    distance = abs(top_mean[1] - low_mean[1])
    return distance


def decect_inattention(image):
    result = 0
    EYE_MIN_DISTANCE = 0.3
    MOUTH_MAX_DISTANCE = 20

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('main\shape_predictor_68_face_landmarks.dat')

    image = imutils.resize(image, width=480)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray, 0)

    for face in faces:
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)
        eye = final_ear(shape)
        ear = eye[0]

        distance = lip_distance(shape)
        if ear < EYE_MIN_DISTANCE:
            result = 1

        if (distance > MOUTH_MAX_DISTANCE):
            result = 1
                
    return result
