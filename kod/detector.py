from imageai.Detection import ObjectDetection
import os, firebaseDbLib, time, io, cv2, serial
from datetime import datetime



portwrite = "/dev/ttyUSB2"
port = "/dev/ttyUSB1"

is_raspberry_pi = os.uname().nodename == "teknofestPi"
if is_raspberry_pi:
    #print("Connecting Port..")
    #try:
    #    serw = serial.Serial(portwrite, baudrate = 115200, timeout = 1,rtscts=True, dsrdtr=True)
    #    serw.write('AT+QGPS=1\r'.encode())
    #    serw.close()
    #    time.sleep(1)
    #except Exception as e: 
    #    print("Serial port connection failed.")
    #    print(e)
    from picamera2 import Picamera2
    picam2 = Picamera2()
    picam2.start()
else:
    kamera = cv2.VideoCapture(0)


execution_path = os.getcwd()
detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "retinanet_resnet50_fpn_coco-eeacb38b.pth"))
detector.loadModel()

ser = serial.Serial(port, baudrate = 115200, timeout = 0.5,rtscts=True, dsrdtr=True)



#GPS part
#def parseGPS(data):
#    print(data, end='') #prints raw data
#    if data[0:6] == "$GPRMC":
#        sdata = data.split(",")
#        if sdata[2] == 'V':
#            print("\nNo satellite data available.\n")
#            return
#        print("-----Parsing GPRMC-----")
#        time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
#        lat = decode(sdata[3]) #latitude
#        dirLat = sdata[4]      #latitude direction N/S
#        lon = decode(sdata[5]) #longitute
#        dirLon = sdata[6]      #longitude direction E/W
#        speed = sdata[7]       #Speed in knots
#        trCourse = sdata[8]    #True course
#        date = sdata[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6] #date
#        variation = sdata[10]  #variation
#        degreeChecksum = sdata[13] #Checksum
#        dc = degreeChecksum.split("*")
#        degree = dc[0]        #degree
#        checksum = dc[1]      #checksum
#
#        latitude = lat.split() # parsing latitude
#        longitute = lon.split() # parsing longitute
#
#        print("\nLatitude: " + str(int(latitude[0]) + (float(latitude[2])/60)) + dirLat) 
#
#        print("Longitute: " + str(int(longitute[0]) + (float(longitute[2])/60)) + dirLon)
#
#        print("time : %s, latitude : %s(%s), longitude : %s(%s), speed : %s,True Course : %s, Date : %s, Magnetic Variation : %s(%s),Checksum : %s "%   (time,lat,dirLat,lon,dirLon,speed,trCourse,date,variation,degree,checksum))
#
#        firebaseDbLib.update_gps_data()

  
#def decode(coord):
#    #Converts DDDMM.MMMMM -> DD deg MM.MMMMM min
#    x = coord.split(".")
#    head = x[0]
#    tail = x[1]
#    deg = head[0:-2]
#    min = head[-2:]
#    return deg + " deg " + min + "." + tail + " min"


#AI part

while True:

    if is_raspberry_pi:

        data = ser.readline().decode('utf-8')
        #if(firebaseDbLib.gpsEnabled == True):
            #parseGPS(data)

        frame = picam2.capture_image("main")
        image, detections = detector.detectObjectsFromImage(input_image=frame, output_type="array")

    else:
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





