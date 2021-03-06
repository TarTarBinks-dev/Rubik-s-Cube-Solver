import cv2
import numpy as np
from picamera import PiCamera
from PIL import Image
import RPi.GPIO as GPIO
import time

##Yellow face starts facing up/ towards camera


#Motor setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ControlPin = [10,9,11,25]

for pin in ControlPin:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,0)
#clockwise
Seq = [ [1,0,0,1],
        [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1] ]
#counter clockwise
SeqC = [ [0,0,0,1],
         [0,0,1,1],
         [0,0,1,0],
         [0,1,1,0],
         [0,1,0,0],
         [0,1,0,0],
         [1,1,0,0],
         [1,0,0,0],
         [1,0,0,1] ]
#camera setup
camera = PiCamera()
#Res must be divisible by 3
res = 720
camera.resolution = (res, res)

def Yturn():
    for i in range(128):
    #512 is one revolution
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(ControlPin[pin], Seq[halfstep][pin])
            time.sleep(0.001)
            
def Yprimeturn():
    for i in range(128):
    #512 is one revolution
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(ControlPin[pin], SeqC[halfstep][pin])
            time.sleep(0.001)

def colorfinder():
    counter = 1
    faceColors = ["pink", "pink", "pink", "pink", "pink", "pink", "pink", "pink", "pink"]
    camera.capture("/home/pi/Desktop/cube.jpg")
    while counter <= 9:
        
        
        im = Image.open("/home/pi/Desktop/cube.jpg")
        
        
        if counter == 1:
            im_crop = im.crop((0, 0, res/3, res/3))
        if counter == 2:
             im_crop = im.crop((res/3, 0, (res/3) + (res/3), res/3))
        if counter == 3:
             im_crop = im.crop(((res/3) + (res/3), 0, res, res/3))
        if counter == 4:
             im_crop = im.crop((0, res/3, res/3, (res/3) + (res/3)))
        if counter == 5:
             im_crop = im.crop((res/3, res/3, (res/3) + (res/3), (res/3) + (res/3)))
        if counter == 6:
             im_crop = im.crop(((res/3) + (res/3), res/3, (res/3) + (res/3) + (res/3), (res/3) + (res/3)))
        if counter == 7:
             im_crop = im.crop((0, (res/3) + (res/3), res/3, res))
        if counter == 8:
             im_crop = im.crop((res/3, (res/3) + (res/3), (res/3) + (res/3), res))
        if counter == 9:
             im_crop = im.crop(((res/3) + (res/3), (res/3) + (res/3), res, res))
        im_crop.save("/home/pi/Desktop/cubecropped.jpg")
        img = cv2.imread("/home/pi/Desktop/cubecropped.jpg")
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
        # store in array
        
        #red color
        low_red = np.array([151, 155, 84])
        high_red = np.array([179, 255, 255])
        red_mask = cv2.inRange(hsv_img, low_red, high_red)
        contours1, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours1 = sorted(contours1, key=lambda x:cv2.contourArea(x), reverse=True)
            
        for cnt in contours1:
            area1 = cv2.contourArea(cnt)
            if area1 > 5000:
                faceColors[counter-1] = "red"

        
        #yellow color
        low_yellow = np.array([25, 70, 120])
        high_yellow = np.array([30, 255, 255])
        yellow_mask = cv2.inRange(hsv_img, low_yellow, high_yellow)
        contours2, _ = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours2 = sorted(contours2, key=lambda x:cv2.contourArea(x), reverse=True)
         
        for cnt in contours2:
            area2 = cv2.contourArea(cnt)
            if area2 > 5000:
                faceColors[counter-1] = "yellow"
        
        #blue color
        low_blue = np.array([90, 60, 0])
        high_blue = np.array([121, 255, 255])
        blue_mask = cv2.inRange(hsv_img, low_blue, high_blue)
        contours3, _ = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours3 = sorted(contours3, key=lambda x:cv2.contourArea(x), reverse=True)
         
        for cnt in contours3:
            area3 = cv2.contourArea(cnt)
            if area3 > 5000:
                faceColors[counter-1] = "blue"
                
        #green color
        low_green = np.array([40, 70, 80])
        high_green = np.array([70, 255, 255])
        green_mask = cv2.inRange(hsv_img, low_green, high_green)
        contours4, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours4 = sorted(contours4, key=lambda x:cv2.contourArea(x), reverse=True)
         
        for cnt in contours4:
            area4 = cv2.contourArea(cnt)
            if area4 > 5000:
               faceColors[counter-1] = "green"
                
                
        counter+=1
                
        cv2.imshow("Frame", img)
        cv2.imshow("RedMask", red_mask)
        cv2.imshow("YellowMask", yellow_mask)
        cv2.imshow("GreenMask", green_mask)
        cv2.imshow("BlueMask", blue_mask)
        key =cv2.waitKey(1)
        
        if key== 27:
            break
    
def mainCubeChecker():
    colorfinder()
    yellowFace = faceColors
    A = yellowFace[0]
    a = yellowFace[1]
    B = yellowFace[2]
    d = yellowFace[3]
    up = yellowFace[4]
    b = yellowFace[5]
    D = yellowFace[6]
    c = yellowFace[7]
    C = yellowFace[8]
    #print(yellowFace)
    #rotate Cube to Red side
    colorfinder()
    redFace = faceColors
    E = redFace[0]
    e = redFace[1]
    F = redFace[2]
    h = redFace[3]
    front = redFace[4]
    f = redFace[5]
    H = redFace[6]
    g = redFace[7]
    G = redFace[8]
    colorfinder()
    redFace = faceColors
    E = redFace[0]
    e = redFace[1]
    F = redFace[2]
    h = redFace[3]
    front = redFace[4]
    f = redFace[5]
    H = redFace[6]
    g = redFace[7]
    G = redFace[8]
#mainCubeChecker()
