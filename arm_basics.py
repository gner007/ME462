# libraies
from math import atan,sin,cos,pi,acos,atan2
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
    angle1=atan2(y,x)-atan2(l2*sin(angle2),(l1+l2*cos(angle2)))
    return angle1,angle2

def velocity():
    
    return

def angular_velocity():
    
    return

# inputs are positions of each links
# output is a graph shows a    
def arm_plot (x1,y1,x2,y2):
    plt.plot([0, x1],[0,y1],'r-', linewidth=2)
    plt.plot([x1,x2],[y1,y2],'r-', linewidth=2)
    plt.plot([0],[0], marker="o",)
    plt.plot([x1],[y1], marker="o")
    plt.plot([x2],[y2], marker="o")
    plt.xlim(-(l1+l2),l1+l2+1)
    plt.ylim(-(l1+l2),l1+l2+1)
      
# inputs initial cordinates,final coordinates, Step
# shows all steps in one fig    
def arm_move (xi,yi,xf,yf,N=10):
    tetha1_i,tetha2_i=IK(xi,yi,-1)
    tetha1_f,tetha2_f=IK(xf,yf,-1)
    delta_tetha1=(tetha1_f-tetha1_i)/N
    delta_tetha2=(tetha2_f-tetha2_i)/N
    plt.figure(1)
    plt.ion()
    i=0
    while i<N+1:     
        x1,y1,x2,y2=FK(tetha1_i+delta_tetha1*i,tetha2_i+delta_tetha2*i)
        arm_plot (x1,y1,x2,y2)
        plt.draw()
        plt.pause(0.1)
        i=i+1
    plt.ioff()
    plt.show(3)
    plt.close
    
arm_move (2,2,8,8,N=10)
