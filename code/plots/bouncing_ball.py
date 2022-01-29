#!/usr/bin/env python3
# code/plots/bouncing_ball.py
# {{{
# This code accompanies the book _Python for MATLAB Development:
# Extend MATLAB with 300,000+ Modules from the Python Package Index_ 
# ISBN 978-1-4842-7222-0 | ISBN 978-1-4842-7223-7 (eBook)
# DOI 10.1007/978-1-4842-7223-7
# https://github.com/Apress/python-for-matlab-development
# 
# Copyright © 2022 Albert Danial
# 
# MIT License:
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
# }}}
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from copy import copy
A  = 0.08    # bowl shape:  y = A*x^2
dt = 1.0/500 # time step, seconds
T  = np.arange(0, 20, dt)
n_iter = len(T)
damping = 0.9997
restitution = 0.995
ball_radius = 0.3
history_x, history_y = [], []
point, trace = None, None

def timestep(pos,vel):
    new_pos = copy(pos)
    new_vel = copy(vel)
    new_vel[1] += -9.8*dt
    new_vel    *= damping
    new_pos[0] += new_vel[0]*dt
    new_pos[1] += new_vel[1]*dt
    bowl_y = A*new_pos[0]**2
    if new_pos[1] < bowl_y:
        # hit the bowl, bounce back
        normal = np.array([-2*A*new_pos[0],1])
        normal /= np.linalg.norm(normal)
        new_vel += -2*new_vel.dot(normal)*normal
        new_pos[1] = bowl_y
    return new_pos, new_vel

def run_simulation():
    nX = 21
    pos  = np.zeros((n_iter,2))
    pos[0,:] = np.array([-3., 3.]) # initial position, m
    vel = np.array([0.5, 0])       # initial velocity, m/s
    bowl = np.zeros((nX,2))
    bowl[:,0] = np.linspace(-3.5, 3.5, num=nX)
    X         = bowl[:,0]
    bowl[:,1] = A*X**2
    # centerline is the curve offset from the parabolic
    # bowl by the radius of the ball; it is where the
    # ball's center appears to bounce
    den = 1/np.sqrt(1 + (2*A*X)**2)
    centerline = np.zeros((nX,2))
    centerline[:,0] = X + 2*A*ball_radius*X*den
    centerline[:,1] = A*X**2 - ball_radius*den
    for i in range(1,n_iter):
        pos[i], vel = timestep(pos[i-1],vel)
    return bowl, centerline, pos, vel

def init(bowl, centerline):
    global point, trace
    fig, ax = plt.subplots()
    plt.plot(bowl[:,0],bowl[:,1],':')
    plt.plot(centerline[:,0],centerline[:,1])
    plt.ylim([-1,4])
    ax.set_aspect('equal')
    point, = ax.plot([], [], 'o', markersize=25)
    trace, = ax.plot([], [], ',-', lw=1)
    return fig

def animate(i):
    global history_x, history_y
    if i == 0:
        history_x.clear()
        history_y.clear()
    history_x.append(pos[i,0])
    history_y.append(pos[i,1])
    point.set_data(pos[i,0], pos[i,1])
    trace.set_data(history_x, history_y)
    return point, trace

bowl, centerline, pos, vel = run_simulation()
fig = init(bowl, centerline)
ani = animation.FuncAnimation(
    fig, animate, n_iter, interval=dt*1000, blit=True)
plt.show()
