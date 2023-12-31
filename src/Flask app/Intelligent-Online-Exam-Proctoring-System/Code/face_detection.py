
import cv2
import numpy as np

def get_face_detector(modelFile=None,
                      configFile=None,
                      quantized=False):

    if quantized:
        if modelFile == None:
            modelFile = r'C:/wamp64/www/WebApp1/Flask app/Intelligent-Online-Exam-Proctoring-System/Code/models/opencv_face_detector_uint8.pb'#'E:/trial/Flask app/Intelligent-Online-Exam-Proctoring-System/Code/models/opencv_face_detector_uint8.pb'                         
        if configFile == None:
            configFile = r'C:/wamp64/www/WebApp1/Flask app/Intelligent-Online-Exam-Proctoring-System/Code/models/opencv_face_detector.pbtxt'
        model = cv2.dnn.readNetFromTensorflow(modelFile, configFile)
                                                                                                                                    #give the raw path for the appropriate file where is located
    else:
        if modelFile == None:
            modelFile = r'C:/wamp64/www/WebApp1/Flask app/Intelligent-Online-Exam-Proctoring-System/Code/models/res10_300x300_ssd_iter_140000.caffemodel'
        if configFile == None:
            configFile = r'C:/wamp64/www/WebApp1/Flask app/Intelligent-Online-Exam-Proctoring-System/Code/models/deploy.prototxt'
        model = cv2.dnn.readNetFromCaffe(configFile, modelFile)
    return model

def find_faces(img, model):
   
    h, w = img.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0,
	(300, 300), (104.0, 177.0, 123.0))
    model.setInput(blob)
    res = model.forward()
    faces = []
    for i in range(res.shape[2]):
        confidence = res[0, 0, i, 2]
        if confidence > 0.5:
            box = res[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x, y, x1, y1) = box.astype("int")
            faces.append([x, y, x1, y1])
    return faces

def draw_faces(img, faces):
    for x, y, x1, y1 in faces:
        cv2.rectangle(img, (x, y), (x1, y1), (0, 0, 255), 3)
        