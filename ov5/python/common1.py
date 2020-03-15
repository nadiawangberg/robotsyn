import numpy as np
from math import floor, ceil

# Task 1a
def central_difference(I):
    filtr_u = np.array([0.5, 0, -0.5])

    Iu = np.zeros_like(I)
    for r in range(len(I)):
        Iu[r] = np.convolve(filtr_u, I[r],mode="same")

    Iv = np.zeros_like(I)
    for c in range(len(I[0])):
        Iv[:,c] = np.convolve(filtr_u, I[:,c],mode="same")

    Im = np.sqrt(np.square(Iu) + np.square(Iv)) # Placeholder
    return Iu, Iv, Im

# Task 1b
def blur(I, sigma):
    """
    Applies a 2-D Gaussian blur with standard deviation sigma to
    a grayscale image I.
    """
    w=2*np.ceil(3*sigma) + 1 # size of kernel
    kernel = np.zeros(int(w))

    middle_i = floor(len(kernel)/2)
    for i in range(len(kernel)):
        u = abs(middle_i-i) # distance from middle
        kernel[i] = np.exp(-u**2/(2*sigma**2))/(np.sqrt(2*np.pi)*sigma)

    print(kernel)
    I_blur = I
    for r in range(len(I_blur)):
        I_blur[r] = np.convolve(kernel, I_blur[r],mode="same")

    for c in range(len(I_blur[0])):
        I_blur[:,c] = np.convolve(kernel, I_blur[:,c],mode="same")

    return I_blur

# Task 1c
def extract_edges(Iu, Iv, Im, threshold):
    """
    Returns the u and v coordinates of pixels whose gradient
    magnitude is greater than the threshold.
    """

    # This is an acceptable solution for the task (you don't
    # need to do anything here). However, it results in thick
    # edges. If you want better results you can try to replace
    # this with a thinning algorithm as described in the text.
    v,u = np.nonzero(Im > threshold)
    theta = np.arctan2(Iv[v,u], Iu[v,u])
    return u, v, theta

def rgb2gray(I):
    """
    Converts a red-green-blue (RGB) image to grayscale brightness.
    """
    return 0.2989*I[:,:,0] + 0.5870*I[:,:,1] + 0.1140*I[:,:,2]
