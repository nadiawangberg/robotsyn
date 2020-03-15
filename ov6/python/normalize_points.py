import numpy as np

def normalize_points(pts):
    """ Computes a normalizing transformation of the points such that
    the points are centered at the origin and their mean distance from
    the origin is equal to sqrt(2).

    See HZ, Ch. 4.4.4: Normalizing transformations (p107).
    

    Args:
        pts:    Input 2D point array of shape n x 2

    Returns:
        pts_n:  Normalized 2D point array of shape n x 2
        T:      The normalizing transformation in 3x3 matrix form, such
                that for a point (x,y), the normalized point (x',y') is
                found by multiplying T with the point:

                    |x'|       |x|
                    |y'| = T * |y|
                    |1 |       |1|
    """

    # todo: Compute pts_n and T
    #Calculate averages
    n = len(pts)
    u_avg = 0
    v_avg = 0
    for point in pts:
        u_avg += point[0]
        v_avg += point[1]
    u_avg /= n
    v_avg /= n


    #Calculate sigmas
    sigma = 0
    for point in pts:
        #print(point)
        v1 = point[0] - u_avg
        v2 = point[1] - v_avg
        sigma += np.sqrt(v1**2 + v2**2)
    sigma /= n



    sqrt_2 = np.sqrt(2)
    T = np.array([[sqrt_2/sigma, 0, -sqrt_2/sigma * u_avg], 
                   [0, sqrt_2/sigma, -sqrt_2/sigma * v_avg],
                   [0,    0,     1] ])


    pts_n = []
    for i in range(len(pts)):
        #print("u_normalized", pts[i,1]/v_avg)
        x_i = T@np.array([[pts[i,0]],[pts[i,1]],[1]])
        #print(x_i)
        pts_n.append([float(x_i[0]), float(x_i[1])])

    pts_n = np.array(pts_n)


    #pts_n = pts
    #T = np.eye(3)
    #print("PTSSSSS;", pts)
    #print("PTSSSSS NNN;", pts_n)
    return pts_n, T
    #return pts, np.eye(3)
