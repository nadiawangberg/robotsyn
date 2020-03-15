import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math as math
import numpy as np


def point(x,y,z):
    return np.array([[x], [y], [z], [1]])

#fiducial markers in arm frame
p1 = np.array([-0.130851, -0.0092500, 0.0092500, 1.0]).transpose()
p2 = np.array([0.177649, -0.0092500, 0.0092500, 1.0]).transpose()
p3 = np.array([0.432149, -0.0092500, 0.0092500, 1.0]).transpose()

#fiducial markers in rotors frame
p4 = np.array([-0.027000, -0.0879548, -0.0357487, 1.0]).transpose()
p5 = np.array([-0.027000, -0.1760080, -0.0540649, 1.0]).transpose()
p6 = np.array([-0.027000 , 0.2088050, -0.0448200 , 1.0]).transpose()
p7 = np.array([-0.027000, 0.1073210, -0.0397018 , 1.0]).transpose()


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
    #X,Y,Z should be given in meters
    fx = 1075.47
    fy = 1077.22
    cx = 621.01
    cy = 362.80

    u = cx + fx*(X/Z)
    v = cy + fy*(Y/Z)

    return u,v

def draw_line(a, b, **args):
    plt.plot([a[0], b[0]], [a[1], b[1]], **args, linewidth=3.5)

def draw_frame(T):
    #From T to camera
    origin = T@point(0,0,0)
    o1,o2 = cam_to_pxl(origin[0], origin[1], origin[2])

    x_axis = T@point(0.05,0,0) #red
    y_axis = T@point(0,0.05,0) #green
    z_axis = T@point(0,0,0.05) #blue

    #From cam to pixel coordinates
    x1,x2 = cam_to_pxl(x_axis[0], x_axis[1], x_axis[2])
    y1,y2 = cam_to_pxl(y_axis[0], y_axis[1], y_axis[2])
    z1,z2 = cam_to_pxl(z_axis[0], z_axis[1], z_axis[2])

    #Draw x,y,z axis
    draw_line([o1,o2], [x1,x2], color='red')
    draw_line([o1,o2], [y1,y2], color='green')
    draw_line([o1,o2], [z1,z2], color='blue')

    #plt.text(o1- 30,o2 - 5, label)

def plot_point(point, T, color = 'wo'):
    point_transformed = T@point
    x,y = cam_to_pxl(point_transformed[0], point_transformed[1], point_transformed[2])
    plt.plot(x,y,color)


#Platform to camera matrix
T_plat_to_cam = [[0.894372, -0.447712, 0.0127064, -0.25861],
            [-0.0929288, -0.213413, -0.972924, 0.116584],
            [0.438049, 0.868713, -0.232355, 0.791487],
            [0, 0, 0, 1]]

# oppg 2a
img=mpimg.imread('quanser.jpg')
imgplot = plt.imshow(img)

screw0 = np.array([[0], [0], [0], [1]])
screw1 = np.array([[0.1145], [0], [0], [1]])
screw2 = np.array([[0], [0.1145], [0], [1]])
screw3 = np.array([[0.1145], [0.1145], [0], [1]])

plot_point(screw0, T_plat_to_cam)
plot_point(screw1, T_plat_to_cam)
plot_point(screw2, T_plat_to_cam)
plot_point(screw3, T_plat_to_cam)

#oppg 2b
draw_frame(T_plat_to_cam)

#oppg 3c
psi = 11.77 #Yaw
T_base_to_plat = Translate(0.0573, 0.0573, 0) @ R_z(psi)
T_base_to_cam = T_plat_to_cam @ T_base_to_plat
draw_frame(T_base_to_cam) #trans to cam to pix

#oppg 3d
theta = 28.87 #Pitch
T_hinge_to_base = Translate(0, 0, 0.325) @ R_y(theta)
T_hinge_to_cam = T_base_to_cam @ T_hinge_to_base
draw_frame(T_hinge_to_cam)

#oppg 3d
T_arm_to_hinge = Translate(0, 0, -0.0552)
T_arm_to_cam = T_hinge_to_cam @ T_arm_to_hinge
draw_frame(T_arm_to_cam) #arm to plat

#oppg 3e
phi = -0.5 #Roll
T_rotors_to_arm = Translate(0.653, 0, -0.0312) @ R_x(phi)
T_rotors_to_cam = T_arm_to_cam @ T_rotors_to_arm
draw_frame(T_rotors_to_cam)

#oppg 3f
plot_point(p1, T_arm_to_cam, 'co')
plot_point(p2, T_arm_to_cam, 'co')
plot_point(p3, T_arm_to_cam, 'co')

plot_point(p4, T_rotors_to_cam, 'co')
plot_point(p5, T_rotors_to_cam, 'co')
plot_point(p6, T_rotors_to_cam, 'co')
plot_point(p7, T_rotors_to_cam, 'co')

plt.show()