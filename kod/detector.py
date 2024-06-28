from imageai.Detection import ObjectDetection
import os, firebaseDbLib, time, io, cv2
from datetime import datetime
kamera = cv2.VideoCapture(0)
execution_path = os.getcwd()
detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "retinanet_resnet50_fpn_coco-eeacb38b.pth"))
detector.loadModel()
while True:

    ret, frame = kamera.read()
    image, detections = detector.detectObjectsFromImage(input_image=frame, output_type="array")
    for eachObject in detections:
        print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
        if eachObject["name"] == "cell phone" and eachObject["percentage_probability"] > 45:
            firebaseDbLib.algilanmaArttir()
            unix_timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
            is_success, buffer = cv2.imencode(".jpg", image)
            data = io.BytesIO(buffer)
            a = firebaseDbLib.plaka + " " + str(unix_timestamp) + ".jpeg"
            firebaseDbLib.upload_file(a,data)
            print("telefon algılandı")
            time.sleep(15)
kamera.release()