import math

import numpy as np
import pygame

pygame.init()
windowSize = 500


def invertCoord(x, y):
    y = windowSize - y
    return (x, y)


def debugPrint(title, value):
    print(f"{title}: {value}")


class ArmSolver:
    """
    A solver to a two segment arm. Measurements are made in inches
    """

    def __init__(self, **kwargs):
        """
        xBase = the x offset of the whole arm
        yBase = the y offset of the whole arm

        length1 = the length of the first segment in inches
        length2 = the length of the second segment in inches

        thetaInit1 = the initial angle of the base joint in degrees
        thetaInit2 = the initial angle of the middle joint in degrees

        Limits1 = the limits of the base joint in radians [max, min]
        Limits2 = the limits of the middle joint in radians [max, min]
        Limits3 = the limits of the joint at the end of the arm [max, min]

        xReachLimitMax = how far the arm can reach 
        yReachLimitMax = how high arm can reach

        xReachLimitMin = how close the arm can reach 
        yReachLimitMin = how low arm can reach
        """

        self.xBase = kwargs.get("xBase", 0)
        self.yBase = kwargs.get("yBase", 0)

        self.lengths = [kwargs.get("length1", 100), kwargs.get("length2", 100)]
        self.reach = sum(self.lengths)

        self.reachLimits = [[kwargs.get("xReachLimitMax", (windowSize / 2) + self.reach),
                             kwargs.get("yReachLimitMax", (windowSize / 2) + self.reach)],
                            [kwargs.get("xReachLimitMin", (windowSize / 2) - self.reach),
                             kwargs.get("yReachLimitMin", (windowSize / 2) - self.reach)]
                            ]

        self.thetas = [kwargs.get("thetaInit1", 0), kwargs.get("thetaInit2", 0)]

        self.limits = [kwargs.get("limits1", [-math.pi, math.pi]), kwargs.get("limits2", [-math.pi, math.pi]),
                       kwargs.get("limits3", [-math.pi, math.pi]), ]

        point1x = self.xBase + self.lengths[0] * np.cos(self.thetas[0])
        point1y = self.yBase + self.lengths[0] * np.sin(self.thetas[0])

        self.joints = [[self.xBase, self.yBase],
                       [point1x, point1y],
                       [point1x + self.lengths[1] * np.cos(self.thetas[1]),
                        point1y + self.lengths[1] * np.sin(self.thetas[1])]]

    def update_joint_coords(self):
        """
        A method to take the current angles and move the points to those angles
        """

        """
        
        """

        for i in range(len(self.joints) - 1):
            
            self.joints[i + 1] = [self.joints[i][0] + self.lengths[i] * np.cos(self.thetas[i]),
                                  self.joints[i][1] + self.lengths[i] * np.sin(self.thetas[i])]

    def moveToTarget(self, target):
        """
        A method to move arm to go to a certain point, if it can
        """
        # d = np.sqrt(np.power((x2 - x1),2) + np.power((y2-y1),2))

        if target[0] > self.reachLimits[0][0]:

            target[0] = self.reachLimits[0][0]

        elif target[0] < self.reachLimits[1][0]:

            target[0] = self.reachLimits[1][0]

        if target[1] > self.reachLimits[0][1]:

            target[1] = self.reachLimits[0][1]

        elif target[1] < self.reachLimits[1][1]:

            target[1] = self.reachLimits[1][1]

        # print("New target")
        # print(target[0], target[1])
        # print(self.reachLimits[0][0], self.reachLimits[0][1])

        ## check how far away arm is
        d = np.sqrt(np.power((target[0] - self.joints[2][0]), 2) + np.power((target[1] - self.joints[2][1]), 2))

        if d >= 0.0625:

            baseToTarget = np.sqrt(
                np.power((target[0] - self.joints[0][0]), 2) + np.power((target[1] - self.joints[0][1]), 2))
            joint2ToTarget = np.sqrt(
                np.power((target[0] - self.joints[1][0]), 2) + np.power((target[1] - self.joints[1][1]), 2))

            newThetas = [0, 0]

            ## move arm slightly towards target
            pointToTargetAngle = np.arctan((target[1] - self.joints[2][1]) / (target[0] - self.joints[2][0]))
            newTarget = (self.joints[2][0] + (0.0625 * np.cos(pointToTargetAngle)),
                         self.joints[2][1] + (0.0625 * np.sin(pointToTargetAngle)))

            angleToTarget = np.arctan((newTarget[1] - self.joints[0][1]) / (newTarget[0] - self.joints[0][0]))

            # lawOfCosines = np.arccos((a^2 + b^2 - c^2)/(2*a*b)) ## angle is between a & b

            ## get base angle

            newThetas[0] = np.arccos(
                ((np.power(baseToTarget, 2) + np.power(self.lengths[0], 2)) - np.power(joint2ToTarget, 2)) / (
                        2 * baseToTarget * self.lengths[0]))
            # print(str(np.arccos((np.power(baseToTarget, 2) + np.power(self.lengths[0], 2) - np.power(self.lengths[1],2))/(2*baseToTarget*self.lengths[0]))))
            # print(str(np.arccos((np.power(500, 2) + np.power(37, 2) - np.power(100,2))/(2*500*37))))
            # print(str((np.power(500, 2) + np.power(37, 2) - np.power(100,2))/(2*500*37)))
            # print(str((np.power(500, 2) + np.power(37, 2) - np.power(100,2))))
            # print(str((2*500*37)))

            ## get angle of elbow/middle joint

            newThetas[1] = np.arccos(
                ((np.power(self.lengths[0], 2) + np.power(joint2ToTarget, 2)) - np.power(baseToTarget, 2)) / (
                        2 * self.lengths[0] * joint2ToTarget))
            # arccos((l1^2 + l2^2 - bt^2)/2*l1*l2)

            """
            (a ^ 2 + b ^ 2 - c^2)/2ab
            """

            # print(str(newThetas))
            for i in range(len(newThetas)):

                if newThetas[i] > self.limits[i][1]:
                    self.thetas[i] = self.limits[i][1]

                elif newThetas[i] < self.limits[i][0]:

                    self.thetas[i] = self.limits[i][0]

                else:

                    self.thetas[i] = newThetas[i]

            self.update_joint_coords()


arm = ArmSolver(xBase=250, yBase=250)
window = pygame.display.set_mode((windowSize, windowSize))
pygame.display.set_caption("Robot Arm Inverse Kinematics")
window.fill((255, 255, 255))
running = True
font = pygame.font.SysFont('lucidacalligraphy', 10)
while running:
    window.fill((255, 255, 255))
    pygame.draw.circle(window, (0, 255, 0), (250, 250), 5)

    # draw arm
    for i in range(len(arm.lengths)):
        pygame.draw.line(window, (0, 0, 255), (arm.joints[i][0], arm.joints[i][1]),
                         (arm.joints[i + 1][0], arm.joints[i + 1][1]), 5)

    click = pygame.mouse.get_pos()

    targetPt = [click[0], click[1]]

    # draw target
    pygame.draw.circle(window, (0, 0, 0), targetPt, 7)

    # draw joints
    for i in range(len(arm.joints)):
        pygame.draw.circle(window, (0, 255, 255), ((arm.joints[i][0], arm.joints[i][1])), 5)

    arm.moveToTarget(targetPt)
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
