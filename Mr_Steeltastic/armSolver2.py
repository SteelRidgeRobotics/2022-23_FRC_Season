import math
import pygame

# set up pygame
pygame.init()

windowSize = 800
window = pygame.display.set_mode((windowSize, windowSize))

pygame.display.set_caption("Robot Arm Inverse Kinematics")

window.fill((255, 255, 255))

font = pygame.font.SysFont("Consolas", 20)


def invertCoord(coords):
    """
    Invert coordinate pair. We need this to convert between 
    the normal Cartesian plane with (0, 0) in the lower left corner and the pygame plane with (0, 0) in the upper left corner
    """

    return (coords[0], windowSize - coords[1])


def debugPrint(title, value):

    print(f"{title}: {value}")


def label(screen: pygame.Surface, xy: tuple, text: str, color: tuple):
    """
        Function for creating a label at a certain point. xy is the upper left coordinates.
        """

    screen.blit(font.render(text, False, color), xy)


class ArmSolver2:
    """
    Arm inverse kinematics
    """

    def __init__(self, baseX, baseY, length1, length2):
        """
        Create class. length1 and length2 are the first and second lengths. baseX and baseY are the coordinates on the Cartesian plane that the base joint should be at.
        """

        self.length1 = length1
        self.length2 = length2

        # calculate how far and close arm can reach. with two segments about the same length, the minReach is essentially negligible, but is important when we have different lengths.
        self.maxReach = self.length1 + self.length2
        self.minReach = abs(self.length1 - self.length2)

        self.baseX = baseX
        self.baseY = baseY

        # initial angles for the arm should be 45 degrees. Note that theta2 is calculated relative to theta1.
        self.theta1 = math.radians(45)
        self.theta2 = math.radians(0)

        self.joints = [[self.baseX, self.baseY],
                       [
                           self.baseX + self.length1 * math.cos(self.theta1),
                           self.baseY + self.length1 * math.sin(self.theta1)
                       ],
                       [
                           self.baseX + self.length1 * math.cos(self.theta1) +
                           self.length2 * math.cos(self.theta1 + self.theta2),
                           self.baseY + self.length1 * math.sin(self.theta1) +
                           self.length2 * math.sin(self.theta1 + self.theta2)
                       ]]

        # bool to keep track of whether we are doing the elbow up position or the elbow down position (based on whether elbow is up or down when arm faces forward
        self.elbowUp = True

    def targetToAngles(self, target: tuple):
        """
        Given a target position, return angles needed to move the end effector (final joint) to that position.
        """

        # offset target based on base coordinates (we can do base coordinates other than (0, 0) this way, which is neat.)
        target = ((target[0] - self.baseX), (target[1] - self.baseY))

        # use pythagorean theorem to calculate distance from base to target
        r = math.sqrt(((target[0]**2) + (target[1]**2)))

        # if r is within range of arm calculate
        if self.minReach <= r <= self.maxReach:

            # in the triangle with lengths L1, L2, and R, alpha is the angle opposite r.
            alpha = math.acos(((self.length1**2) + (self.length2**2) -
                               (r**2)) / (2 * self.length1 * self.length2))

            # theta2 and alpha are supplementary, so to find theta2 do 180 - alpha
            self.theta2 = math.radians(180) - alpha

            # psi and beta add up to theta1 in elbowup, and subtract to make theta1 in elbowdown.
            psi = math.atan2(
                (self.length2) * math.sin(self.theta2),
                (self.length1 + ((self.length2) * math.cos(self.theta2))))
            beta = math.atan2(target[1], target[0])

            if (self.elbowUp and self.joints[2][0] >= self.baseX) or (not self.elbowUp and self.joints[2][0] < self.baseX):

                self.theta1 = beta + psi

            elif (not self.elbowUp and self.joints[2][0] >= self.baseX) or (self.elbowUp and self.joints[2][0] < self.baseX):

                self.theta1 = beta - psi

            # this 2D list represents all the joints.
            self.joints = [
                [self.baseX, self.baseY],
                [
                    self.baseX + self.length1 * math.cos(self.theta1),
                    self.baseY + self.length1 * math.sin(self.theta1)
                ],
                [
                    self.baseX + r * math.cos(beta),
                    self.baseY + r * math.sin(beta)
                ]
            ]


def draw(surface: pygame.Surface, arm: ArmSolver2, target: tuple):
    """
    Draw arm and robot body.
    """

    # pass the target into our function that gives us angles from the target
    arm.targetToAngles(invertCoord(target))

    # fill window
    surface.fill((255, 255, 255))

    # draw arm range
    pygame.draw.circle(surface, (255, 100, 100),
                       invertCoord((arm.baseX, arm.baseY)), arm.maxReach)
    pygame.draw.circle(surface, (255, 255, 255),
                       invertCoord((arm.baseX, arm.baseY)), arm.minReach - 2)

    # draw robot
    topleft = invertCoord((arm.baseX - 150, arm.baseY))
    robot = pygame.Rect(topleft[0], topleft[1], 200, arm.baseY)
    pygame.draw.rect(surface, (0, 0, 0), robot)

    # draw arm joint by joint, length by length
    for jointIdx in range(2):

        pygame.draw.line(
            surface, (0, 255, 0),
            invertCoord((arm.joints[jointIdx][0], arm.joints[jointIdx][1])),
            invertCoord(
                (arm.joints[jointIdx + 1][0], arm.joints[jointIdx + 1][1])), 5)

        pygame.draw.circle(
            surface, (0, 0, 255),
            invertCoord((arm.joints[jointIdx][0], arm.joints[jointIdx][1])), 5)

    pygame.draw.circle(surface, (0, 0, 255),
                       invertCoord((arm.joints[2][0], arm.joints[2][1])), 5)

    pygame.draw.circle(surface, (100, 100, 255), (targetX, targetY), 5)

    # invert target x and y so that when we blit it to the surface (0, 0) is in the lower left
    invertX, invertY = invertCoord((targetX, targetY))

    # blit labels like our target coords, the first angle, and the second angle relative to the first angle
    label(window, (5, 5), f"({invertX}, {invertY})", (0, 0, 0))
    label(window, (5, 30), f"Angle 1: {math.degrees(arm.theta1)}", (255, 0, 0))
    label(window, (5, 55), f"Angle 2: {math.degrees(arm.theta2)}", (0, 0, 255))

    # flip (update) display
    pygame.display.flip()


# arm with baseX, baseY, length1, and length2
armSolver = ArmSolver2(windowSize / 2, 30, 220, 220)

# initialize targetX and targetY
targetX, targetY = invertCoord(
    (armSolver.joints[2][0], armSolver.joints[2][1]))

# draw arm
draw(window, armSolver, (0, 0))

# main loop

running = True

while running:

    # draw arm
    draw(window, armSolver, (targetX, targetY))

    # iterate through events in queue
    for event in pygame.event.get():

        # if we quit stop the loop
        if event.type == pygame.QUIT:

            running = False

        elif event.type == pygame.KEYDOWN:

            # if e is pressed toggle whether we calculate elbow up or elbow down
            if event.key == pygame.K_e:

                armSolver.elbowUp = not armSolver.elbowUp
                draw(window, armSolver, (targetX, targetY))

    # list of keys currently being pressed (not using KEYDOWN because that is for when key is initially pressed, this keeps track of keys being held.
    keys = pygame.key.get_pressed()

    # if a or LEFT is held, move targetX left
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:

        targetX -= 0.2

    # if d or RIGHT is held, move targetX right
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:

        targetX += 0.2

    # if w or UP is held, move targetY up
    if keys[pygame.K_w] or keys[pygame.K_UP]:

        targetY -= 0.2

    # if s or DOWN is held, move targetY down
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:

        targetY += 0.2

    # if i is held move robot left
    if keys[pygame.K_i]:

        armSolver.baseX -= 0.2
        targetX -= 0.2

    # if p is held move robot right
    if keys[pygame.K_p]:

        armSolver.baseX += 0.2
        targetX += 0.2
