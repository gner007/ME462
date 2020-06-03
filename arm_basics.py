# libraies
from math import atan,sin,cos,pi,acos,atan2,sqrt
import numpy as np
import matplotlib.pyplot as plt
import cmath as c
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation, rc
from IPython.display import HTML

# variables defaults
l1=23.4; l2=19.5 ;z_off=11.2            # constants  
tetha_0=0; tetha_1=0; tetha_2=0         # angles  
GR0=5 ;GR1=120/16 ; GR2=6;

link1_pos=l1*c.exp(1j*tetha_1)
link2_pos=l2*c.exp(1j*tetha_2)
pin_pos=link1_pos+link2_pos

r_pin=pin_pos.real
z_pin=pin_pos.imag

# 16_segment constants
segment_x=1
segment_y=1.75
x_i_ref=-15
y_i_ref=25
z_ref=15

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

# for debug purposes to close the path close from arm_plot function
def plot_path(N=100):
    ax = plt.gca(projection="3d")
    
    delta_x=segment_x*3
    delta_y=segment_y*2+segment_x
    colour='b','r'
    
    for i in range(0,12):
        xi=x_i_ref+delta_x*i; yi=y_i_ref ; a=segment_x;  b=segment_y; z=z_ref
        ax.scatter([xi,xi+a,xi+2*a,xi,xi+a,xi+2*a,xi,xi+a,xi+2*a,],[yi,yi,yi,yi-b,yi-b,yi-b,yi-2*b,yi-2*b,yi-2*b],[z,z,z,z,z,z,z,z,z],c=colour[i%2],s=0.1)
    
    for i in range(0,12):
        xi=x_i_ref+delta_x*i; yi=y_i_ref-delta_y ; a=segment_x;  b=segment_y; z=z_ref
        ax.scatter([xi,xi+a,xi+2*a,xi,xi+a,xi+2*a,xi,xi+a,xi+2*a,],[yi,yi,yi,yi-b,yi-b,yi-b,yi-2*b,yi-2*b,yi-2*b],[z,z,z,z,z,z,z,z,z],c=colour[(i+1)%2],s=0.1)
    
    
    # ax.plot([15,30],[0,0],[20,20],c='r',linewidth=0.6)
    # ax.scatter([15,30],[0,0],[20,20],c='r',s=2)
    
    # heigth=20
    # radius=10
    # x_center=16
    # y_center=16
    # z = np.ones(100)*heigth
    # tetha=np.linspace(0,2*pi,100)
    # x = x_center + radius*np.sin(tetha)
    # y = y_center + radius*np.cos(tetha)
    # ax.plot(x,y,z, color='b',linewidth=0.3)
    # ax.scatter(x_center,y_center,heigth, c='b',s=3)
    
    # y_constant=0
    # radius=7
    # x_center=22
    # z_center=21
    # y = np.ones(100)*y_constant
    # tetha=np.linspace(0,2*pi,100)
    # x = x_center + radius*np.sin(tetha)
    # z = z_center + radius*np.cos(tetha)
    # ax.plot(x,y,z, color='g',linewidth=0.3)
    # ax.scatter(x_center,y_constant,z_center, c='g',s=3)
    
    # x_off = np.ones(12)*6
    # y_off = np.ones(12)*5
    # z=np.ones(12)*16
    # ax.plot([6,10,12,14,18,16,18,14,12,10,6,8]+x_off,[14,14,18,14,14,10,6,6,2,6,6,10]+y_off,z, color='m',linewidth=0.3)
    # ax.scatter([6,10,12,14,18,16,18,14,12,10,6,8]+x_off,[14,14,18,14,14,10,6,6,2,6,6,10]+y_off,z,c='m',s=1)

# inputs are positions of each links
# output is a graph shows a    
def arm_plot (x1,y1,z1,x2,y2,z2):
    ax = plt.gca(projection="3d")
    x,y,z = [0,0,x1,x2],[0,0,y1,y2],[0,0+z_off,z1+z_off,z2+z_off]
    
    ax.scatter(x,y,z, c='r',s=2)
    ax.plot(x,y,z, color='r',linewidth=0.5)
    
    plot_path()
    
    ax.set_xlim3d(-l1-l2,l1+l2)
    ax.set_ylim3d(0,l1+l2)
    ax.set_zlim3d(0,l1+l2+z_off)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    
    plt.show()
      
# inputs initial cordinates,final coordinates, Step
# shows all steps in one fig    
def arm_move (xi,yi,zi,xf,yf,zf,N=10,cont=0):
    tetha0_i,tetha1_i,tetha2_i=IK(xi,yi,zi,-1)
    tetha0_f,tetha1_f,tetha2_f=IK(xf,yf,zf,-1)
    
    # if(tetha1_f-tetha1_i>pi):   delta_tetha1=(2*pi-(tetha1_f-tetha1_i))/N 
    # else :  delta_tetha1=(tetha1_f-tetha1_i)/N
    # if(tetha2_f-tetha2_i>pi):   delta_tetha2=(2*pi-(tetha2_f-tetha2_i))/N
    # else :  delta_tetha2=(tetha2_f-tetha2_i)/N
    # if(tetha0_f-tetha0_i>pi):   delta_tetha0=(2*pi-(tetha0_f-tetha0_i))/N
    # else :  delta_tetha0=(tetha0_f-tetha0_i)/N
    
    delta_tetha1=(tetha1_f-tetha1_i)/N
    delta_tetha2=(tetha2_f-tetha2_i)/N
    delta_tetha0=(tetha0_f-tetha0_i)/N
    plt.figure(1)
    plt.ion()
    i=0
    if cont==1: i=1
    while i<N+1:     
        [x1,y1,z1],[x2,y2,z2]=FK(tetha0_i+delta_tetha0*i,tetha1_i+delta_tetha1*i,tetha2_i+delta_tetha2*i)
        arm_plot (x1,y1,z1,x2,y2,z2)
        plt.draw()
        plt.pause(0.001)
        i=i+1
    plt.ioff()
    plt.show(1)
    plt.close
    
# coordinate system transformations
def cylinder2xy(r,phi):
    x=r*cos(phi)
    y=r*sin(phi)
    return x,y    
def xy2cylinder(x,y):
    r=sqrt(x**2+y**2)
    phi=atan2(y,x)
    return r,phi    

# inputs are circle's center xc,yc; radius r; heigth z; and step amount N;
# outputs are a matrix N*3 dimeansions for angles of each step
def arm_angles_circle(xc,yc,r,z,N=10,cw=-1):
    i=0
    alpha=atan2(yc,xc)
    beta=(2*pi)/N
    x=xc-r*cos(alpha)
    y=yc-r*sin(alpha)
    print(x,y)
    tetha0,tetha1,tetha2=IK(x,y,z,-1)
    angles=np.array([tetha0,tetha1,tetha2])
    i=i+1
    while i<N:     
        x=xc-r*cos(alpha-cw*beta*i)
        y=yc-r*sin(alpha-cw*beta*i)
        print(x,y)
        tetha_0,tetha_1,tetha_2=IK(x,y,z,-1)
        row=np.array([tetha_0,tetha_1,tetha_2])
        angles=np.vstack((angles,row))

        i=i+1
    return angles
    
def arm_angles_circle_90degree1(xc=22,zc=21,y=0,r=7,N=50,cw=-1):
    i=0
    alpha=atan2(zc,xc)
    beta=(2*pi)/N
    x=xc-r*cos(alpha)
    z=zc-r*sin(alpha)-z_off
    print(x,y)
    tetha0,tetha1,tetha2=IK(x,y,z,-1)
    angles=np.array([tetha0,tetha1,tetha2])
    i=i+1
    while i<N:     
        x=xc-r*cos(alpha-cw*beta*i)
        z=zc-r*sin(alpha-cw*beta*i)-z_off
        print(x,y)
        tetha_0,tetha_1,tetha_2=IK(x,y,z,-1)
        row=np.array([tetha_0,tetha_1,tetha_2])
        angles=np.vstack((angles,row))
        i=i+1
    return angles

def arm_angles_circle_90degree2(xc=20,zc=21,y=0,r=7,N=50,cw=-1):
    i=0
    alpha=atan2(zc,xc)
    beta=(2*pi)/N
    x=xc-r*cos(alpha)
    z=zc-r*sin(alpha)-z_off
    print(x,y)
    tetha0,tetha1,tetha2=IK(x,y,z,-1)
    angles=np.array([tetha0,tetha1,tetha2])
    i=i+1
    while i<N:     
        x=xc-r*cos(alpha-cw*beta*i)
        z=zc-r*sin(alpha-cw*beta*i)-z_off
        print(x,y)
        tetha_0,tetha_1,tetha_2=IK(y,x,z,-1)
        row=np.array([tetha_0,tetha_1,tetha_2])
        angles=np.vstack((angles,row))
        i=i+1
    return angles

def arm_draw_with_angleset(angles,mid_step=4):
    for i in range(0,len(angles)-1):
        _,[xi,yi,zi]=FK(angles[i][0],angles[i][1],angles[i][2])
        _,[xf,yf,zf]=FK(angles[i+1][0],angles[i+1][1],angles[i+1][2])
        if i==0: cont=0 
        else: cont=1
        arm_move(xi,yi,zi,xf,yf,zf,mid_step,cont)
        
    # _,[xi,yi,zi]=FK(angles[len(angles)-1][0],angles[len(angles)-1][1],angles[len(angles)-1][2])
    # _,[xf,yf,zf]=FK(angles[0][0],angles[0][1],angles[0][2])
    # arm_move(xi,yi,zi,xf,yf,zf,mid_step,cont=1)

def arm_angles_line(xi,yi,zi,xf,yf,zf,N=20,f=0):
    delta_x=(xf-xi)/N
    delta_y=(yf-yi)/N
    delta_z=(zf-zi)/N
    tetha0,tetha1,tetha2=IK(xi,yi,zi-z_off,-1)
    angles=np.array([tetha0,tetha1,tetha2])
    i=1
    while i<N+f:     
        x=xi+delta_x*i
        y=yi+delta_y*i
        z=zi+delta_z*i-z_off
        tetha_0,tetha_1,tetha_2=IK(x,y,z,-1)
        row=np.array([tetha_0,tetha_1,tetha_2])
        angles=np.vstack((angles,row))
        i=i+1
    return angles



def angles2gcode(angles,x=1,y=1,z=1):
    angles=angles*180/pi
    for i in range (0,len(angles)): print('x'+str("{:.3f}".format(90-angles[i][1]))+' y'+ str("{:.3f}".format(angles[i][1]+angles[i][2])+' z'+str("{:.3f}".format(angles[i][0]))))

def angles2gcode_wo_z(angles,x=1,y=1,z=1):
    angles=angles*180/pi
    for i in range (0,len(angles)): print('x'+str("{:.3f}".format(90-angles[i][1]))+' y'+ str("{:.3f}".format(angles[i][1]+angles[i][2])))

def arm_angles_star(xc,yc,z,l_star,N=10):
    xyz1=[xc-(l_star/2),yc+(l_star/3),z]
    xyz2=[xc-(l_star/6),yc+(l_star/3),z]
    xyz3=[xc,yc+(2*l_star/3),z]
    xyz4=[xc+(l_star/6),yc+(l_star/3),z]
    xyz5=[xc+(l_star/2),yc+(l_star/3),z]
    xyz6=[xc+(l_star/3),yc,z]
    xyz7=[xc+(l_star/2),yc-(l_star/3),z]
    xyz8=[xc+(l_star/6),yc-(l_star/3),z]
    xyz9=[xc,yc-(2*l_star/3),z]
    xyz10=[xc-(l_star/6),yc-(l_star/3),z]
    xyz11=[xc-(l_star/2),yc-(l_star/3),z]
    xyz12=[xc-(l_star/3),yc,z]
    angles1=arm_angles_line(xyz1[0],xyz1[1],xyz1[2],xyz2[0],xyz2[1],xyz2[2],N)
    angles2=arm_angles_line(xyz2[0],xyz2[1],xyz2[2],xyz3[0],xyz3[1],xyz3[2],N)    
    angles3=arm_angles_line(xyz3[0],xyz3[1],xyz3[2],xyz4[0],xyz4[1],xyz4[2],N)
    angles4=arm_angles_line(xyz4[0],xyz4[1],xyz4[2],xyz5[0],xyz5[1],xyz5[2],N)
    angles5=arm_angles_line(xyz5[0],xyz5[1],xyz5[2],xyz6[0],xyz6[1],xyz6[2],N)
    angles6=arm_angles_line(xyz6[0],xyz6[1],xyz6[2],xyz7[0],xyz7[1],xyz7[2],N)
    angles7=arm_angles_line(xyz7[0],xyz7[1],xyz7[2],xyz8[0],xyz8[1],xyz8[2],N)
    angles8=arm_angles_line(xyz8[0],xyz8[1],xyz8[2],xyz9[0],xyz9[1],xyz9[2],N)
    angles9=arm_angles_line(xyz9[0],xyz9[1],xyz9[2],xyz10[0],xyz10[1],xyz10[2],N)
    angles10=arm_angles_line(xyz10[0],xyz10[1],xyz10[2],xyz11[0],xyz11[1],xyz11[2],N)
    angles11=arm_angles_line(xyz11[0],xyz11[1],xyz11[2],xyz12[0],xyz12[1],xyz12[2],N)
    angles12=arm_angles_line(xyz12[0],xyz12[1],xyz12[2],xyz1[0],xyz1[1],xyz1[2],N)
    angles=np.vstack((angles1,angles2,angles3,angles4,angles5,angles6,angles7,angles8,angles9,angles10,angles11,angles12))
    return angles

def arm_goandback(xi,yi,zi,xf,yf,zf,N=20):
     angles1=arm_angles_line(xi,yi,zi,xf,yf,zf,N)  
     angles2=arm_angles_line(xf,yf,zf,xi,yi,zi,N) 
     angles3=arm_angles_line(xi,yi,zi,xf,yf,zf,N)  
     angles4=arm_angles_line(xf,yf,zf,xi,yi,zi,N)     
     angles5=arm_angles_line(xi,yi,zi,xf,yf,zf,N)  
     angles6=arm_angles_line(xf,yf,zf,xi,yi,zi,N)     
     angles=np.vstack((angles1,angles2,angles3,angles4,angles5,angles6))
     return angles
 
    

    
def segment_16(lines,x_off=0,y_off=0,z_off=0):
    xi=x_i_ref+x_off ; yi=y_i_ref-y_off ; a=segment_x;  b=segment_y; z=z_ref+z_off
    points=np.array([[xi,yi,z],[xi+a,yi,z],[xi+2*a,yi,z],[xi,yi-b,z],[xi+a,yi-b,z],[xi+2*a,yi-b,z],[xi,yi-2*b,z],[xi+a,yi-2*b,z],[xi+2*a,yi-2*b,z]])
    N=5
    result=np.zeros(((len(lines)-1)*N+1,3))
    for i in range (0,len(lines)-1):
        if (i==len(lines)-2): f=1
        else: f=0
        a=lines[i]-1; b=lines[i+1]-1
        angles=arm_angles_line(points[a][0],points[a][1],points[a][2],points[b][0],points[b][1],points[b][2],N,f) 
        result[i*N:N*(i+1)+f]=angles  
    return result

def alphabeth (x):
    if (x=='A'): lines= np.array([7,1,3,6,4,6,9]) ;
    elif (x=='B'): lines= np.array([7,8,2,1,3,6,5,6,9,8]) ;
    elif (x=='C'): lines= np.array([3,1,7,9]) ; 
    elif (x=='D'): lines= np.array([7,8,2,1,3,9,8]) ;     
    elif (x=='E'): lines= np.array([3,1,4,5,4,7,9]) ;
    elif (x=='F'): lines= np.array([7,4,5,4,1,3]) ;
    elif (x=='G'): lines= np.array([3,1,7,9,6,5]) ;    
    elif (x=='H'): lines= np.array([7,1,4,6,3,9]) ;    
    elif (x=='I'): lines= np.array([7,9,8,2,1,3]) ; 
    elif (x=='J'): lines= np.array([4,7,9,3]) ;     
    elif (x=='K'): lines= np.array([7,1,4,5,3,5,9]) ;
    elif (x=='L'): lines= np.array([1,7,9]) ;
    elif (x=='M'): lines= np.array([7,1,5,3,9]) ;    
    elif (x=='N'): lines= np.array([7,1,9,3]) ;   
    elif (x=='O'): lines= np.array([7,1,3,9,7]) ;
    elif (x=='P'): lines= np.array([7,1,3,6,4]) ; 
    elif (x=='Q'): lines= np.array([7,1,3,9,5,9,7]) ;     
    elif (x=='R'): lines= np.array([7,1,3,6,4,5,9]) ;
    elif (x=='S'): lines= np.array([7,9,6,4,1,3]) ;
    elif (x=='T'): lines= np.array([8,2,1,3]) ;    
    elif (x=='U'): lines= np.array([1,7,9,3]) ;    
    elif (x=='V'): lines= np.array([1,7,3]) ;
    elif (x=='W'): lines= np.array([1,7,5,9,3]) ; 
    elif (x=='X'): lines= np.array([7,3,5,1,9]) ;     
    elif (x=='Y'): lines= np.array([7,9,3,6,4,1]) ;
    elif (x=='Z'): lines= np.array([1,3,7,9]) ;
    elif (x=='0'): lines= np.array([7,1,3,9,7,3]) ;
    elif (x=='1'): lines= np.array([5,3,9]) ;    
    elif (x=='2'): lines= np.array([1,3,6,4,7,9]) ;
    elif (x=='3'): lines= np.array([1,3,6,5,6,9,7]) ;
    elif (x=='4'): lines= np.array([1,4,6,3,9]) ; 
    elif (x=='5'): lines= np.array([3,1,4,5,9,7]) ;     
    elif (x=='6'): lines= np.array([3,1,7,9,6,4]);
    elif (x=='7'): lines= np.array([1,3,9]) ;
    elif (x=='8'): lines= np.array([7,1,3,6,4,6,9,7]) ;    
    elif (x=='9'): lines= np.array([7,9,3,1,4,6]) ;    
    elif (x=='/'): lines= np.array([7,3]) ;
    elif (x=='['): lines= np.array([3,2,8,9]) ;     
    elif (x==']'): lines= np.array([1,2,8,7]) ;
    elif (x=='{'): lines= np.array([3,2,5,4,5,8,9]) ;
    elif (x=='}'): lines= np.array([1,2,5,6,5,8,7]) ;    
    elif (x=='-'): lines= np.array([5,6]) ;
    elif (x=='_'): lines= np.array([7,9]) ;
    else : 
        lines=np.array([4,1,3,6,5,8]); 
        print('please add to alphabeth',x);
    
    return lines


def write(sentence,row=0):
    x_offset=0
    length=len(sentence)
    space=0
    delta_x=segment_x*3
    delta_y=segment_y*2+segment_x
    delta_z=0.5
    y_offset=row*delta_y
    for i in range (0,length):
        letter=sentence[i]
        if (letter==' '):
            #print('space');
            space=0
        else :
            
            lines=alphabeth(letter)
            x_offset=delta_x*i
            angles=segment_16(lines,x_offset,y_offset,0)
            #arm_draw_with_angleset(angles,mid_step=1)
            angles2gcode(angles)
            
            if (i!=length-1):
                initial_pos=lines[len(lines)-1]
                initial_column=(initial_pos+2)%3
                initial_row=int((initial_pos-1)/3)
                #print('initial',initial_pos)
                
                next_letter=sentence[i+1]
                if (next_letter==' '):
                    space=1
                    next_letter=sentence[i+2]
                    
                
                next_lines=alphabeth(next_letter)
                next_pos=next_lines[0]
                next_column=3+(next_pos+2)%3
                next_row=int((next_pos-1)/3)
                #print('next',next_pos)
            
                xi=x_i_ref+x_offset+segment_x*initial_column
                yi=y_i_ref-segment_y*initial_row-y_offset
                z=z_ref+delta_z
                xf=x_i_ref+x_offset+segment_x*next_column+delta_x*space
                yf=y_i_ref-segment_y*next_row-y_offset
            
                angles_zoff=arm_angles_line(xi, yi, z, xf, yf, z,N=5,f=1)
                #arm_draw_with_angleset(angles_zoff,mid_step=1)
                angles2gcode(angles_zoff)
    return 



write('0123456789',row=0)
# lines = alphabeth('A')
 
# angles_A=segment_16(lines)
# arm_draw_with_angleset(angles_A,mid_step=1)    
# angles_l=arm_goandback(15, 0, 20, 30, 0, 20)
# angles_c=arm_angles_circle(16,16,10,20-z_off,N=100,cw=1)
# angles_star=arm_angles_star(18,15,16,12,10) 
# angles_cc=arm_angles_circle_90degree1()

# arm_draw_with_angleset(angles_l,mid_step=1)   
# arm_draw_with_angleset(angles_c,mid_step=1)
# arm_draw_with_angleset(angles_star,mid_step=1)
# arm_draw_with_angleset(angles_cc,mid_step=1)

# angles2gcode_wo_z(angles_l)
# angles2gcode(angles_c)
# angles2gcode(angles_star)
# angles2gcode_wo_z(angles_cc)
# angles2gcode_wo_z(angles_cc)