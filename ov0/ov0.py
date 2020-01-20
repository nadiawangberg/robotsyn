import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math as math


def distancee(v1, v2):
	return math.sqrt(math.pow(v1[0]-v2[0], 2) + math.pow(v1[1]-v2[1], 2) + math.pow(v1[2]-v2[2], 2))


img=mpimg.imread('roomba.jpg')
red_filtered = img[:,:,0]
new = img.copy()

plt.subplot(211)
imgplot = plt.imshow(img) #strong saturation = a lot of that color

"""
for y in range(len(red_filtered)): 
	for x in range(len(red_filtered[0])):
		if (red_filtered[y][x] > 200):
			new[y][x] = [255,255,255]
		else:
			new[y][x] = [0,0,0]

plt.subplot(212)
imgplot2 = plt.imshow(new)
plt.show()
"""

c_ref = [255,0,0] #strong red

for y in range(len(img)): 
	for x in range(len(img[0])):
		#print(distancee(c_ref, img[y][x]))
		if distancee(c_ref, img[y][x]) < 190:
			new[y][x] = [255,255,255]
		else:
			new[y][x] = [0,0,0]

plt.subplot(212)
imgplot2 = plt.imshow(new)
plt.show()



#Tasks
# a) done 
# b) 0 is the red channel, because the red roomba is bright
# c) no it sucks :C