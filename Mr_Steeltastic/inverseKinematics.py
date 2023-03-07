# create arm object

class InverseKinematics:
    # init class
    def __init__(self, **kwargs):
        # offsets of base

        # create theta array

        # create joint array

        # create lengths array

        # create limits array
    
    # add segments
        # add to joints
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