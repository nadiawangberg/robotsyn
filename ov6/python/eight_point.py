import numpy as np
from normalize_points import *

def eight_point(uv1, uv2):
    """ Given n >= 8 point matches, (u1 v1) <-> (u2 v2), compute the
    fundamental matrix F that satisfies the equations

        (u2 v2 1)^T * F * (u1 v1 1) = 0

    Args:
        uv1: (n x 2 array) Pixel coordinates in image 1.
        uv2: (n x 2 array) Pixel coordinates in image 2.

    Returns:
        F:   (3 x 3 matrix) Fundamental matrix mapping points in image 1
             to lines in image 2.

    See HZ Ch. 11.2: The normalized 8-point algorithm (p.281).
    """

    #Normalise points
    uv1_n, T1 = normalize_points(uv1)
    uv2_n, T2 = normalize_points(uv2)

    A = []
    for i in range(len(uv1_n)):
        u_i = float(uv1_n[i,0]) # u'
        v_i = float(uv1_n[i,1])
        u_i2 = float(uv2_n[i,0]) #u regular
        v_i2 = float(uv2_n[i,1])
        A.append([u_i2*u_i, u_i2*v_i, u_i2, v_i2*u_i,  v_i2*v_i, v_i2, u_i, v_i, 1])
    
    A = np.asarray(A) # 110 x 9
    U, S, V_T = np.linalg.svd(A) #SVD - singular value decomposition, solves Ax = 0
    F = np.reshape(V_T[-1], (3,3))
    F_fixed = closest_fundamental_matrix(F)

    #Denormalize

    return T2.T@F_fixed@T1 #Denormalise F

def closest_fundamental_matrix(F):
    """
    Computes the closest fundamental matrix in the sense of the
    Frobenius norm. See HZ, Ch. 11.1.1 (p.280).
    """
    
    #makes lines straight
    U, D, V_t = np.linalg.svd(F)
    D_mat = np.diag(D)
    D_mat[-1,-1] = 0.0
    F_cor = U@D_mat@V_t

    return F_cor