# this is code made from a tutorial at https://nrsyed.com/2017/12/17/animating-the-jacobian-inverse-method-with-an-interactive-matplotlib-plot/
# We had a few issues with just usin ctrl+c and ctrl+v from github so I decided to make my own and change it some

import numpy as np
import math

class RobotArm:
    # like the code that this was based on we can change the place where the base arm joins to the robot
    # If no arguments, they are set to 0.
    # init class
    def __init__(self, **kwargs):
        self.xBase = kwargs.get('xBase', 0)
        self.yBase = kwargs.get('yBase', 0)
        # a list of the arm angles
        self.thetas = np.array([[]], dtype=float)
        # the matrices of the joint coordinates
        self.joints = np.array([[self.xBase, self.yBase, 0, 1]], dtype=float).T
        # a list of all the arm lengths
        self.lengths = []
        
    def add_arm_segment(self, **kwargs):
        """ add_arm_segment(length, thetaInit=0)
                Here we add another segment to the arm. We have to define the length
                and we can define the initial angle of the arm as well (which will come in hand later).
        """
        self.joints = np.append(self.joints, np.array([[0, 0, 0, 1]]).T, axis=1)
        self.lengths.append(kwargs['length'])
        # get initial angle. If nothing entered, it will be 0
        self.thetas = np.append(self.thetas, kwargs.get('thetaInit', 0))
        
    def get_transformation_matrix(self, theta, x, y):
        """
        We learned that you can use matrices to help do inverse kinematics
        """
        transformationMatrix =  np.array([
            [math.cos(theta), -math.sin(theta), 0, x],
            [math.sin(theta), math.cos(theta), 0, y],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
            ])
        
        return transformationMatrix

    def update_joint_coords(self):
        """
        Recompute x & y coordinates of each joint and end effector
        """
        T = self.get_transformation_matrix(self.thetas.item(0), self.xBase, self.yBase)
        for i in range (len(self.lengths) - 1):
            T_next = self.get_transformation_matrix(self.thetas[i+1], self.lengths[i], 0)
            T = T.dot(T_next)
            self.joints[:, [i+1]] = T.dot(np.array([[0, 0, 0, 1]]).T)
        
        # 
        endEffectorCoords = np.array([[self.lengths[-1], 0, 0, 1]]).T
        self.joints[:, [-1]] = T.dot(endEffectorCoords)

    def get_jacobian(self):
        """
        Return the 3 x n Jacobian for current set of joint angles.
        """

        kUnitVec = np.array([[0,0,1]], dtype=float)

        jacobian = np.zeros((3, len(self.joints[0,:]) - 1), dtype=float)
        endEffectorCoords = self.joints[:, [-1]]

        # Utilize cross product to compute each row of the Jacobian matrix.
        print(str(endEffectorCoords))
        print("Up: endEffectorCorrds.")
        for i in range(len(self.joints[0, :]) - 1):
            currentJointCoords = self.joints[:3,[-1]]
            print("Down: currentJointCoords \n" + str(currentJointCoords))
            jacobian[:,i] = np.cross(kUnitVec, np.subtract(endEffectorCoords, currentJointCoords)).reshape(3,)

            return jacobian
    def update_theta(self, deltaTheta):
        self.thetas += deltaTheta.flatten()
