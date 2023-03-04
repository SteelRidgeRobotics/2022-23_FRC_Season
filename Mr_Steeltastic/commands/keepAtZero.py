import commands2
from subsystems.arm import Arm

class KeepAtZero(commands2.CommandBase):

    def __init__(self, arm: Arm) -> None:

        super().__init__()

        self.arm = arm
        
        self.addRequirements([self.arm])

        
    def execute(self):
        
        self.arm.keepArmsAtZero()