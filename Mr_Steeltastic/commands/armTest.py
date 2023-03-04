import commands2
import wpilib
from subsystems.arm import Arm

## create command class that enters numbers into the HoldAtPercentage method of
#  the Arm object.
class ArmTest(commands2.CommandBase):

    def __init__(self, arm: Arm, grabber) -> None:
        
        super().__init__()
        
        self.arm = arm
        self.addRequirements([self.arm])

    
        self.grabber = grabber
        
        self.start = 0.0

    def execute(self):

        self.arm.midMotor.moveToAngle(self.grabber)
    
    def end(self, interrupted):
        
        self.arm.holdAtPercentage(0.0, 0.0, 0.0, 0.0)
    
    def isFinished(self):
        """
        Return whether or not the command is finished.
        """
            
        return wpilib.Timer.getFPGATimestamp() - self.start >= 30