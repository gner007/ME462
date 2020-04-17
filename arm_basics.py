# libraies
from math import atan,sin,cos,pi,acos,atan2,sqrt
import numpy as np
import matplotlib.pyplot as plt
import cmath as c
from mpl_toolkits.mplot3d import Axes3D

# variables defaults
l1=8; l2=6                  # constants  
tetha_0=0; tetha_1=0; tetha_2=0        # angles  


link1_pos=l1*c.exp(1j*tetha_1)
link2_pos=l2*c.exp(1j*tetha_2)
pin_pos=link1_pos+link2_pos

r_pin=pin_pos.real
z_pin=pin_pos.imag

# inputs are angles of links 
# outputs are position coordinates of links
def FK(angle0,angle1,angle2):
    r1=l1*cos(angle1)
    r2=r1+l2*cos(angle1+angle2)
    z1=l1*sin(angle1)
    z2=z1+l2*sin(angle1+angle2)
    phi=angle0
    
    x1,y1=cylinder2xy(r1, phi)
    x2,y2=cylinder2xy(r2, phi)
    np.link1=[x1,y1,z1]
    np.link2=[x2,y2,z2]
    return np.link1,np.link2

# inputs are position of link_2 and sign variable
# outputs angles of links
def IK(x,y,z,sign=-1):
    r,phi=xy2cylinder(x,y)
    
    angle0=phi
    angle2=sign*acos((r**2+z**2-l1**2-l2**2)/(2*l1*l2))
    angle1=atan2(z,r)-atan2(l2*sin(angle2),(l1+l2*cos(angle2)))
    np.angles=[angle0, angle1, angle2]
    return np.angles

# inputs are angles and desired angular velocities
# outputs are corresponding linear velocities
def linear_velocity(angle0,angle1,angle2,angle0_d,angle1_d,angle2_d):
    xyz1,xyz2=FK(angle0,angle1,angle2)
    x=xyz2[0]
    y=xyz2[1]
    z=xyz2[2]
    r=sqrt(x**2+y**2)
    
    np.Jacobian_1_tetha12_rz=([-l1*sin(angle1)-l2*sin(angle1+angle2), -l2*sin(angle1+angle2)],[l1*cos(angle1)+l2*cos(angle1+angle2), l2*cos(angle1+angle2)])
    np.Jacobian_1_inv_rz_tetha12=np.linalg.inv(np.Jacobian_1_tetha12_rz)    
    np.Jacobian_2_rphi_xy=([cos(angle0),-r*sin(angle0)],[sin(angle0),r*cos(angle0)])
    np.Jacobian_2_inv_xy_rphi=np.linalg.inv(np.Jacobian_2_rphi_xy)    
    
    r_d,z_d=np.dot(np.Jacobian_1_tetha12_rz,([angle1_d],[angle2_d]))
    x_d,y_d=np.dot(np.Jacobian_2_rphi_xy,([r_d],[angle0_d]))
    return x_d,y_d,z_d

# inputs are angles and desired linear velocities
# outputs are corresponding angular velocities
def angular_velocity(angle0,angle1,angle2,x_d,y_d,z_d):
    xyz1,xyz2=FK(angle0,angle1,angle2)
    x=xyz2[0]
    y=xyz2[1]
    z=xyz2[2]
    r=sqrt(x**2+y**2)
    
    np.Jacobian_1_tetha12_rz=([-l1*sin(angle1)-l2*sin(angle1+angle2), -l2*sin(angle1+angle2)],[l1*cos(angle1)+l2*cos(angle1+angle2), l2*cos(angle1+angle2)])
    np.Jacobian_1_inv_rz_tetha12=np.linalg.inv(np.Jacobian_1_tetha12_rz)    
    np.Jacobian_2_rphi_xy=([cos(angle0),-r*sin(angle0)],[sin(angle0),r*cos(angle0)])
    np.Jacobian_2_inv_xy_rphi=np.linalg.inv(np.Jacobian_2_rphi_xy)
    
    r_d,angle0_d=np.dot(np.Jacobian_2_inv_xy_rphi,([x_d],[y_d]))
    angle1_d,angle2_d=np.dot(np.Jacobian_1_inv_rz_tetha12,([r_d],[z_d]))
    return angle0_d,angle1_d,angle2_d

# inputs are positions of each links
# output is a graph shows a    
def arm_plot (x1,y1,z1,x2,y2,z2):
    ax = plt.gca(projection="3d")
    x,y,z = [0,x1,x2],[0,y1,y2],[0,z1,z2]
    ax.scatter(x,y,z, c='r',s=100)
    ax.plot(x,y,z, color='r')
    
    ax.set_xlim3d(-l1-l2,l1+l2)
    ax.set_ylim3d(-l1-l2,l1+l2)
    ax.set_zlim3d(0,l1+l2)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    
    plt.show()
      
# inputs initial cordinates,final coordinates, Step
# shows all steps in one fig    
def arm_move (xi,yi,zi,xf,yf,zf,N=10):
    tetha0_i,tetha1_i,tetha2_i=IK(xi,yi,zi,-1)
    tetha0_f,tetha1_f,tetha2_f=IK(xf,yf,zf,-1)
    delta_tetha1=(tetha1_f-tetha1_i)/N
    delta_tetha2=(tetha2_f-tetha2_i)/N
    delta_tetha0=(tetha0_f-tetha0_i)/N
    plt.figure(1)
    plt.ion()
    i=0
    while i<N+1:     
        [x1,y1,z1],[x2,y2,z2]=FK(tetha0_i+delta_tetha0*i,tetha1_i+delta_tetha1*i,tetha2_i+delta_tetha2*i)
        arm_plot (x1,y1,z1,x2,y2,z2)
        plt.draw()
        plt.pause(0.1)
        i=i+1
    plt.ioff()
    plt.show(3)
    plt.close
    

def cylinder2xy(r,phi):
    x=r*cos(phi)
    y=r*sin(phi)
    return x,y
    
def xy2cylinder(x,y):
    r=sqrt(x**2+y**2)
    phi=atan2(y,x)
    return r,phi    
    
    
    
arm_move (2,2,2,0,0,14,N=10)