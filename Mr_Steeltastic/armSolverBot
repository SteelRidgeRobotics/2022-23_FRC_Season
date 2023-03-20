import math

def debugPrint(title, value):
    
    print(f"{title}: {value}")


class ArmSolverBot:
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
        
        # bool to keep track of whether we are doing the elbow up position or the elbow down position (based on whether elbow is up or down when arm faces forward
        self.elbowUp = True
    
    def targetToAngles(self, target: tuple):
        """
        Given a target position, return angles needed to move the end effector (final joint) to that position.
        """
        
        # offset target based on base coordinates (we can do base coordinates other than (0, 0) this way, which is neat.)
        target = ((target[0] - self.baseX), (target[1] - self.baseY))
        
        # use pythagorean theorem to calculate distance from base to target
        r = math.sqrt(((target[0] ** 2) + (target[1] ** 2)))
        
        # if r is within range of arm calculate
        if self.minReach <= r <= self.maxReach:
            
            # in the triangle with lengths L1, L2, and R, alpha is the angle opposite r.
            alpha = math.acos(((self.length1 ** 2) + (self.length2 ** 2) - (r ** 2)) / (2 * self.length1 * self.length2))
            
            # theta2 and alpha are supplementary, so to find theta2 do 180 - alpha
            self.theta2 = math.radians(180) - alpha
            
            # psi and beta add up to theta1 in elbowup, and subtract to make theta1 in elbowdown.
            psi = math.atan2((self.length2) * math.sin(self.theta2), (self.length1 + ((self.length2) * math.cos(self.theta2))))
            beta = math.atan2(target[1], target[0])

            if self.elbowUp:

                self.theta1 = beta + psi

            else:

                self.theta1 = beta - psi

            return (math.degrees(self.theta1), math.degrees(self.theta2))
        
        return (None, None)

arm = ArmSolverBot(0, 0, 22, 22)
print(arm.targetToAngles((44 * math.cos(math.radians(45)), 44 * math.sin(math.radians(45)))))