import matplotlib.pyplot as plt
import numpy as np
import math as math
from common import draw_frame

def estimate_H(xy, XY):
    A=np.zeros((2*len(xy),9),dtype=float)

    for i in range(0,len(xy),2): # For all points, place in matrix
        x1,y1 = xy[i]
        X1,Y1 = XY[i]
        
        A[i] = [X1, Y1, 1, 0, 0, 0, -X1*x1, -Y1*x1, -x1]
        A[i+1] = [0, 0, 0, X1, Y1, 1, -X1*y1, -Y1*y1, -y1]

    U,S,V_T=np.linalg.svd(A)
    v = V_T.transpose()
    h = v[:,-1] #all the rows, last columns
    H = np.reshape(h, (3,3)) #become a matrix again
    return H


def decompose_H(H):
    lamb = math.sqrt(H[0,0]**2 + H[1,0]**2 + H[2,0]**2)
    H_a = 1/lamb * H
    r_3a = np.cross(H_a[:,0], H_a[:,1])

    H_b = -1/lamb * H
    r_3b = np.cross(H_b[:,0], H_b[:,1])

    R_t_a = np.column_stack((H_a[:,0], H_a[:,1], r_3a, H_a[:,2]))
    R_t_b = np.column_stack((H_b[:,0], H_b[:,1], r_3b, H_b[:,2]))

    T1 = np.vstack((R_t_a, [0,0,0,1])) # add last row
    T2 = np.vstack((R_t_b, [0,0,0,1])) # add last row

    return T1, T2

def choose_solution(T1, T2):
    return T1 if T1[2,3] > 0 else T2

K           = np.loadtxt('../data/cameraK.txt')
all_markers = np.loadtxt('../data/markers.txt')
XY          = np.loadtxt('../data/model.txt')
n           = len(XY)

for image_number in range(23):
    I = plt.imread('../data/video%04d.jpg' % image_number)
    markers = all_markers[image_number,:]
    markers = np.reshape(markers, [n, 3])
    matched = markers[:,0].astype(bool) # First column is 1 if marker was detected
    uv = markers[matched, 1:3] # Get markers for which matched = 1

    # Convert pixel coordinates to normalized image coordinates
    xy = (uv - K[0:2,2])/np.array([K[0,0], K[1,1]])

    H = estimate_H(xy, XY[matched, :2])
    T1,T2 = decompose_H(H)
    T = choose_solution(T1, T2)

    # Compute predicted corner locations using model and homography
    uv_hat = (K@H@XY.T)
    uv_hat = (uv_hat/uv_hat[2,:]).T

    plt.clf()
    plt.imshow(I, interpolation='bilinear')
    draw_frame(K, T, scale=7)
    plt.scatter(uv[:,0], uv[:,1], color='red', label='Observed')
    plt.scatter(uv_hat[:,0], uv_hat[:,1], marker='+', color='yellow', label='Predicted')
    plt.legend()
    plt.xlim([0, I.shape[1]])
    plt.ylim([I.shape[0], 0])
    plt.savefig('../data/out%04d.png' % image_number)
    plt.show()
