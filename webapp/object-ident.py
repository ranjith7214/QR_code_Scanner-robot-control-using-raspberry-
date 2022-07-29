import cv2
#from sim800l import SIM800L
#import pyttsx3

#Libraries
import RPi.GPIO as GPIO
import time
from time import sleep
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
buzzer=23
#irsensor=4
relay=27
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(relay,GPIO.OUT)
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
#sim800l=SIM800L('dev/serial0')
#sms="hi"
#destno="7092447008"
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(irsensor,GPIO.IN) 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
#thres = 0.45 # Threshold to detect object

  
# init function to get an engine instance for the speech synthesis 
#engine = pyttsx3.init()


classNames = []
classFile = "/home/pi/Desktop/Object_Detection_Files/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "/home/pi/Desktop/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/home/pi/Desktop/Object_Detection_Files/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    print(len(objects))
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            print()
            #engine.say(className)
            #engine.runAndWait()
            dist=int(distance())
            print(dist)
            if(dist<30):
               # print("hai")
                GPIO.output(buzzer,GPIO.HIGH)
                GPIO.output(relay,GPIO.HIGH)
                print ("Beep")
                sleep(00.00001) 
                #engine.say(className +"is in"+str(dist)+"centimeter")
                #engine.runAndWait()
            else:
                GPIO.output(buzzer,GPIO.LOW)
                GPIO.output(relay,GPIO.LOW)
                print ("No Beep")
                sleep(0.00001)
#             if(GPIO.input(4)):
#                 value=GPIO.input(4)
#                 GPIO.output(relay,GPIO.LOW)
#                 print(value)
#                 print("alive1")
#             
#             else:
#                 value=GPIO.input(4)
#                 print(value)
#                 print("IR sensor detected")
#                 GPIO.output(relay,GPIO.HIGH)
#                 sim800l.send_sms(destno,className+" "+"detected near to your place")
#                 sim800l.setup()
#                 time.sleep(60)
            if className in objects:
                print(className)
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    return img,objectInfo


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)


    while True:
        success, img = cap.read()
        result, objectInfo = getObjects(img,0.45,0.2,objects=["dog","horse","sheep","cow","elephant","bear","zebra","giraffe"])
        #print(objectInfo)
        cv2.imshow("Output",img)
        cv2.waitKey(1)
