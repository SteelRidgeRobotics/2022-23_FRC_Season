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
        self.thetas = np.array([[]], dtype=np.float_)
        # the matrices of the joint coordinates
        self.joints = np.array([[self.xBase, self.yBase, 0, 1]], dtype=np.float_).T
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
        '''update_joint_coords()
            Recompute x and y coordinates of each joint and end effector.
        '''
        
        # "T" is a cumulative transformation matrix that is the result of
        # the multiplication of all transformation matrices up to and including
        # the ith joint of the for loop.
        T = self.get_transformation_matrix(
            self.thetas[0].item(), self.xBase, self.yBase)
        for i in range(len(self.lengths) - 1):
            T_next = self.get_transformation_matrix(
                self.thetas[i+1], self.lengths[i], 0)
            T = T.dot(T_next)
            self.joints[:,[i+1]] = T.dot(np.array([[0,0,0,1]]).T)

        # Update end effector coordinates.
        endEffectorCoords = np.array([[self.lengths[-1],0,0,1]]).T
        self.joints[:,[-1]] = T.dot(endEffectorCoords)

    def get_jacobian(self):
        '''get_jacobian()
            Return the 3 x N Jacobian for the current set of joint angles.
        '''

        # Define unit vector "k-hat" pointing along the Z axis.
        kUnitVec = np.array([[0,0,1]], dtype=np.float_)

        jacobian = np.zeros((3, len(self.joints[0,:]) - 1), dtype=np.float_)
        endEffectorCoords = self.joints[:3,[-1]]

        # Utilize cross product to compute each row of the Jacobian matrix.
        for i in range(len(self.joints[0,:]) - 1):
            currentJointCoords = self.joints[:3,[i]]
            jacobian[:,i] = np.cross(
                kUnitVec, (endEffectorCoords - currentJointCoords).reshape(3,))
        return jacobian
    
    def update_theta(self, deltaTheta):
        self.thetas += deltaTheta.flatten()

    def get_angles(self):
        angles = []
        T = 0
        for i in range(len(self.joints[0,:]) - 1):
            distancex = self.joints[0][i+1] - self.joints[0][i]
            distancey = self.joints[1][i+1] - self.joints[1][i]
            result = np.arctan(distancey/distancex)

            if i > 0:
                # we find the dotProduct of the previous segment and this segment
                dotProduct = (self.joints[0][i] - self.joints[0][i-1]) * distancex + (self.joints[1][i] - self.joints[1][i-1]) * distancey
                cosTheta = dotProduct/(np.abs(self.lengths[i-1])*np.abs(self.lengths[i]))
                result = np.arccos(cosTheta)

            angles.append(result)
        print("angles " + str(angles))

    def add_limits(self):
        self.limits = np.zeros(shape=(2,len(self.joints)))

    def def_joint_limit(self, joint, min, max):
        self.limits[0][joint] = min
        self.limits[1][joint] = max

        
    def get_joint_limits(self):
        return self.limits
