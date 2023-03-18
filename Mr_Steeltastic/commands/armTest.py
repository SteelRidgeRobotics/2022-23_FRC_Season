import commands2
import wpilib
from subsystems.arm import Arm
import ctre
## create command class that enters numbers into the HoldAtPercentage method of
#  the Arm object.
class ArmTest(commands2.CommandBase):

    def __init__(self, arm: Arm) -> None:
        
        super().__init__()
        
        self.arm = arm
        self.addRequirements([self.arm])
    
        # self.grabber = grabber
        
        self.start = 0.0

    def execute(self):
        self.arm.baseMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.midMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.topMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.grabberMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.topMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, 0.15)
        #self.arm.holdAtPercentage(-0.135, -0.105, 0.125)

        # For cone for future reference: self.arm.holdAtPercentage(0.0, 0.0, 0.145)
    
    def end(self, interrupted):
        
        self.arm.holdAtPercentage(0.0, 0.0, 0.0)
        
    def isFinished(self):
        """
        Return whether or not the command is finished.
        """
            
        #return wpilib.Timer.getFPGATimestamp() - self.start >= 30
        return False