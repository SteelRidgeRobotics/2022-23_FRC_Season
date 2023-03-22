import commands2
import constants
from subsystems.arm import Arm
from armSolverBot import ArmSolverBot

class MoveArm(commands2.CommandBase):
    
    def __init__(self, arm: Arm):

        super().__init__()

        self.arm = arm

        self.addRequirements([self.arm])

    def execute(self):
        
        neededPoses = self.arm.cycleList

    def end(self, interrupted: bool):
        pass
    def isFinished(self):

        return False