import math
import pygame

pygame.init()

windowSize = 600
window = pygame.display.set_mode((windowSize, windowSize))

pygame.display.set_caption("Robot Arm Inverse Kinematics")

window.fill((255,255,255))

def invertCoord(coords):

    return (coords[0], windowSize - coords[1])

def debugPrint(title, value):

    print(f"{title}: {value}")

class ArmSolver2():
    
    def __init__(self, baseX, baseY, length1,  length2):

        self.length1 = length1
        self.length2 = length2

        self.reach = length1 + length2
        
        self.baseX = baseX
        self.baseY = baseY

        self.joints = [[self.baseX, self.baseY],
                       [self.baseX + self.length1 * math.cos(45), self.baseY + self.length1 * math.sin(45)],
                       [self.baseX + self.length1 * math.cos(45) + self.length2 * math.cos(45), self.baseY + self.length1 * math.sin(45) + self.length2 * math.sin(45)]]

        self.elbowUp = True

    def targetToAngles(self, target: tuple):

        r = math.sqrt(((target[0] ** 2) + (target[1] ** 2)))

        if r <= self.reach:

            alpha = math.acos(((self.length1 ** 2) + (self.length2 ** 2) - (r ** 2)) / (2 * self.length1 * self.length2))
            theta2 = -(math.radians(180) - alpha) if self.elbowUp else math.radians(180) - alpha

            psi = math.atan2(self.length2 * math.sin(theta2), (self.length1 + (self.length2 * math.cos(theta2))))
            beta = math.atan2(target[1], target[0])

            if self.elbowUp:
                
                theta1 = beta + psi

            else:

                theta1 = beta - psi
                
            if theta1 > 0:
                
                if self.elbowUp:

                    self.joints = [[self.baseX, self.baseY],
                                   [self.baseX + self.length1 * math.cos(theta1), self.baseY + self.length1 * math.sin(theta1)],
                                   [self.baseX + self.length1 * math.cos(theta1) + self.length2 * math.cos(theta1 + theta2), self.baseY + self.length1 * math.sin(theta1) + self.length2 * math.sin(theta1 + theta2)]]

                if not self.elbowUp:

                    self.joints = [[self.baseX, self.baseY],
                                   [self.baseX + self.length1 * math.cos(theta1), self.baseY + self.length1 * math.sin(theta1)],
                                   [self.baseX + self.length1 * math.cos(theta1) + self.length2 * math.cos(theta1 + theta2), self.baseY + self.length1 * math.sin(theta1) + self.length2 * math.sin(theta1 + theta2)]]
    
def draw(surface: pygame.Surface, arm: ArmSolver2, mousePos: tuple):

    arm.targetToAngles(invertCoord(mousePos))

    surface.fill((255, 255, 255))

    pygame.draw.circle(window, (0, 0, 255), (arm.joints[0][0], arm.joints[0][1]), 5)

    for jointIdx in range(2):

        pygame.draw.line(window, (0, 255, 0), invertCoord((arm.joints[jointIdx][0], arm.joints[jointIdx][1])), invertCoord((arm.joints[jointIdx + 1][0], arm.joints[jointIdx + 1][1])), 5)
        pygame.draw.circle(window, (0, 0, 255), invertCoord((arm.joints[jointIdx][0], arm.joints[jointIdx][1])), 5)

    pygame.draw.circle(window, (0, 0, 255), invertCoord((arm.joints[2][0], arm.joints[2][1])), 5)
    pygame.draw.circle(window, (255, 0, 0), (mousePos[0], mousePos[1]), 3)

    pygame.display.flip()

arm = ArmSolver2(0, 0, 250, 250)

draw(window, arm, (0, 0))

running = True

while running:

    draw(window, arm, pygame.mouse.get_pos())

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_e:

                arm.elbowUp = not arm.elbowUp