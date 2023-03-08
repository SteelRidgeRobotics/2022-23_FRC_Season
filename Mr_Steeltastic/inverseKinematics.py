import numpy as np
import math
# create arm object

class InverseKinematics:
    # init class
    def __init__(self, **kwargs):
        # offsets of base
        self.xBase = kwargs.get('xBase', 0)
        self.yBase = kwargs.get('yBase', 0)
        # create theta array
        self.thetas = np.array([[]], dtype=np.float_)
        # create joint array
        self.joints = np.array([[self.xBase, self.yBase, 0, 1]], dtype=np.float_)
        # create lengths array
        self.lengths = []
        # create limits array
        self.limits = [[],[]]
    # add segments
    def add_segment(self, length, **kwargs):
        # add to joints
        self.joints
        # add to lengths
        # add to thetas
        # limits

    # transform matrix
        # transformation matrix 
        """
        | cos(theta), - sin(theta), 0, x |
        | sin(theta), - cos(theta), 0, y |
        | 0, 0, 1, 0 |
        | 0, 0, 0, 1 |
        """
        # return transformation matrix

    # update joint positions
        # 1st transformation matrix

        # loop
            # get next transformation matrix
            # multiply (use numpy.multpily)
            # append new value to joints
        
        # update the end effector coordiniates
        # multiply endeffecotr coordinates and set it to the last item

    # get jacobian
        # define unit vector "k-hat" pointing along Z axis
        # make jacobian, an empty  array, length 3 and # of joints - 1
        # Utilize cross product to compute each row of the Jacobian matrix
        # record last item (end effector coords)
        # loop for each joint
            # find current joint
            # the item in jacobian joint (i) = the cross product of k-hat, and the difference 
            ## between end effector coords and current joint coords. reshape that into 3, n
        # return the jacobian
    
    
    
    # update thetas

    # get angles
    
    # get limits