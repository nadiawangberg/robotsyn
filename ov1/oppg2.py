import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math as math
import numpy as np


#Platform to camera matrix
T_p_to_c = [[0.894372, -0.447712, 0.0127064, -0.25861],
		    [-0.0929288, -0.213413, -0.972924, 0.116584],
		    [0.438049, 0.868713, -0.232355, 0.791487],
		    [0, 0, 0, 1]]


screw0 = np.array([[0], [0], [0], [1]])
screw1 = np.array([[0.1145], [0], [0], [1]])
screw2 = np.array([[0], [0.1145], [0], [1]])
screw3 = np.array([[0.1145], [0.1145], [0], [1]])


def cam_to_pxl(X,Y,Z): # task 1d
	#camera intrinsic (heli_intrinsics)
	#everything should be given in meters
	fx = 1075.47
	fy = 1077.22
	cx = 621.01
	cy = 362.80

	u = cx + fx*(X/Z)
	v = cy + fy*(Y/Z)

	return u,v

img=mpimg.imread('quanser.jpg')
imgplot = plt.imshow(img)

screw0_cam = T_p_to_c @ screw0
x,y = cam_to_pxl(screw0_cam[0], screw0_cam[1], screw0_cam[2])
plt.plot(x,y, 'bo')

screw1_cam = T_p_to_c @ screw1
x,y = cam_to_pxl(screw1_cam[0], screw1_cam[1], screw1_cam[2])
plt.plot(x,y, 'bo')

screw2_cam = T_p_to_c @ screw2
x,y = cam_to_pxl(screw2_cam[0], screw2_cam[1], screw2_cam[2])
plt.plot(x,y, 'bo')

screw3_cam = T_p_to_c @ screw3
x,y = cam_to_pxl(screw3_cam[0], screw3_cam[1], screw3_cam[2])
plt.plot(x,y, 'bo')


plt.show()