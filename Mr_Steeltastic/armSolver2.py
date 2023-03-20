import math
from operator import invert
from cairo import Surface
import pygame

pygame.init()

windowSize = 600
window = pygame.display.set_mode((windowSize, windowSize))

pygame.display.set_caption("Robot Arm Inverse Kinematics")

window.fill((255, 255, 255))

font = pygame.font.SysFont("Consolas", 20)

def invertCoord(coords):
    
    return (coords[0], windowSize - coords[1])


def debugPrint(title, value):
    
    print(f"{title}: {value}")

def label(screen: Surface, xy: tuple, text: str, color: tuple):

        screen.blit(font.render(text, False, color), xy)


class ArmSolver2:

    def __init__(self, baseX, baseY, length1, length2):

        self.length1 = length1
        self.length2 = length2

        self.maxReach = self.length1 + self.length2
        self.minReach = abs(self.length1 - self.length2)

        self.baseX = baseX
        self.baseY = baseY

        self.theta1 = math.radians(45)
        self.theta2 = math.radians(45)

        self.joints = [
            
                    [self.baseX, 
                    self.baseY],
                       
                    [self.baseX + self.length1 * math.cos(self.theta1), 
                    self.baseY + self.length1 * math.sin(self.theta1)],
                       
                    [self.baseX + self.length1 * math.cos(self.theta1) + self.length2 * math.cos(self.theta2), 
                    self.baseY + self.length1 * math.sin(self.theta1) + self.length2 * math.sin(self.theta2)]
                    ]

        self.elbowUp = True

    def targetToAngles(self, target: tuple):
        
        target = ((target[0] - self.baseX), (target[1] - self.baseY))

        r = math.sqrt(((target[0] ** 2) + (target[1] ** 2)))

        if self.minReach <= r <= self.maxReach:

            alpha = math.acos(((self.length1 ** 2) + (self.length2 ** 2) - (r ** 2)) / (2 * self.length1 * self.length2))

            self.theta2 = (math.radians(180) - alpha) if self.elbowUp else math.radians(180) - alpha

            psi = math.atan2((self.length2) * math.sin(self.theta2), (self.length1 + ((self.length2) * math.cos(self.theta2))))
            beta = math.atan2(target[1], target[0])

            if self.elbowUp:

                self.theta1 = beta + psi

            else:

                self.theta1 = beta - psi

            self.joints = [[self.baseX, self.baseY],
                           [self.baseX + self.length1 * math.cos(self.theta1), self.baseY + self.length1 * math.sin(self.theta1)],
                           [self.baseX + r * math.cos(beta), self.baseY + r * math.sin(beta)]]

def draw(surface: pygame.Surface, arm: ArmSolver2, target: tuple):

    arm.targetToAngles(invertCoord(target))

    surface.fill((255, 255, 255))

    pygame.draw.circle(surface, (255, 100, 100), invertCoord((arm.baseX, arm.baseY)), arm.maxReach)

    pygame.draw.circle(surface, (255, 255, 255), invertCoord((arm.baseX, arm.baseY)), arm.minReach - 2)

    for jointIdx in range(2):
        
        pygame.draw.line(window, (0, 255, 0), 
                         invertCoord((arm.joints[jointIdx][0], arm.joints[jointIdx][1])),
                         invertCoord((arm.joints[jointIdx + 1][0], arm.joints[jointIdx + 1][1])), 5)
        
        pygame.draw.circle(window, (0, 0, 255), invertCoord((arm.joints[jointIdx][0], arm.joints[jointIdx][1])), 5)

    pygame.draw.circle(window, (0, 0, 255), invertCoord((arm.joints[2][0], arm.joints[2][1])), 5)

    pygame.draw.circle(window, (100, 100, 255), (targetX, targetY), 5)

    invertX, invertY = invertCoord((targetX, targetY))

    label(window, (5, 5), f"({invertX}, {invertY})", (0, 0, 0))
    label(window, (5, 30), f"Angle 1: {math.degrees(arm.theta1)}", (255, 0, 0))
    label(window, (5, 55), f"Angle 2: {math.degrees(arm.theta2)}", (0, 0, 255))

    pygame.display.flip()

arm = ArmSolver2(100, 40, 200, 200)

targetX, targetY = invertCoord((arm.joints[2][0], arm.joints[2][1]))

draw(window, arm, (0, 0))

running = True

while running:

    draw(window, arm, (targetX, targetY))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_e:
                
                arm.elbowUp = not arm.elbowUp
                draw(window, arm, (targetX, targetY))

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:

        targetX -= 0.2

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:

        targetX += 0.2

    if keys[pygame.K_w] or keys[pygame.K_UP]:

        targetY -= 0.2

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:

        targetY += 0.2