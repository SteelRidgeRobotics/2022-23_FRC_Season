import pygame

from robot_arm import *

pygame.init()
xOffset = 250
yOffset = 250
Arm = RobotArm(xBase=xOffset, yBase=yOffset)

xTargetMax = xOffset + 50
yTargetMax = yOffset - 30

xTargetMin = xOffset - 50
yTargetMin = yOffset + 5

Arm.add_arm_segment(length=21.578000, thetaInit=math.radians(20))
Arm.add_arm_segment(length=22.000000, thetaInit=math.radians(45))
# Arm.add_arm_segment(length=22, thetaInit=math.radians(45))
Arm.update_joint_coords()

target = Arm.joints[:, [-1]]

window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Robot Arm Inverse Kinematics")
window.fill((255, 255, 255))

font = pygame.font.SysFont('lucidacalligraphy', 10)

reach = sum(Arm.lengths)

# add limits
Arm.add_limits()
epsilon = 0.1
Arm.def_joint_limit(0, 0, math.pi)
Arm.def_joint_limit(1, -math.pi, math.pi)
Arm.def_joint_limit(2, -math.pi, math.pi)


# Arm.def_joint_limit(3, -math.pi, math.pi)

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


def move_to_target_with_limits():
    global Arm, target, reach

    distPerUpdate = 0.002 * reach
    angles = Arm.get_angles()

    if np.linalg.norm(target - Arm.joints[:, [-1]]) > 0.002 * reach:
        ## move a little bit in the direction we want to
        targetVector = (target - Arm.joints[:, [-1]])[:3]
        targetUnitVector = targetVector / np.linalg.norm(targetVector)
        deltaR = distPerUpdate * targetUnitVector
        J = Arm.get_jacobian()
        JInv = np.linalg.pinv(J)
        deltaTheta = JInv.dot(deltaR)

        ## check if this movement will violate our constraints
        limits = Arm.get_joint_limits()
        for ii, (_joint, _motion) in enumerate(zip(Arm.thetas, deltaTheta.flatten())):
            ## test lower joint limit
            if _joint + _motion < limits[0][ii]:
                ## if the motion would cause violation, set joint to lower limit
                deltaTheta[ii] = limits[0][ii] - _joint

            ## test upper limit
            elif _joint + _motion > limits[1][ii]:
                ## if the motion would cause violation, set joint to upper limit
                deltaTheta[ii] = limits[1][ii] - _joint

        Arm.update_theta(deltaTheta)
        Arm.update_joint_coords()


def apply_limits_to_arm():
    global Arm
    angles = Arm.get_angles()
    J = Arm.get_jacobian()
    deltaTheta = []

    # apply limits and check which need to be recalculated
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
    # we now have the old angles and our new angle(s) set to its limit
    # do inverse kinematics for the other ones.
    Arm.update_theta(deltaTheta)
    Arm.update_joint_coords()


targetPt = (250, 250)

running = True
while running:
    window.fill((255, 255, 255))
    pygame.draw.circle(window, (255, 0, 0), (250, 250), reach, 5)
    pygame.draw.circle(window, (0, 255, 0), (xOffset, yOffset), 5)

    # draw arm
    for i in range(len(Arm.lengths)):
        pygame.draw.line(window, (0, 0, 255), (Arm.joints[0][i], Arm.joints[1][i]),
                         (Arm.joints[0][i + 1], Arm.joints[1][i + 1]), 5)

    # draw target
    pygame.draw.circle(window, (0, 0, 0), targetPt, 7)

    # draw joints
    for i in range(len(Arm.joints) - 1):
        pygame.draw.circle(window, (0, 255, 255), (Arm.joints[0][i], Arm.joints[1][i]), 5)

    # Run IK code
    move_to_target_with_limits()

    limit0 = font.render(str(Arm.get_joint_limits()[0][0]) + " -> " + str(Arm.get_joint_limits()[1][0]), 1, (0, 0, 0))
    limit1 = font.render(str(Arm.get_joint_limits()[0][1]) + " -> " + str(Arm.get_joint_limits()[1][1]), 1, (0, 0, 0))
    limit2 = font.render(str(Arm.get_joint_limits()[0][2]) + " -> " + str(Arm.get_joint_limits()[1][2]), 1, (0, 0, 0))
    limit3 = font.render(str(Arm.get_joint_limits()[0][3]) + " -> " + str(Arm.get_joint_limits()[1][3]), 1, (0, 0, 0))

    window.blit(limit0, (0, 10))
    window.blit(limit1, (0, 20))
    window.blit(limit2, (0, 30))
    window.blit(limit3, (0, 40))

    angleDisplay = font.render(str(Arm.get_angles()), 1, (0, 0, 0))
    window.blit(angleDisplay, (0, 0))

    click = pygame.mouse.get_pos()
    if click[0] > xTargetMax:
        new_clickX = xTargetMax
        click = (new_clickX, click[1])
    elif click[0] < xTargetMin:
        new_clickX = xTargetMin
        click = (new_clickX, click[1])
    if click[1] < yTargetMax:
        new_clickY = yTargetMax
        click = (click[0], new_clickY)
    elif click[1] > yTargetMin:
        new_clickY = yTargetMin
        click = (click[0], new_clickY)

    targetPt = (click[0], click[1])
    target = np.array([[click[0], click[1], 0, 1]]).T
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
