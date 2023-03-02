import commands2
from subsystems.arm import Arm

## create command class that enters numbers into the HoldAtPercentage method of the Arm object.
class ArmTest(commands2.CommandBase):
    def __init__(self, arm: Arm, base, mid, top, grabber) -> None:
        super().__init__()
        self.arm = arm
        
        self.addRequirements([self.arm])
    
    def execute(self):
        self.arm.HoldAtPercentage(base, mid, top, grabber)
    
    def end(self, interrupted):
        self.arm.HoldAtPercentage(0.0, 0.0, 0.0, 0.0)
    
    def isFinished(self):
        ## Will keep doing this command, unless we make a statement that will
        ## return true once the command is "finished"
        return False




