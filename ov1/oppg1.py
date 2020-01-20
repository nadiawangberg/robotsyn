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

"""
def point(x,y):
    return np.array([[x], [y], [1]])

def draw_line(a, b, **args):
    plt.plot([100,200], [10,20], **args, label='line 1', linewidth=2)
    print([a[0,0], b[0,0]], [a[1,0], b[1,0]])
    plt.plot([a[0,0], b[0,0]], [a[1,0], b[1,0]], **args, label='line 2', linewidth=2)
"""

def point2(x,y,z):
    return np.array([[x], [y], [z], [1]])

def draw_line2(u, v, **args):
    plt.plot([u[0], v[0]], [u[1], v[1]], **args, label='line 1', linewidth=2)

def draw_frame2(T, label):
    origin = T@point(0,0,0)
    draw_line(origin, T@point(1,0,0), color='red')
    draw_line(origin, T@point(0,1,0), color='green')
    #plt.text(origin[0,0], origin[1,0] - 0.4, label)

"""
def draw_frame(T, label):
    origin = T@point(0,0)
    draw_line(origin, T@point(1,0), color='red')
    draw_line(origin, T@point(0,1), color='green')
    plt.text(origin[0,0], origin[1,0] - 0.4, label)
"""
"""
def draw_frame2(T, label):
    plt.plot(100, 150, 'r+')
    origin = T@np.array([[0], [0], [0], [1]])
    print(origin)
    x_trans = T@np.array([[1], [0], [0], [1]])
    y_trans = T@np.array([[0], [1], [0], [1]])
    x1, x2  = cam_to_pxl(x_trans[0], x_trans[1], x_trans[2])
    y1, y2 = cam_to_pxl(y_trans[0], y_trans[1], y_trans[2])
    draw_line(origin, [x1, x2], color='red')
    draw_line(origin, [y1, y2], color='red')
    #plt.text(origin[0,0], origin[1,0] - 0.4, label)
"""

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

    #test, drawline
    plt.plot([100,200], [10,20], 'red', label='line 1', linewidth=2)
    draw_line2([150,200], [30,20])


    origin = T_o_to_c@point(0,0,0)
    plt.plot(origin[0], orgin[1], 

    """
    draw_line(origin, T@point(1,0), color='red')
    draw_line(origin, T@point(0,1), color='green')
    plt.text(origin[0,0], origin[1,0] - 0.4, label)
    """

    plt.plot(box_cp[:,0], box_cp[:,1], 'bo')


#load box
box = np.loadtxt("box.txt")

#plots
plot_3d_box()
plot_2d_box()
transform_box()

plt.show()
