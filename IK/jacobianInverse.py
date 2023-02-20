import numpy as np
import math
from robot_arm import *
import pygame

xOffset = 250
yOffset = 250
Arm = RobotArm(xBase=xOffset, yBase=yOffset)

Arm.add_arm_segment(length=75, thetaInit=math.radians(20))
Arm.add_arm_segment(length=75, thetaInit=math.radians(45))
Arm.add_arm_segment(length=75, thetaInit=math.radians(45))
Arm.update_joint_coords()

target = Arm.joints[:, [-1]]

window = pygame.display.set_mode((500,500))
pygame.display.set_caption("Robot Arm Inverse Kinematics")
window.fill((255,255,255))

reach = sum(Arm.lengths)

# add limits
Arm.add_limits()
Arm.def_joint_limit(0, 0, math.pi)
Arm.def_joint_limit(1, -math.pi, math.pi)
Arm.def_joint_limit(2, -math.pi, math.pi)


def move_to_target():
    global Arm, target, reach

    distPerUpdate = 0.01 * reach

    if np.linalg.norm(target - Arm.joints[:, [-1]]) > 0.01 * reach:
        targetVector = (target - Arm.joints[:, [-1]])[:3]
        targetUnitVector = targetVector / np.linalg.norm(targetVector)
        deltaR = distPerUpdate * targetUnitVector
        J = Arm.get_jacobian()
        JInv = np.linalg.pinv(J)
        deltaTheta = JInv.dot(deltaR)
        Arm.update_theta(deltaTheta)
        Arm.update_joint_coords()
        


    angles = Arm.get_angles()
    deltaTheta = []
    # check if the angle of arm is above the max or below the min
    # we do this for each arm, hence the for loop
    for i in range(len(angles)):
        # check if it is less than min
        if angles[i] < Arm.limits[0][i]:
            print("ERROR 1")
            deltaTheta = np.append(deltaTheta, Arm.limits[0][i])
        # check if it is more than max
        elif angles[i] > Arm.limits[1][i]:
            print("ERROR 2")
            deltaTheta = Arm.limits[1][i]
        else:
            deltaTheta = np.append(deltaTheta, Arm.thetas[i])
    print(deltaTheta)
    

def apply_limits_to_arm():
        global Arm
        angles = Arm.get_angles()
        J = Arm.get_jacobian()
        deltaTheta = []
        # check if the angle of arm is above the max or below the min
        # we do this for each arm, hence the for loop
        for i in range(len(angles)):
            # check if it is less than min
            if angles[i] < Arm.limits[0][i]:
                print("ERROR 1")
                deltaTheta = np.append(deltaTheta, Arm.limits[0][i])
            # check if it is more than max
            elif angles[i] > Arm.limits[1][i]:
                print("ERROR 2")
                deltaTheta = Arm.limits[1][i]
            else:
                deltaTheta = np.append(deltaTheta, Arm.thetas[i])
        print("deltaTheta: " + str(deltaTheta))
        Arm.update_theta(deltaTheta)
        Arm.update_joint_coords()

targetPt = (250, 250)

running = True
while running:
    window.fill((255,255,255))
    pygame.draw.circle(window, (255, 0, 0), (250, 250), reach, 5)
    pygame.draw.circle(window, (0, 255, 0), (xOffset, yOffset), 5)

    # draw arm
    for i in range(len(Arm.lengths)):
        pygame.draw.line(window, (0, 0, 255), (Arm.joints[0][i], Arm.joints[1][i]), (Arm.joints[0][i+1], Arm.joints[1][i+1]), 5)

    #draw target
    pygame.draw.circle(window, (0, 0, 0), targetPt, 7)

    # draw joints
    for i in range(len(Arm.joints)):
        pygame.draw.circle(window, (0, 255, 255), (Arm.joints[0][i], Arm.joints[1][i]), 5)
    
    # Run IK code
    move_to_target()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = pygame.mouse.get_pos()
            print(str(click))
            targetPt = (click[0], click[1])
            target = np.array([[click[0],click[1], 0, 1]]).T
            print(str(target))
            print(str(Arm.joints))

            print("ANGLES: " + str(Arm.get_angles()))

            angles = Arm.get_angles()
        
            
    pygame.display.flip()