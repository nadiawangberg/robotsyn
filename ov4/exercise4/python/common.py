import numpy as np

K                  = np.loadtxt('../data/cameraK.txt')
p_model            = np.loadtxt('../data/model.txt')
platform_to_camera = np.loadtxt('../data/pose.txt')

def residuals(uv, weights, yaw, pitch, roll):
    #camera params
    fx = K[0][0]
    fy = K[1][1]
    cx = K[0][2]
    cy = K[1][2]

    # Helicopter model from Exercise 1 (aka homography_estm based on yaw, pitch roll)
    base_to_platform = translate(0.1145/2, 0.1145/2, 0.0)@rotate_z(yaw)
    hinge_to_base    = translate(0, 0, 0.325)@rotate_y(pitch)
    arm_to_hinge     = translate(0, 0, -0.0552)
    rotors_to_arm    = translate(0.653, 0, -0.0312)@rotate_x(roll)
    base_to_camera   = platform_to_camera@base_to_platform
    hinge_to_camera  = base_to_camera@hinge_to_base
    arm_to_camera    = hinge_to_camera@arm_to_hinge
    rotors_to_camera = arm_to_camera@rotors_to_arm

    res = []
    for i in range(len(p_model)):
        #predefined 3d transforms
        if (i <= 2):
            X = arm_to_camera @ p_model[i]
        else:
            X = rotors_to_camera @ p_model[i]

        #Convert from 3d to pxl coords
        X_i_c = X[0]
        Y_i_c = X[1]
        Z_i_c = X[2]
        u_hat = cx + fx * (X_i_c/Z_i_c)
        v_hat = cy + fy * (Y_i_c/Z_i_c)

        #defined residual vec
        e_u = u_hat - uv[i][0]
        e_v = v_hat - uv[i][1]
        r_i = np.sqrt(e_u**2 + e_v**2)*weights[i] #weights[i], whether it is detected or not

        res.append(r_i)
    return res

    # Tip: If A is an Nx2 array, np.linalg.norm(A, axis=1)
    # computes the Euclidean length of each row of A and
    # returns an Nx1 array.

def normal_equations(uv, weights, yaw, pitch, roll):
    #
    # Task 1b: Compute the normal equation terms
    #
    step = 0.001 # random
    r = residuals(uv, weights, yaw, pitch, roll)
    r_yaw = residuals(uv, weights, yaw+step, pitch, roll)
    r_pitch = residuals(uv, weights, yaw, pitch+step, roll)
    r_roll = residuals(uv, weights, yaw, pitch, roll+step)

    J = np.zeros((len(r), 3))
    for i in range(len(r)):
        J[i][0] = (r_yaw[i]-r[i])/step
        J[i][1] = (r_pitch[i]-r[i])/step
        J[i][2] = (r_roll[i]-r[i])/step
    print("J: ", J)
    JTJ = np.transpose(J)@J
    JTr = np.transpose(J)@r
    return JTJ, JTr

def gauss_newton(uv, weights, yaw, pitch, roll):
    #
    # Task 1c: Implement the Gauss-Newton method
    #
    max_iter = 100
    step_size = 0.25 #alpha
    for iter in range(max_iter):
        JTJ, JTr = normal_equations(uv, weights, yaw, pitch, roll)
        delta = np.linalg.solve(JTJ, -JTr)

        yaw += step_size*delta[0]
        pitch += step_size*delta[1]
        roll += step_size*delta[2]

    return yaw, pitch, roll

"""
def levenberg_marquardt(uv, weights, yaw, pitch, roll):
    #
    # Task 2a: Implement the Levenberg-Marquardt method
    #
    max_iter = 10
    JTJ,JTr=normal_equations(uv,weights,yaw,pitch,roll)
    lam=sum(np.diagonal(JTJ))/len(JTJ)
    step_size=1
    error=10000

    for i in range(max_iter):
        print("lambda: "+str(lam)+" iter: "+str(i))
        
        JTJ,JTr=normal_equations(uv,weights,yaw,pitch,roll)
        delta=np.linalg.solve(JTJ+lam*np.eye(3),-JTr)
        new_yaw=yaw+step_size*delta[0]
        new_pitch=pitch+step_size*delta[1]
        new_roll=roll+step_size*delta[2]
        new_error=sum(residuals(uv,weights,new_yaw,new_pitch,new_roll))
        if (new_error<error):
            if(abs(new_error-error)>0.001):
                yaw=new_yaw
                pitch=new_pitch
                roll=new_roll
                lam/=10
            else:
                continue
        else:
            lam*=10
        
    return yaw, pitch, roll
"""

def levenberg_marquardt(uv, weights, yaw, pitch, roll):
    alpha = 1

    #initialize lambda (1)
    JTJ, JTr = normal_equations(uv, weights, yaw, pitch, roll)
    lam = 10**(-3) * np.average(JTJ.diagonal())
    
    xtol = 0.01
    error=10000
    
    max_iter = 100
    for iter in range(max_iter):
        print("lambda: "+str(lam)+" iter: "+str(iter))

        JTJ, JTr = normal_equations(uv, weights, yaw, pitch, roll)
        delta = np.linalg.solve(JTJ + lam*np.eye(3), -JTr)
        new_yaw = yaw + alpha*delta[0]
        new_pitch = pitch + alpha*delta[1]
        new_roll = roll + alpha*delta[2]

        #Termination condition
        if (np.sqrt((new_roll-roll)**2 + (new_yaw-yaw)**2 + (new_pitch-pitch)**2) < xtol):
            return new_yaw, new_pitch, new_roll

        new_error = sum(residuals(uv, weights, new_yaw, new_pitch, new_roll))

        if (new_error < error): # 2. (reduced error)
            yaw = new_yaw
            roll = new_roll
            pitch = new_pitch
            error = new_error # only update error when new angles are used
            lam /= 10.0
        else: # 3.
            lam *= 10.0


    return yaw, pitch, roll

def rotate_x(radians):
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[1, 0, 0, 0],
                     [0, c,-s, 0],
                     [0, s, c, 0],
                     [0, 0, 0, 1]])

def rotate_y(radians):
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[ c, 0, s, 0],
                     [ 0, 1, 0, 0],
                     [-s, 0, c, 0],
                     [ 0, 0, 0, 1]])

def rotate_z(radians):
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[c,-s, 0, 0],
                     [s, c, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])

def translate(x, y, z):
    return np.array([[1, 0, 0, x],
                     [0, 1, 0, y],
                     [0, 0, 1, z],
                     [0, 0, 0, 1]])
