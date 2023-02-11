'''
Copyright (C) 2013 Travis DeWolf
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import numpy as np
import pyglet
from pyglet import *

import Arm


def get_joint_positions():
    """This method finds the (x,y) coordinates of each joint"""

    x = np.array([0,
                  arm.L[0] * np.cos(arm.q[0]),
                  arm.L[0] * np.cos(arm.q[0]) + arm.L[1] * np.cos(arm.q[0] + arm.q[1]),
                  arm.L[0] * np.cos(arm.q[0]) + arm.L[1] * np.cos(arm.q[0] + arm.q[1]) +
                  arm.L[2] * np.cos(np.sum(arm.q))]) + window.width / 2

    y = np.array([0,
                  arm.L[0] * np.sin(arm.q[0]),
                  arm.L[0] * np.sin(arm.q[0]) + arm.L[1] * np.sin(arm.q[0] + arm.q[1]),
                  arm.L[0] * np.sin(arm.q[0]) + arm.L[1] * np.sin(arm.q[0] + arm.q[1]) +
                  arm.L[2] * np.sin(np.sum(arm.q))])

    return np.array([x, y]).astype('int')

class Simulation(pyglet.window.Window):
    def __init__(self):

        pyglet.window.Window.__init__(self, 1000, 600)

        #pyglet.clock.schedule_interval(update, 1/60.0)

        self.step = 0

        self.last_first = 0.0
        self.last_second = 0.0

        self.traj_theta1 = []
        self.traj_theta2 = []

    def set_jps(self):
        self.jps = get_joint_positions()  # get new joint (x,y) positions

    #batch = pyglet.graphics.Batch()
   


    def on_draw(self):
        batch = pyglet.graphics.Batch()
        self.clear()
        batch.draw()
        
        for i in range(3):

            line1 = shapes.Line(self.jps[0][i],
                self.jps[1][i],
                self.jps[0][i + 1],
                self.jps[1][i + 1],
                10,
                color = (50, 225, 30),
                batch = batch
            )
            """
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
            ('v2i',
            (self.jps[0][i], self.jps[1][i],
            self.jps[0][i + 1], self.jps[1][i + 1])))"""


    #@window.event
    def on_mouse_motion(self,x, y, dx, dy):
    # call the inverse kinematics function of the arm
    # to find the joint angles optimal for pointing at
    # this position of the mouse
        label.text = '(x,y) = (%.3f, %.3f)' % (x, y)
        arm.q = arm.inv_kin([x - self.width/2, y])  # get new arm angles
        self.jps = get_joint_positions()  # get new joint (x,y) positions

arm = Arm.Arm3Link(L=np.array([400, 200, 0]))

window = Simulation()
window.set_jps()

label = pyglet.text.Label(
    'Mouse (x,y)', font_name='Times New Roman',
    font_size=36, x=window.width//2, y=window.height//2,
    anchor_x='center', anchor_y='center')

pyglet.app.run()

