import numpy as np
import matplotlib.pyplot as plt



def Rotation(deg): #theta is radians
	rad = deg*np.pi/180
	return np.array([[np.cos(rad), -np.sin(rad),0],[np.sin(rad), np.cos(rad),0], [0,0,1]])

def translate(x,y): #amount you want to translate from x to y
	return np.array([[1,0,x],[0,1,y],[0,0,1]])





print(Rotation(30)*translate(3,0))

print(translate(3,0)*Rotation(30))

