import math

import numpy as np
import pygame


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
        self.joints = np.array([[self.xBase, self.yBase, 0, 1]], dtype=np.float_).T
        # create lengths array
        self.lengths = []
        # create limits array
        self.limits = np.array([[kwargs.get("maxLimit", math.pi), kwargs.get("minLimit", -math.pi)]], dtype=np.float_).T

    # add segments
    def add_segment(self, **kwargs):
        # add to joints
        self.joints = np.append(self.joints, np.array([[0, 0, 0, 1]]).T, axis=1)
        # add to lengths
        self.lengths.append(kwargs["length"])
        # add to thetas
        self.thetas = np.append(self.thetas, kwargs.get('thetaInit', 0))
        # limits
        maxLimit = kwargs.get("maxLimit", math.pi)
        minLimit = kwargs.get("minLimit", -math.pi)

        self.limits = np.append(self.limits, np.array([[maxLimit, minLimit]]).T, axis=1)

    # transform matrix
    def get_transformation_matrix(self, theta, x, y):
        # return transformation matrix 
        transformationMatrix = np.array([
            [math.cos(theta), -math.sin(theta), 0, x],
            [math.sin(theta), -math.cos(theta), 0, y],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])
        """
        | cos(theta), - sin(theta), 0, x |
        | sin(theta), - cos(theta), 0, y |
        | 0, 0, 1, 0 |
        | 0, 0, 0, 1 |
        """
        # return transformation matrix
        return transformationMatrix

    # update joint positions
    def update_joint_positions(self):
        # 1st transformation matrix
        t = self.get_transformation_matrix(
            self.thetas[0].item(), self.xBase, self.yBase)
        # loop
        for i in range(len(self.lengths) - 1):
            # get next transformation matrix
            t_next = self.get_transformation_matrix(self.thetas[i + 1],
                                                    self.lengths[i + 1], 0)
            # multiply (use numpy.multpily)
            t = np.multiply(t, t_next)
            # append new value to joints 
            # self.joints = np.multiply(self.joints, t).T #MAY NEED TO DO THE NEXT JOINT
            self.joints[:, [i + 1]] = t.dot(np.array([[0, 0, 0, 1]]).T)
        # update the end effector coordiniates (last joint)
        endEffectorCoords = np.array([[self.lengths[-1], 0, 0, 1]]).T
        # multiply endeffector coordinates with coords and set it to the last item
        new_joints = t.dot(endEffectorCoords)
        self.joints[:, [-1]] = new_joints

    # get jacobian
    def get_jacobian(self):
        # define unit vector "k-hat" pointing along Z axis
        unitVector = np.array([[0, 0, 1]], dtype=np.float_)
        # make jacobian, an empty  array, length 3 and # of joints - 1
        jacobian = np.zeros((3, len(self.joints[0, :]) - 1), dtype=np.float_)

        endEffectorCoords = self.joints[:3, [-1]]
        # Utilize cross product to compute each row of the Jacobian matrix
        # loop for each joint
        for i in range(len(self.joints[0, :]) - 1):
            # find current joint
            currentJointCoords = self.joints[:3, [i]]
            # the item in jacobian joint (i) = the cross product of k-hat, and the difference 
            ## between end effector coords and current joint coords. reshape that into 3, n
            jacobian[:, i] = np.cross(
                unitVector, (endEffectorCoords - currentJointCoords).reshape(3, ))

        # return the jacobian
        return jacobian

    # update thetas
    def update_thetas(self, deltaTheta):
        self.thetas += deltaTheta.flatten()

    # get angles

    # get limits
    def get_limits(self):
        return self.limits

    def move_to_target(self, target):
        # global values
        # set distance per update
        distPerUpdate = 0.0625  # * sum(self.lengths)

        # if the distance to move to target is greater than our distance per update
        if np.linalg.norm(target - self.joints[:, -1]):
            # target vector = target - last joint, and reshape to 3
            targetVector = (target - self.joints[:, [-1]])[:3]
            # target unit vector = target vector / the norm of target vector
            targetUnitVector = targetVector / np.linalg.norm(targetVector)
            # delta R = distance per update * target unit vector
            deltaR = distPerUpdate * targetUnitVector
            # create jacobian
            J = self.get_jacobian()
            # get psuedo inverse of jacobian (pinv)
            Jpinv = np.linalg.pinv(J)
            # get the deltaTheta by multiplying delta R by psuedo inverse of jacobian
            deltaTheta = Jpinv.dot(deltaR)
            # get limits
            limits = self.get_limits()
            # check if movement will violate limits for each joint
            for ii, (joint, motion) in enumerate(zip(self.thetas, deltaTheta.flatten())):
                # test lower limit
                if joint + motion < limits[1][ii]:
                    # if motion would violate, set to lower limit
                    deltaTheta[ii] = limits[1][ii]
                # test upper limit
                elif joint + motion > limits[0][ii]:
                    # if motion would violate, set to upper limit
                    deltaTheta[ii] = limits[0][ii]

        # update theta
        self.update_thetas(deltaTheta)
        # update joint coordinates
        self.update_joint_positions()

    def plot(self, window):
        for i in range(len(self.lengths)):
            pygame.draw.line(window, (0, 0, 255), (self.joints[0][i], self.joints[1][i]),
                             (self.joints[0][i + 1], self.joints[1][i + 1]), 5)

        for i in range(len(self.joints) - 1):
            pygame.draw.circle(window, (0, 255, 255), (self.joints[0][i], self.joints[1][i]), 5)
        pygame.display.flip()


pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Robot Arm Inverse Kinematics")
window.fill((255, 255, 255))

font = pygame.font.SysFont('lucidacalligraphy', 10)

Arm = InverseKinematics(xOffset=250, yOffset=250)

Arm.add_segment(length=50.0, maxLimit=math.pi, minLimit=-math.pi)
Arm.add_segment(length=25.0, maxLimit=math.pi, minLimit=-math.pi)

running = True
while running:
    window.fill((255, 255, 255))
    pygame.draw.circle(window, (255, 0, 0), (250, 250), sum(Arm.lengths), 5)
    pygame.draw.circle(window, (0, 255, 0), (250, 250), 5)

    # Run IK code
    click = pygame.mouse.get_pos()
    targetPt = (click[0], click[1])
    target = np.array([[click[0], click[1], 0, 1]]).T
    pygame.draw.circle(window, (0, 0, 0), targetPt, 7)

    Arm.move_to_target(target)
    Arm.plot(window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            """
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = pygame.mouse.get_pos()
            print(str(click))
            targetPt = (click[0], click[1])
            target = np.array([[click[0],click[1], 0, 1]]).T
            print("TARGET: "+ str(target))
            print(str(Arm.joints))

            print("ANGLES: " + str(Arm.get_angles()))
            """

    pygame.display.flip()
