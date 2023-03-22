import commands2
import constants
from subsystems.arm import Arm

class MoveArm(commands2.CommandBase):
    
    def __init__(self, arm: Arm):

        super().__init__()

        self.arm = arm

        self.addRequirements([self.arm])

    def execute(self):
        
        neededPoses = self.arm.cycleList[self.arm.cycleIndex]
        self.arm.armToPos(neededPoses[0], neededPoses[1], neededPoses[2], 0)

    def end(self):

        pass

    def isFinished(self):

        return False