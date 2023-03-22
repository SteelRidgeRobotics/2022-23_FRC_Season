import commands2
import wpilib
from subsystems.arm import Arm
import ctre
import constants
## create command class that enters numbers into the HoldAtPercentage method of
#  the Arm object.
class SetPositions(commands2.CommandBase):

    def __init__(self, arm: Arm) -> None:
        
        super().__init__()
        
        self.arm = arm
        self.addRequirements([self.arm])

        wpilib.SmartDashboard.putBoolean("Moving Arm?", False)
    
        # self.grabber = grabber
        
        self.start = 0.0

    def execute(self):
        self.arm.baseMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.midMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.topMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.grabberMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        #self.arm.baseMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, -0.5)
        #self.arm.holdAtPercentage(-0.135, -0.105, 0.125)
        wpilib.SmartDashboard.putBoolean("Moving Arm?", True)
        self.arm.armToPos((-30 * (2048 / 360) * constants.BASERATIO), (-120 * (2048 / 360) * constants.MIDDLERATIO), (0 * (2048 / 360) * constants.TOPRATIO), 0) 
        
        #self.arm.armToPos(self.arm.baseMotor.getCurrentAngle() * (2048 / 360), (-45 * (2048 / 360)), self.arm.topMotor.getCurrentAngle() * (2048 / 360), 0)
        # For cone for future reference: self.arm.holdAtPercentage(0.0, 0.0, 0.145)
    
    def end(self, interrupted):
        wpilib.SmartDashboard.putBoolean("Moving Arm?", False)
        self.arm.holdAtPercentage(0.0, 0.0, 0.0)
        
    def isFinished(self):
        """
        Return whether or not the command is finished.
        """
            
        #return wpilib.Timer.getFPGATimestamp() - self.start >= 30
        return False