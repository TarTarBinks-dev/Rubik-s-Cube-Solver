import cv2
import numpy as np
from picamera import PiCamera
from PIL import Image
import RPi.GPIO as GPIO
from time import sleep

DIR = 20
STEP = 21
DIR3 = 19
STEP3 = 26
DIR2 = 13
STEP2 = 6
DIR4 = 
STEP4 = 

CW = 1
CCW = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR3, GPIO.OUT)
GPIO.setup(STEP3, GPIO.OUT)
GPIO.setup(DIR2, GPIO.OUT)
GPIO.setup(STEP2, GPIO.OUT)
GPIO.setup(DIR4, GPIO.OUT)
GPIO.setup(STEP4, GPIO.OUT)

delay = .0108
# delay = .0208

GPIO.setwarnings(False)
      
#camera setup
camera = PiCamera()
#Res must be divisible by 3
res = 720
camera.resolution = (res, res)

faceColors = ["pink", "pink", "pink", "pink", "pink", "pink", "pink", "pink", "pink"]

#Solved cube corners for reference
AQN = ["yellow", "blue", "orange"]
BJM = ["yellow", "green", "orange"]
DRE = ["yellow", "blue", "red"]
CFI = ["yellow", "red", "green"]
HSU = ["red", "blue", "white"]
GLV = ["red", "green", "white"]
XTO = ["white", "blue", "orange"]
WKP = ["white", "green", "orange"]

def Xturn():
    GPIO.output(DIR, CW)
    GPIO.output(DIR3, CW)
    for x in range(200):
        GPIO.output(STEP, GPIO.HIGH)
        GPIO.output(STEP3, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        GPIO.output(STEP3, GPIO.LOW)
        sleep(delay)

def Xprimeturn():
    GPIO.output(DIR, CCW)
    GPIO.output(DIR3, CCW)
    for x in range(200):
        GPIO.output(STEP, GPIO.HIGH)
        GPIO.output(STEP3, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        GPIO.output(STEP3, GPIO.LOW)
        sleep(delay)

def Yturn():
    GPIO.output(DIR2, CW)
    GPIO.output(DIR4, CW)
    for x in range(200):
        GPIO.output(STEP2, GPIO.HIGH)
        GPIO.output(STEP4, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP2, GPIO.LOW)
        GPIO.output(STEP4, GPIO.LOW)
        sleep(delay)       

def Yprimeturn():
    GPIO.output(DIR2, CCW)
    GPIO.output(DIR4, CCW)
    for x in range(200):
        GPIO.output(STEP2, GPIO.HIGH)
        GPIO.output(STEP4, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP2, GPIO.LOW)
        GPIO.output(STEP4, GPIO.LOW)
        sleep(delay)

def colorfinder():
    counter = 1
    #faceColors = ["pink", "pink", "pink", "pink", "pink", "pink", "pink", "pink", "pink"]
    camera.capture("/home/pi/Desktop/cube.jpg")
    while counter <= 9:
        
        
        im = Image.open("/home/pi/Desktop/cube.jpg")
        
        
        if counter == 1:
            im_crop = im.crop((80, 80, (res/3)-80, (res/3)-80))
        if counter == 2:
             im_crop = im.crop(((res/3)+80, 80, (res/3) + (res/3)-80, (res/3)-80))
        if counter == 3:
             im_crop = im.crop(((res/3) + (res/3) + 80, 80, res-80, (res/3)-80))
        if counter == 4:
             im_crop = im.crop((80, (res/3)+80, (res/3)-80, (res/3) + (res/3) - 80))
        if counter == 5:
             im_crop = im.crop(((res/3)+80, (res/3)+80, (res/3) + (res/3) - 80, (res/3) + (res/3)-80))
        if counter == 6:
             im_crop = im.crop(((res/3) + (res/3) + 80, (res/3) + 80, (res/3) + (res/3) + (res/3) -80, (res/3) + (res/3) - 80))
        if counter == 7:
             im_crop = im.crop((80, (res/3) + (res/3) + 80, (res/3) - 80, res - 80))
        if counter == 8:
             im_crop = im.crop(((res/3) + 80, (res/3) + (res/3) + 80, (res/3) + (res/3) - 80, res - 80))
        if counter == 9:
             im_crop = im.crop(((res/3) + (res/3) + 80, (res/3) + (res/3) + 80, res - 80, res - 80))
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
        low_yellow = np.array([23, 108, 90])
        high_yellow = np.array([40, 255, 255])
        yellow_mask = cv2.inRange(hsv_img, low_yellow, high_yellow)
        contours2, _ = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours2 = sorted(contours2, key=lambda x:cv2.contourArea(x), reverse=True)
         
        for cnt in contours2:
            area2 = cv2.contourArea(cnt)
            if area2 > 5000:
                faceColors[counter-1] = "yellow"
        
        #blue color
        low_blue = np.array([106, 239, 215])
        high_blue = np.array([128, 255, 255])
        blue_mask = cv2.inRange(hsv_img, low_blue, high_blue)
        contours3, _ = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours3 = sorted(contours3, key=lambda x:cv2.contourArea(x), reverse=True)
         
        for cnt in contours3:
            area3 = cv2.contourArea(cnt)
            if area3 > 5000:
                faceColors[counter-1] = "blue"
                
        #green color
        low_green = np.array([36, 171, 159])
        high_green = np.array([71, 255, 255])
        green_mask = cv2.inRange(hsv_img, low_green, high_green)
        contours4, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours4 = sorted(contours4, key=lambda x:cv2.contourArea(x), reverse=True)
         
        for cnt in contours4:
            area4 = cv2.contourArea(cnt)
            if area4 > 5000:
               faceColors[counter-1] = "green"
                
        #Orange color
        low_orange = np.array([0, 167, 112])
        high_orange = np.array([10, 255, 255])
        orange_mask = cv2.inRange(hsv_img, low_orange, high_orange)
        contours5, _ = cv2.findContours(orange_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours5 = sorted(contours5, key=lambda x:cv2.contourArea(x), reverse=True)
         
        for cnt in contours5:
            area5 = cv2.contourArea(cnt)
            if area5 > 5000:
               faceColors[counter-1] = "orange"
        
        
#         #White color
#         low_white = np.array([110, 100, 100])
#         high_white = np.array([130, 255, 255])
#         white_mask = cv2.inRange(hsv_img, low_white, high_white)
#         contours6, _ = cv2.findContours(white_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#         contours6 = sorted(contours6, key=lambda x:cv2.contourArea(x), reverse=True)
#          
#         for cnt in contours6:
#             area6 = cv2.contourArea(cnt)
#             if area6 > 5000:
        if faceColors[counter-1]=="pink":
            
            faceColors[counter-1] = "white"
                
        
        counter+=1
                
        #cv2.imshow("Frame", img)
#         cv2.imshow("RedMask", red_mask)
#         cv2.imshow("YellowMask", yellow_mask)
#         cv2.imshow("GreenMask", green_mask)
#         cv2.imshow("BlueMask", blue_mask)
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
    Xturn()
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
    Xturn()
    colorfinder()
    whiteFace = faceColors
    U = whiteFace[0]
    u = whiteFace[1]
    V = whiteFace[2]
    x = whiteFace[3]
    down = whiteFace[4]
    v = whiteFace[5]
    X = whiteFace[6]
    w = whiteFace[7]
    W = whiteFace[8]
    Xturn()
    colorfinder()
    orangeFace = faceColors
    O = orangeFace[0]
    o = orangeFace[1]
    P = orangeFace[2]
    n = orangeFace[3]
    back = orangeFace[4]
    p = orangeFace[5]
    N = orangeFace[6]
    m = orangeFace[7]
    M = orangeFace[8]
    Yturn()
    colorfinder()
    blueFace = faceColors
    S = blueFace[0]
    s = blueFace[1]
    T = blueFace[2]
    r = blueFace[3]
    left = blueFace[4]
    t = blueFace[5]
    R = blueFace[6]
    q = blueFace[7]
    Q = blueFace[8]
    Yturn()
    Yturn()
    colorfinder()
    greenFace = faceColors
    K = greenFace[0]
    k = greenFace[1]
    L = greenFace[2]
    j = greenFace[3]
    right = greenFace[4]
    l = greenFace[5]
    J = greenFace[6]
    i = greenFace[7]
    I = greenFace[8]

def cornerAssigner():
    mAQN = [A, Q, N]
    mBJM = [B, J, M]
    mDRE = [D, R, E]
    mCFI = [C, F, I]
    mHSU = [H, S, U]
    mGLV = [G, L, V]
    mXTO = [X, T, O]
    mWKP = [W, K, P]

#Pass in any corner, it will do the algo to get that specific corner to where it should go.
def cornerSorter(Corner):
    coner.sort()
    AQN.sort()
    if (corner == AQN){
        #get one of the letters of one of the colors of the corner EX: A
    }
#use "list".sort() method for comparing the two corners.








