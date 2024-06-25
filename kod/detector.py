from imageai.Detection import ObjectDetection
import os , firebaseDbLib ,time
import cv2
from datetime import datetime
kamera = cv2.VideoCapture(0)
execution_path = os.getcwd()
detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "retinanet_resnet50_fpn_coco-eeacb38b.pth"))
detector.loadModel()
while True:

    ret, frame = kamera.read()

    cv2.imwrite(os.path.join("/tmp","tmp.jpg"),frame)
    detections = detector.detectObjectsFromImage(input_image=os.path.join("/tmp","tmp.jpg"), output_image_path=os.path.join("/tmp", "imagenew.jpg"))
    os.remove(os.path.join("/tmp","tmp.jpg"))
    tmpImagePath = os.path.join("/tmp","imagenew.jpg")
    for eachObject in detections:
        print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
        if eachObject["name"] == "cell phone" and eachObject["percentage_probability"] > 45:
            firebaseDbLib.algilanmaArttir()
            unix_timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
            a = firebaseDbLib.plaka + " " + str(unix_timestamp)
            firebaseDbLib.upload_file(a)
            print("telefon algılandı")
            time.sleep(15)
    os.remove(tmpImagePath)
kamera.release()