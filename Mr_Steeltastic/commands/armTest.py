import commands2
import wpilib
from subsystems.arm import Arm

## create command class that enters numbers into the HoldAtPercentage method of
#  the Arm object.
class ArmTest(commands2.CommandBase):

    def __init__(self, arm: Arm, base, mid, top, grabber) -> None:
        
        super().__init__()
        
        self.arm = arm
        self.addRequirements([self.arm])

        self.base = base
        self.mid = mid
        self.top = top
        self.grabber = grabber
        
        self.start = wpilib.Timer.getFPGATimestamp()

    def execute(self):

        self.arm.holdAtPercentage(self.base, self.mid, self.top, self.grabber)
    
    def end(self, interrupted):
        
        self.arm.holdAtPercentage(0.0, 0.0, 0.0, 0.0)
    
    def isFinished(self):
        """
        Return whether or not the command is finished.
        """

        if wpilib.Timer.getFPGATimestamp() - self.start >= 30:
            
            return True




