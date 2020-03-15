import numpy as np

def linear_triangulation(uv1, uv2, P1, P2):
    """
    Compute the 3D position of a single point from 2D correspondences.

    Args:
        uv1:    2D projection of point in image 1.
        uv2:    2D projection of point in image 2.
        P1:     Projection matrix with shape 3 x 4 for image 1.
        P2:     Projection matrix with shape 3 x 4 for image 2.

    Returns:
        X:      3D coordinates of point in the camera frame of image 1.
                (not homogeneous!)

    See HZ Ch. 12.2: Linear triangulation methods (p312)
    """
    
    u = uv1[0]
    v = uv1[1]
    u_d = uv2[0]
    v_d = uv2[1]
    A = [[u*P1[2].T - P1[0].T],
         [v*P1[2].T - P1[1].T],
         [u_d*P2[2].T - P2[0].T],
         [v_d*P2[2].T - P2[1].T]]


    U, S, V_t = np.linalg.svd(A)
    X = V_t[-1,-1] #TODO, hva skjer, last column of last matrix
 
    X_3d = [X[0], X[1], X[2]] #X[3] = 1
    return X_3d
