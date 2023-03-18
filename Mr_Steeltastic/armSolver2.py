import numpy as np

class ArmSolver2():
    
    def __init__(self, length1,  length2):

        self.length1 = length1
        self.length2 = length2
    

    def targetToAngles(self, x, y):
        
        r = ((x ** 2) + (y ** 2)) ** 0.5

        alpha = np.arccos((self.length1 ** 2) + (self.length2 ** 2) - r ** 2)
        theta2 = np.pi - alpha

        psi = np.arctan2(self.length2 * np.sin(theta2), (self.length1 + self.length2 * np.cos(theta2)))
        beta = np.arctan2(y, x)

        theta1 = beta - psi

        return np.degrees(theta1), np.degrees(theta2)
    
as2 = ArmSolver2(100, 100)
print(as2.targetToAngles(100, 100))