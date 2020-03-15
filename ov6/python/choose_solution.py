import numpy as np
from linear_triangulation import *
from camera_matrices import *

def choose_solution(uv1, uv2, K1, K2, Rts):
    """
    Chooses among the rotation and translation solutions Rts
    the one which gives the most points in front of both cameras.
    """

    #NB!!! uv1 is many points
    
    #Rts - motion_from_essential(E) [(R1,t1), (R1,t2), (R2, t1), (R2, t2)]
    soln = 0
    for i in range(len(Rts)): # Rts : [(R1,t1), (R1,t2), (R2, t1), (R2, t2)]
        #print("Rts: ", Rts)
        R = Rts[i][0]
        t = Rts[i][1]
        P1, P2 = camera_matrices(K1, K2, R, t)
        #print("P1!!", P1)
        X = linear_triangulation(uv1[1], uv2[1], P1, P2) #done with one random point
        #4 x 1 vector 

        if X[2] > 0: # points can only be in front of both cameras
            print("FOUNDDDDDDDDDDDDDITTTTTTTTTTTTTTTT, Z > 0")
            print(X)
            soln = i
            break

    #soln = 0
    print('Choosing solution %d' % soln)
    return Rts[soln]
