import serial               #import serial pacakge
from time import sleep
import webbrowser           #import package for opening link in browser
import sys #import system package
import RPi.GPIO as GPIO
import serial
import time
#from sim800l import SIM800L
import time
import pyttsx3
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
in1=26
GPIO.setup(in1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO_TRIGGER_Right = 27
GPIO_ECHO_Right = 22
GPIO_TRIGGER_Left = 5
GPIO_ECHO_Left = 6
vibrator = 12
engine=pyttsx3.init()

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_Right, GPIO.OUT)
GPIO.setup(GPIO_ECHO_Right, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_Left, GPIO.OUT)
GPIO.setup(GPIO_ECHO_Left, GPIO.IN)
GPIO.setup(vibrator, GPIO.OUT)

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
def distanceRight():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER_Right, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_Right, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO_Right) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO_Right) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance_Right = (TimeElapsed * 34300) / 2
 
    return distance_Right

def distanceLeft():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER_Left, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_Left, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO_Left) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO_Left) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance_Left = (TimeElapsed * 34300) / 2
 
    return distance_Left

def GPS_Info():
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
    nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
    
    print("NMEA Time: ", nmea_time,'\n')
    print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
    
    lat = float(nmea_latitude)                  #convert string into float for calculation
    longi = float(nmea_longitude)               #convertr string into float for calculation
    
    lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
    long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format
    
#convert raw NMEA string into degree decimal format   
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position
    
def divi():
    import requests

    url = "https://www.fast2sms.com/dev/bulkV2"
    


    querystring = {"authorization":"ZGIflw3HAkc42MVNWrgbqvReOs091mx8DBKJ5CTz7htLXYijnpyf8de72sq5AWaM0HFo6uQKxPcbRzTj","sender_id":"FSTSMS","message":map_link,"variables_values":"12345|asdaswdx","route":"p","numbers":"9791652002"}

    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    
    # print the send message
    #print(returned_msg['message'])

gpgga_info = "$GPGGA,"
ser = serial.Serial ("/dev/ttyS0")              #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0

try:
    while True:
        if GPIO.input(in1)==0:
            value=GPIO.input(in1)
            print(value)
            received_data = (str)(ser.readline())                   #read NMEA string received
            GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                 
            if (GPGGA_data_available>0):
                GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
                NMEA_buff = (GPGGA_buffer.split(','))
                print(type(NMEA_buff))#store comma separated data in buffer
                GPS_Info()                                          #get time, latitude, longitude
     
                print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, '\n')
                map_link = 'http://maps.google.com/?q=' + lat_in_degrees + ',' + long_in_degrees    #create link to plot location on Google map
                print("<<<<<<<<press ctrl+c to plot location on google maps>>>>>>\n")               #press ctrl+c to plot on map and exit 
                print("------------------------------------------------------------\n")
                divi()
        else:
            dist = distance()
            distright= distanceRight()
            distleft= distanceLeft()
            print ("Measured Distance = %.1f cm" % dist)
            print ("Measured Distanceright = %.1f cm" % distright)
            print ("Measured Distanceright = %.1f cm" % distleft)
            
            if(dist<40):
                GPIO.output(vibrator,GPIO.HIGH)
                print("object detected")
                engine.say("object detected")
                engine.runAndWait()
            if(distright<40):
                GPIO.output(vibrator,GPIO.HIGH)
                print("object detected")
                engine.say("object detected")
                engine.runAndWait()
            if(distleft<40):
                GPIO.output(vibrator,GPIO.HIGH)
                print("object detected")
                engine.say("object detected")
                engine.runAndWait()
            GPIO.output(vibrator,GPIO.LOW)
            
            #sim800l.setup()
            #time.sleep(1)
                            
except KeyboardInterrupt:
    divi()
    webbrowser.open(map_link)        #open current position information in google map
    sys.exit(0)
