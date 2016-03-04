import numpy as np
import cv2
import time
import serial

DEVICE = '/dev/ttyACM0'
BAUD = 9600
ser = serial.Serial(DEVICE, BAUD)

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480.0)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240.0)
    xr=yr=wr=hr=xb=yb=wb=hb=xg=yg=wg=hg=0
    print 'Red = 1, Blue = 2, Green = 3'
    detectcolor = input('Which color would you like to detect? ')
    
    # define range of blue color in HSV
    lower_blue = np.array([80, 50, 50], dtype=np.uint8)
    upper_blue = np.array([120,255,255], dtype=np.uint8)
    # define range of red color in HSV
    lower_red = np.array([0, 50, 30], dtype=np.uint8)
    upper_red = np.array([8,255,255], dtype=np.uint8)
    # define range of green color in HSV
    lower_green = np.array([40, 50, 50], dtype=np.uint8)
    upper_green = np.array([80,255,255], dtype=np.uint8)
    
    if detectcolor == 1:
        while cv2.waitKey(1) != 27 and cap.isOpened():
            # Capture frame-by-frame
            ret, frame = cap.read()
            # Convert BGR to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # Threshold the HSV image to get only blue colors
            maskred = cv2.inRange(hsv, lower_red, upper_red)
            # Bitwise-AND mask and original image
            resred = cv2.bitwise_and(frame, frame, mask = maskred)
            rgray = cv2.cvtColor(resred,cv2.COLOR_BGR2GRAY)
            # ret,resred1 = cv2.threshold(rgray,40,255,cv2.THRESH_BINARY)    
            (ret,resred1) = cv2.threshold(rgray, 40, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            redboxblurred = cv2.GaussianBlur(resred1, (5, 5), 0)    
            redCanny = cv2.Canny(redboxblurred, 100, 200)
            # To get more solid edges to bind within rectange
            derp,contours,hierarchy = cv2.findContours(redCanny, 1, 2)
            if (len(contours)>1):
                cnt = contours[0]
                xr,yr,wr,hr = cv2.boundingRect(cnt)
                redbox = cv2.rectangle(frame,(xr,yr),(xr+wr,yr+hr),(0,255,0),2)
		cv2.imshow('redbox',redbox)
	    #end-if
            cv2.imshow('Original Frame',frame)
            cv2.imshow('Red Mask',maskred)
            cv2.imshow('Red Canny',redCanny)
            cv2.imshow('Mask Overlay Result Red',resred)
            cv2.imshow('Red Grayscale',rgray)
            cv2.imshow('Binary Threshold Red',resred1)
            #cv2.imshow('Blurred Red Box',redboxblurred)
    	    if ((xr+(wr/2))>245):
               #object on right half of the frame, turn right
               ser.write('0080 0080')
	    elif ((xr+(wr/2))<235) :
               #object on left half of the frame, turn left
               ser.write('1104 1104')
            elif (((xr+(wr/2))>235) & ((xr+(wr/2))<245)):
               #object in the center of the frame, stop motors
   	       ser.write('0000 0000')
	       #time.sleep(2)
            #end-if
          
    elif detectcolor == 2:
        while cv2.waitKey(1) != 27 and cap.isOpened():
            # Capture frame-by-frame
            ret, frame = cap.read()
            # Convert BGR to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # Threshold the HSV image to get only blue colors
            maskblue = cv2.inRange(hsv, lower_blue, upper_blue)
            resblue = cv2.bitwise_and(frame, frame, mask = maskblue)
            bgray = cv2.cvtColor(resblue,cv2.COLOR_BGR2GRAY)
            (ret,resblue1) = cv2.threshold(bgray, 40, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            blueboxblurred = cv2.GaussianBlur(resblue1, (5, 5), 0)          
            blueCanny = cv2.Canny(blueboxblurred, 100, 200)             
            derp,bcontours,hierarchy = cv2.findContours(blueCanny, 1, 2)
            if (len(bcontours)>1):
                bcnt = bcontours[0]
                xb,yb,wb,hb = cv2.boundingRect(bcnt)
                bluebox = cv2.rectangle(frame,(xb,yb),(xb+wb,yb+hb),(0,255,0),2)
		cv2.imshow('bluebox',bluebox)
	    #end-if
            cv2.imshow('Original Frame',frame)
            cv2.imshow('Blue Mask',maskblue)
            cv2.imshow('Blue Canny',blueCanny)
            cv2.imshow('Mask Overlay Result Blue',resblue)
            cv2.imshow('Blue Grayscale',bgray)
            cv2.imshow('Binary Threshold Result',resblue1)
            #cv2.imshow('Blurred Blue Box',blueboxblurred)
 	    if ((xb+(wb/2))<235) :
                ser.write('1104 1104')
            if ((xb+(wb/2))>145) :
                ser.write('0080 0080')
            if (((xb+(wb/2))<145) & ((xb+(wb/2))>135)):
                ser.write('0000 0000')
            #end if
	  #end-if
            
    elif detectcolor == 3:
        while cv2.waitKey(1) != 27 and cap.isOpened():
            # Capture frame-by-frame
            ret, frame = cap.read()
            # Convert BGR to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # Threshold the HSV image to get only blue colors
            maskgreen = cv2.inRange(hsv, lower_green, upper_green)
            resgreen = cv2.bitwise_and(frame, frame, mask = maskgreen)
            ggray = cv2.cvtColor(resgreen,cv2.COLOR_BGR2GRAY)
            (ret,resgreen1) = cv2.threshold(ggray, 40, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            greenboxblurred = cv2.GaussianBlur(resgreen1, (5, 5), 0)    
            greenCanny = cv2.Canny(greenboxblurred, 100, 200)               
            derp,gcontours,hierarchy = cv2.findContours(greenCanny, 1, 2)
            if (len(gcontours)>1):
                gcnt = gcontours[0]
                xg,yg,wg,hg = cv2.boundingRect(gcnt)
                greenbox = cv2.rectangle(frame,(xg,yg),(xg+wg,yg+hg),(0,255,0),2)
		cv2.imshow('bluebox',greenbox)
	    #end-if
            cv2.imshow('Original frame',frame)
            cv2.imshow('Green Mask',maskgreen)
            cv2.imshow('Green Canny',greenCanny)
            cv2.imshow('Mask Overlay Result Green',resgreen)
            cv2.imshow('Green Grayscale',ggray)
            cv2.imshow('Binary Threshold result',resgreen1)
            #cv2.imshow('Blurred Green Box',greenboxblurred)
 	    if ((xg+(wg/2))<235) :
                ser.write('1104 1104')
	    elif ((xg+(wg/2))>245) :
                ser.write('0080 0080')
            elif (((xg+(wg/2))>235) & ((xg+(wg/2))<245)) :
                ser.write('0000 0000')
            #end-if
            
# Stop motors when exiting program
    ser.write('0000 0000')
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

