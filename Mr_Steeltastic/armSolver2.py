import math

class ArmSolver2():
    
    def __init__(self, length1,  length2):

        self.length1 = length1
        self.length2 = length2
    
    def targetToAngles(self, x, y):
        
        r = ((x ** 2) + (y ** 2)) ** 0.5

        alpha = math.acos(((self.length1 ** 2) + (self.length2 ** 2) - r ** 2) / (2 * self.length1 * self.length2))
        theta2 = math.radians(180) - alpha

        psi = math.atan2(self.length2 * math.sin(theta2), (self.length1 + self.length2 * math.cos(theta2)))
        beta = math.atan2(y, x)

        theta1 = beta - psi

        return theta1, theta2
    
as2 = ArmSolver2(100, 100)
print(as2.targetToAngles(100, 100))