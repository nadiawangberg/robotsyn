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



def Translate(t_x, t_y, t_z):
    return np.array(
            [[1, 0, 0, t_x],
            [0, 1, 0, t_y],
            [0, 0, 1, t_z],
            [0, 0, 0, 1]] )

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

def point(x,y,z):
    return np.array([[x], [y], [z], [1]])

def draw_line(a, b, **args):
    plt.plot([a[0], b[0]], [a[1], b[1]], **args, linewidth=4)

def draw_frame(T):
    origin = T@point(0,0,0)
    o1,o2 = cam_to_pxl(origin[0], origin[1], origin[2])

    x_axis = T@point(0.1,0,0) #red
    y_axis = T@point(0,0.1,0) #green
    z_axis = T@point(0,0,0.1) #blue

    x1,x2 = cam_to_pxl(x_axis[0], x_axis[1], x_axis[2])
    y1,y2 = cam_to_pxl(y_axis[0], y_axis[1], y_axis[2])
    z1,z2 = cam_to_pxl(z_axis[0], z_axis[1], z_axis[2])

    draw_line([o1,o2], [x1,x2], color='red')
    draw_line([o1,o2], [y1,y2], color='green')
    draw_line([o1,o2], [z1,z2], color='blue')

    #plt.text(o1- 30,o2 - 5, label)

img=mpimg.imread('quanser.jpg')
imgplot = plt.imshow(img)

screw0_cam = T_p_to_c @ screw0
x,y = cam_to_pxl(screw0_cam[0], screw0_cam[1], screw0_cam[2])
plt.plot(x,y, 'wo')

screw1_cam = T_p_to_c @ screw1
x,y = cam_to_pxl(screw1_cam[0], screw1_cam[1], screw1_cam[2])
plt.plot(x,y, 'wo')

screw2_cam = T_p_to_c @ screw2
x,y = cam_to_pxl(screw2_cam[0], screw2_cam[1], screw2_cam[2])
plt.plot(x,y, 'wo')

screw3_cam = T_p_to_c @ screw3
x,y = cam_to_pxl(screw3_cam[0], screw3_cam[1], screw3_cam[2])
plt.plot(x,y, 'wo')

draw_frame(T_p_to_c)

#oppg 3c
phi = 10
yaw_motion = T_p_to_c @ Translate(0.0573, 0.0573, 0) @ R_z(phi)
draw_frame(yaw_motion)

plt.show()