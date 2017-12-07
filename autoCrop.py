import numpy as np
import cv2
import glob,os

def splitImage(fileName):
	repeat=1
	white=0
	count=0
	while(repeat==1):
		im=cv2.imread(fileName,cv2.IMREAD_UNCHANGED)
		w,h,_=im.shape
		im[0:w,0:white]=255
		im[0:white,0:h]=255
		imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		(thresh, im_bw) = cv2.threshold(imgray, 245, 255, cv2.THRESH_BINARY)
		ret, thresh = cv2.threshold(imgray, 254, 255, cv2.THRESH_BINARY_INV)
		ret, im_th = cv2.threshold(imgray, 254, 255, cv2.THRESH_BINARY_INV)
		im_floodfill=im_th.copy()
		h,w=im_th.shape[:2]
		mask=np.zeros((h+2,w+2),np.uint8)
		cv2.floodFill(im_floodfill,mask,(0,0),255)
		im_floodfill_inv = cv2.bitwise_not(im_floodfill)
		im_out = im_th | im_floodfill_inv
		im_out2=cv2.bitwise_and(im,im,mask=mask[:-2,:-2])
		im2=np.copy(im)
		dst=cv2.add(im2,im_out2)
		_,_,l=im.shape
		if(l==3):
			b,g,r=cv2.split(im)
			rgba=[b,g,r,im_out]
		else:
			b,g,r,a=cv2.split(im)
			#im_out=cv2.bitwise_or(im_out,a)
			rgba=[b,g,r,im_out]
		dst2=cv2.merge(rgba,4)
		im=dst2
		w,h,_=im.shape
		im[0:w,0:white]=255
		im[0:white,0:h]=255
		ret, thresh = cv2.threshold(im_out, 240, 255, cv2.THRESH_BINARY)
		im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		im3=np.copy(im2)
		cv2.drawContours(im3,contours,-1,255,3)
		if(len(contours)>4 or count>5):
			repeat=0
		else:
			white+=5
			count+=1
	r=0 
	g=0 
	b=0
	i=0
	im2=np.copy(im)
	largestSquares=list();
	for c in contours:
		if(len(largestSquares)<25):
			largestSquares.append(cv2.boundingRect(c))
			largestSquares.sort(key=lambda ls:ls[2]*ls[3])
		else:
			x,y,w,h = cv2.boundingRect(c)
			a=(w)*(h)
			for index, ls in enumerate(largestSquares):
				xl,yl,wl,hl=ls
				al=(wl)*(hl)
				if a>al:
					print(str(a)+" "+str(al))
					largestSquares[index]=cv2.boundingRect(c)
					largestSquares.sort(key=lambda ls:ls[2]*ls[3])
					break
		x,y,w,h = cv2.boundingRect(c)
		a=(w)*(h)
		cv2.rectangle(im2,(x,y),(x+w,y+h),(0,255,0),2)
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(im2,str(i),(x,y+20),font,.5,(0,255,0),1,cv2.LINE_AA)
		i+=1
	index=0
	os.chdir(fileName[:-4])
	for ls in largestSquares:
		xl,yl,wl,hl=ls
		print(str(xl)+" "+str(yl)+" "+str((xl+wl)*(yl+hl)))
		cv2.rectangle(im2,(xl,yl),(xl+wl,yl+hl),(255,255,0),2)
		font = cv2.FONT_HERSHEY_SIMPLEX
		crop_img=im[yl:yl+hl,xl:xl+wl]
		cv2.imwrite("sprite"+str(index)+".png",crop_img)
		if(index>(len(largestSquares)-8)):
			r_im=cv2.resize(crop_img,(50,50))
			os.chdir("../bracket")
			cv2.imwrite(fileName[:-4]+str(index)+".png",r_im)
			os.chdir("../"+fileName[:-4])
		index+=1
		print("hi")
	cv2.imwrite(fileName,im)
	os.chdir("../bracket")
	cv2.imwrite(fileName,im)
	cv2.waitKey(0)

if not os.path.exists("bracket"):
	os.mkdir("bracket")
for pic in glob.glob("*.png"):
	if not os.path.exists(pic[:-4]):
		os.mkdir(pic[:-4])
	splitImage(pic)
	os.chdir("..")