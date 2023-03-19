# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 12:29:50 2023

@author: arthu
"""

G           = 6.67e-11                  # constant G
Ms          = 2.0e30                    # sun
Me          = 5.972e24                  # earth        
AU          = 1.5e11                    # earth sun distance
daysec      = 24.0*60*60                # seconds of a day
e_ap_v      = 29290                     # earth velocity at aphelion
gravconst_e = G*Me*Ms
# setup the starting conditions
# earth
xe,ye,ze    = 1.0167*AU,0,0
xve,yve,zve = 0,e_ap_v,0
# sun
xs,ys,zs    = 0,0,0
xvs,yvs,zvs = 0,0,0
t           = 0.0
dt          = 1*daysec # every frame move this time
xelist,yelist,zelist = [],[],[]
xslist,yslist,zslist = [],[],[]
# start simulation
while t<10*365*daysec:
    ################ earth #############
    # compute G force on earth
    rx,ry,rz = xe - xs, ye - ys, ze - zs
    modr3_e = (rx**2+ry**2+rz**2)**1.5
    fx_e = -gravconst_e*rx/modr3_e
    fy_e = -gravconst_e*ry/modr3_e
    fz_e = -gravconst_e*rz/modr3_e
    
    # update quantities how is this calculated?  F = ma -> a = F/m
    xve += fx_e*dt/Me
    yve += fy_e*dt/Me
    zve += fz_e*dt/Me
    
    # update position
    xe += xve*dt
    ye += yve*dt 
    ze += zve*dt
    
    # save the position in list
    xelist.append(xe)
    yelist.append(ye)
    zelist.append(ze)
    
    ################ the sun ###########
    # update quantities how is this calculated?  F = ma -> a = F/m
    xvs += -fx_e*dt/Ms
    yvs += -fy_e*dt/Ms
    zvs += -fz_e*dt/Ms
    
    # update position
    xs += xvs*dt
    ys += yvs*dt 
    zs += zvs*dt
    xslist.append(xs)
    yslist.append(ys)
    zslist.append(zs)
    
    # update dt
    t +=dt
    

import matplotlib.pyplot as plt
from matplotlib import animation

fig, ax = plt.subplots(figsize=(10,10))
ax.set_aspect('equal')
ax.grid()

line_e,     = ax.plot([],[],'-g',lw=1,c='blue')
point_e,    = ax.plot([AU], [0], marker="o"
                      , markersize=4
                      , markeredgecolor="blue"
                      , markerfacecolor="blue")
text_e      = ax.text(AU,0,'Earth')

point_s,    = ax.plot([0], [0], marker="o"
                      , markersize=7
                      , markeredgecolor="yellow"
                      , markerfacecolor="yellow")
text_s      = ax.text(0,0,'Sun')

exdata,eydata = [],[]                   # earth track
sxdata,sydata = [],[]                   # sun track

print(len(xelist))

def update(i):
    exdata.append(xelist[i])
    eydata.append(yelist[i])
    
    line_e.set_data(exdata,eydata)
    point_e.set_data(xelist[i],yelist[i])
    text_e.set_position((xelist[i],yelist[i]))

    point_s.set_data(xslist[i],yslist[i])
    text_s.set_position((xslist[i],yslist[i]))
    ax.axis('equal')
    ax.set_xlim(-3*AU,3*AU)
    ax.set_ylim(-3*AU,3*AU)

    return line_e,point_s,point_e,text_e,text_s

anim = animation.FuncAnimation(fig
                                ,func=update
                                ,frames=len(xelist)
                                ,interval=1
                                ,blit=True)
plt.show()

