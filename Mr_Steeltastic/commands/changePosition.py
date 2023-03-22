import commands2
from subsystems.arm import Arm

class ChangePosition(commands2.InstantCommand):

    def __init__(self, arm: Arm, forward: bool) -> None:
        
        super().__init__()
        
        self.arm = arm
        self.forward = forward

        self.addRequirements([self.arm])

    def execute(self):

        self.arm.cycleIndex = (self.arm.cycleIndex + 1) % (len(self.arm.cycleList)) if self.forward() else (self.arm.cycleIndex - 1) % (len(self.arm.cycleList))