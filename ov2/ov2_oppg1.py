import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math as math
import numpy as np

fx = 9.842439e+02
cx = 6.900000e+02
fy = 9.808141e+02
cy = 2.331966e+02
k1 = -3.728755e-01
k2 = 2.037299e-01
p1 = 2.219027e-03
p2 = 1.383707e-03
k3 = -7.233722e-02

def R_x(theta):
    t = math.radians(theta)

    c = math.cos(t)
    s = math.sin(t)
    return np.array(
            [[1, 0, 0, 0],
            [0, c, -s, 0],
            [0, s, c, 0],
            [0, 0, 0, 1]] )

def R_y(theta):
    t = math.radians(theta)

    c = math.cos(t)
    s = math.sin(t)
    return np.array(
            [[c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]] )

def R_z(theta):
    t = math.radians(theta)

    c = math.cos(t)
    s = math.sin(t)
    return np.array(
            [[c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]] )


def get_distortion(x,y):
	r = (x**2 + y**2)**0.5
	delta_x =  (k1*(r**2) + k2*(r**4) + k3*(r**6))*x + 2*p1*x*y + p2*(r**2 + 2*x**2) #distortion param x 
	delta_y =  (k1*(r**2) + k2*(r**4) + k3*(r**6))*y + p1*(r**2 + 2*y**2) + 2*p2*x*y #distortion param y 
	return delta_x, delta_y

def cam_to_pxl(X,Y,Z):
    u = cx + fx*(X/Z)
    v = cy + fy*(Y/Z)

    return u,v

def undistort(u_dst, v_dst):
	#1.
	x = (1/fx)*(u_dst-cx) #x = X/Z
	y = (1/fy)*(v_dst-cy) #y = Y/Z
	delta_x, delta_y = get_distortion(x,y)

	#2.
	u_src = int(round(u_dst + fx*delta_x))
	v_src = int(round(v_dst + fy*delta_y))

	return u_src, v_src


img_src = mpimg.imread('data/kitti.jpg')
img_dst = img_src.copy()

plt.figure("original - distorted :(")
imgplot = plt.imshow(img_src)

#undistort every px in dst image
for v_dst in range(len(img_dst)):
	for u_dst in range(len(img_dst[0])):
		u_src, v_src = undistort(u_dst, v_dst)
		img_dst[v_dst][u_dst] = img_src[v_src][u_src]

plt.figure("undistorted :)")
imgplot = plt.imshow(img_dst)

plt.show()


