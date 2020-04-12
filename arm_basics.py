# libraies

from math import atan,sin,cos,pi,acos
import numpy as np
import matplotlib.pyplot as plt

# variables defaults

l1=8; l2=6                  # constants  
tetha_1=0; tetha_2=0        # angles 
w_1=0; w_2=0                # derivatives 
x_1=0; y_1=l1               # positions
v_x_1=0; v_y_1=0            # derivatives
x_2=x_1+0; y_1=y_1+l2       # positions
v_x_2=0; v_y_2=0            # derivatives


# inputs are angles of links 
# outputs are position coordinates of links
def FK(angle1,angle2):
    x1=l1*cos(angle1)
    x2=x1+l2*cos(angle1+angle2)
    y1=l1*sin(angle1)
    y2=y1+l2*sin(angle1+angle2)
    return x1,y1,x2,y2

# inputs are position of link_2 and sign variable
# outputs angles of links
def IK(x,y,sign=-1):
    angle2=sign*acos((x**2+y**2-l1**2-l2**2)/(2*l1*l2))
    angle1=atan(y/x)-atan(l2*sin(angle2)/(l1+l2*cos(angle2)))
    return angle1,angle2

def velocity():
    
    return

def angular_velocity():
    
    return

# inputs are positions of each links
# output is a graph shows arm     
def plotter (x1,y1,x2,y2):
    plt.plot([0, x1],[0,y1],'r-', linewidth=2)
    plt.plot([x1,x2],[y1,y2],'r-', linewidth=2)
    plt.plot([0],[0], marker="o",)
    plt.plot([x1],[y1], marker="o")
    plt.plot([x2],[y2], marker="o")
    plt.xlim(-1,l1+l2+1)
    plt.ylim(-1,l1+l2+1)