import matplotlib.pyplot as plt
import math as math
import numpy as np

from mpl_toolkits import mplot3d

def T_z(t_z):
    return np.array(
            [[1, 0, 0, 0],
            [0, 1, 0, 0],
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

def cam_to_pxl(X,Y,Z):
    c_x = 320.0
    c_y = 240.0
    d_x_inv = 200.0
    d_y_inv = 220.0
    f = 5.0

    u = c_x + d_x_inv*f*(X/Z)
    v = c_y + d_y_inv*f*(Y/Z)

    return u,v

def plot_3d_box():
    #plot box 3d
    fig = plt.figure(1)
    ax = plt.axes(projection='3d')
    ax.scatter3D(box[:,0], box[:,1], box[:,2], cmap='Greens')


def plot_2d_box(): #task 1b
    #copy of global box variable
    box_cp = box.copy()

    #2d box transform
    for point in box_cp:
        point[0], point[1] = cam_to_pxl(point[0],point[1],point[2] + 5) # coordinates translated +5 to turn into cam coords. 

    #plot box 2d
    fig_2 = plt.figure(2)
    ax_2 = plt.axis([0,640, 0, 480])
    plt.plot(box_cp[:,0], box_cp[:,1], 'ro')

def transform_box(): #task 1d
    #copy of global box variable
    box_cp = box.copy()

    #2d box transform
    T_o_to_c = T_z(5)@T_z(1) @ R_x(30) @ R_y(30)
    for p in range(len(box_cp)):
        box_cp[p] = T_o_to_c @ box_cp[p]
        # cam starts within the center of the box
        # the box is translated 5 away, putting the box in the correct pos in respect to the camera
        # the box is translated 1 away, then rotated in respect to ITS axis
        box_cp[p][0], box_cp[p][1] = cam_to_pxl(box_cp[p][0],box_cp[p][1],box_cp[p][2]) # coordinates translated +5 to turn into cam coords. 
    
    #plot box 2d
    fig_2 = plt.figure(3)
    ax_2 = plt.axis([0,640, 480, 0])
    plt.plot(box_cp[:,0], box_cp[:,1], 'bo')

#load box
box = np.loadtxt("box.txt")

#plots
plot_3d_box()
plot_2d_box()
transform_box()

plt.show()
