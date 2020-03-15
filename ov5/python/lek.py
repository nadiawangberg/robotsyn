import numpy as np
import matplotlib.pyplot as plt
from common1 import *

blur_sigma = 0.5
filename       = '../data/image1_und.jpg'
I_rgb      = plt.imread(filename)
I_rgb      = I_rgb/255.0
I_gray     = rgb2gray(I_rgb)
Iu, Iv, Im = central_difference(I_gray)
I_blur = blur(I_gray, blur_sigma)

plt.imshow(I_blur, cmap="gray")
plt.show()