import numpy as np
import matplotlib.pyplot as plt
from common1 import *
from common2 import *

edge_threshold = 0.04
blur_sigma     = 1.1
filename       = '../data/image1_und.jpg'

I_rgb      = plt.imread(filename)
I_rgb      = I_rgb/255.0
I_gray     = rgb2gray(I_rgb)
I_blur     = blur(I_gray, blur_sigma)
Iu, Iv, Im = central_difference(I_blur)
u,v,theta  = extract_edges(Iu, Iv, Im, edge_threshold)

#Task 2a
bins      = 80 #resolution of what can be voted for
rho = u*np.cos(theta) + v*np.sin(theta) #all 
rho_max   = max(rho)
rho_min   = min(rho)
theta_min = min(theta)
theta_max = max(theta)
H = np.zeros([bins,bins]) # Accumulator array

#histogram stores "votes"
H, _, _ = np.histogram2d(theta, rho, bins=bins, range=[[theta_min, theta_max], [rho_min, rho_max]])
H = H.T # Make rows be rho and columns be theta (see documentation)
print(H)
plt.hist(H, bins=bins)

# Task 2b: Find local maxima
line_threshold = 50
window_size = 10
peak_rows,peak_cols = extract_peaks(H, window_size, line_threshold)
#rho,    theta

# Task 2c: Convert peak (row, column) pairs into (theta, rho) pairs.
print(peak_cols,peak_rows)
print("min, max", rho_min, rho_max)

peak_theta = [] # Placeholder to demonstrate use of draw_line
peak_rho   = [] # Placeholder to demonstrate use of draw_line
for i in range(len(peak_rows)):
	rho = (rho_max-rho_min)/(bins-1)*peak_rows[i] + rho_min #(rho_min - rho_max)/(bins-1) * peak_rows[i] + rho_max
	theta = (theta_max-theta_min)/(bins-1) * peak_cols[i] + theta_min
	peak_theta.append(theta)
	peak_rho.append(rho)

print(peak_theta, peak_rho)

plt.figure(figsize=[6,8])
plt.subplot(211)
plt.imshow(H, extent=[theta_min, theta_max, rho_min, rho_max], aspect='auto')
plt.xlabel('$\\theta$ (radians)')
plt.ylabel('$\\rho$ (pixels)')
plt.colorbar(label='Votes')
plt.title('Hough transform histogram')
plt.subplot(212)
plt.imshow(I_rgb)
plt.xlim([0, I_rgb.shape[1]])
plt.ylim([I_rgb.shape[0], 0])
for i in range(len(peak_theta)):
    draw_line(peak_theta[i], peak_rho[i], color='yellow')
plt.tight_layout()
plt.savefig('out2.png')
plt.show()
