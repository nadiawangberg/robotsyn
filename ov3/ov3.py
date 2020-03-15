import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math as math
import numpy as np



# think about whether it is rows or columns
# matrix[row][column]
def decompose(H):
	lamb = math.sqrt(H[0][0]**2 + h[1][0]**2 + h[2][0]**2)
	H_a = 1/lamb * H
	r_3a = H_a[0] CROSS H_a[1]

	H_b = -1/lamb * H
	r_3b = H_b[0] CROSS H_b[1]

	t_a = col 3 of H_a
	t_b = col 3 of H_b

	return (R_a,t_a), (R_b,t_b)

H = np.array(
            [[1, 0, 0],
             [0, 1, 0],
             [0, 0, 1]]

(R1, t1), (R2, t2) = decompose(H)
print(R2)