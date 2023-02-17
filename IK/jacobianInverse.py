import numpy as np
import math
from robot_arm import *
import pygame

xOffset = 150
yOffset = 150
Arm = RobotArm(xBase=xOffset, yBase=yOffset)

Arm.add_arm_segment(length=30, thetaInit=math.radians(10))
Arm.add_arm_segment(length=30, thetaInit=math.radians(15))
Arm.add_arm_segment(length=30, thetaInit=math.radians(20))
Arm.update_joint_coords()

target = Arm.joints[:, [-1]]

window = pygame.display.set_mode((300,300))
pygame.display.set_caption("Robot Arm Inverse Kinematics")
window.fill((255,255,255))



reach = sum(Arm.lengths)
print("\n" + str(Arm.joints))
print("\n [0][0]" + str(Arm.joints[0][0]))
print("\n [0][1]" + str(Arm.joints[0][1]))
print("\n [0][2]" + str(Arm.joints[0][2]))
print("\n [0][3]" + str(Arm.joints[0][3]))

def move_to_target():
    global Arm, target, reach

    distPerUpdate = 0.02 * reach

    if np.linalg.norm(target - Arm.joints[:, [-1]]) > 0.02 * reach:
        targetVector = (target - Arm.joints[:, [-1]])[:3]
        targetUnitVector = targetVector / np.linalg.norm(targetVector)
        deltaR = distPerUpdate * targetUnitVector
        J = Arm.get_jacobian()
        JInv = np.linalg.pinv(J)
        deltaTheta = JInv.dot(deltaR)
        Arm.update_theta(deltaTheta)
        Arm.update_joint_coords()
        pygame.display.flip()

targetPt = (150, 150)

running = True
while running:
    window.fill((255,255,255))
    pygame.draw.circle(window, (255, 0, 0), (150, 150), reach, 5)
    pygame.draw.circle(window, (0, 255, 0), (xOffset, yOffset), 5)

    # draw arm
    pygame.draw.circle(window, (0, 0, 255), (Arm.joints[0][0], Arm.joints[1][0]), 3)
    pygame.draw.circle(window, (0, 0, 255), (Arm.joints[0][1], Arm.joints[1][1]), 3)
    pygame.draw.circle(window, (0, 0, 255), (Arm.joints[0][2], Arm.joints[1][2]), 3)
    pygame.draw.circle(window, (0, 0, 255), (Arm.joints[0][3], Arm.joints[1][3]), 3)
    pygame.draw.line(window, (0, 0, 255), (Arm.joints[0][0], Arm.joints[1][0]), (Arm.joints[0][1], Arm.joints[1][1]))
    pygame.draw.line(window, (0, 0, 255), (Arm.joints[0][1], Arm.joints[1][1]), (Arm.joints[0][2], Arm.joints[1][2]))
    pygame.draw.line(window, (0, 0, 255), (Arm.joints[0][2], Arm.joints[1][2]), (Arm.joints[0][3], Arm.joints[1][3]))

    #draw target
    pygame.draw.circle(window, (0, 0, 0), targetPt, 5)
    
    # Run IK code
    move_to_target()


    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("DOWN!")
            print(str(pygame.mouse.get_pos()))
            print("x =" + str(pygame.mouse.get_pos()[0]))
            print("y =" + str(pygame.mouse.get_pos()[1]))
            click = pygame.mouse.get_pos()
            print(str(click))
            targetPt = (click[0], click[1])
            target = np.array([[click[0],click[1], 0, 1]]).T
            print(str(target))
            print(str(Arm.joints))
            print("THETAS! " + str(Arm.thetas))

            targetVector = (target - Arm.joints[:, [-1]])[:3]
            targetUnitVector = targetVector / np.linalg.norm(targetVector)
            distPerUpdate = 0.02 * reach
            deltaR = distPerUpdate * targetUnitVector
            J = Arm.get_jacobian()
            JInv = np.linalg.pinv(J)
            deltaTheta = JInv.dot(deltaR)
            print("deltaR")
            print(str(deltaR))
            print("deltaTheta")
            print(str(deltaTheta))
            print("jacobian" + str(Arm.get_jacobian()))
            print("Jinv" + str(JInv))

                
                
    pygame.display.flip()