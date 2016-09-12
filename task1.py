import cv2
import numpy as np
from matplotlib import pyplot as plt
def nothing(e):
	pass
th=0
cap = cv2.VideoCapture(0)
#cv2.namedWindow('edges')
#cv2.createTrackbar('th','edges',0,255,nothing)
#cv2.createTrackbar('t','edges',0,255,nothing)
kernel = np.ones((5,5),np.uint8)

while(cap.isOpened()):
	#img = cv2.imread('gazebo.jpg')
	rgb=[]
	x=[]
	y=[]
	ret,img=cap.read()
	
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	lower = np.array([0,0,255],np.uint16)
    	upper = np.array([180,255,255],np.uint16) 
	mask2 = cv2.inRange(hsv,lower, upper) #masking high intensity regions
	dilation = cv2.dilate(mask2,kernel,iterations = 10) # to remove coarseness in image
	# using contours to find position and RGB value of each light
	_,contours0, hierarchy0 = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	for i in range(len(contours0)):
		cnt=contours0[i]
		hie=hierarchy0[0,i]
		M = cv2.moments(cnt)
		cx = int(M['m10']/M['m00'])
 		cy = int(M['m01']/M['m00'])
		x.append(cx)
		y.append(cy)
		rgb.append(img[cy,cx])
	
	print " x coordinates of each light source"
	print x
	print "y coordiante of each source"
	print y
	print "RGB values of each source"
	print rgb
	mask2 = cv2.bitwise_not(mask2)
	img2 = cv2.bitwise_and(img,img,mask=dilation)
	#th = cv2.getTrackbarPos('th','edges')
	#t = cv2.getTrackbarPos('t','edges')
	cv2.imshow("image",img)
	cv2.imshow("maskedimage",img2)
	#cv2.waitKey(0)
	#break
	if cv2.waitKey(3)==ord('q'):
		break

cap.release() 
cv2.destroyAllWindows()
