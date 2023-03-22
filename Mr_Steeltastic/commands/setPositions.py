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

        self.isDone = False

        self.moved = False

        self.arm.baseMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.midMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.topMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.grabberMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)

        self.arm.armToPos(0, (-40 * (2048/360)), 0, 0)

    def execute(self):
        #self.arm.baseMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, -0.5)
        #self.arm.holdAtPercentage(-0.135, -0.105, 0.125)
        wpilib.SmartDashboard.putBoolean("Moving Arm?", True)
        #self.arm.armToPos((-30 * (2048 / 360)), (-120 * (2048 / 360)), (0 * (2048 / 360)), 0) 
        self.arm.toggleArm()
        self.isDone = True
        #self.arm.armToPos(60197/constants.BASERATIO, -15196/constants.MIDDLERATIO, 8038/constants.TOPRATIO, 0) #Cube pick up

        #self.arm.armToPos((-30 * (2048 / 360)), (-30*(2048 / 360)), 0, 0) 

        #self.arm.armToPos(self.arm.baseMotor.getCurrentAngle() * (2048 / 360), (-45 * (2048 / 360)), self.arm.topMotor.getCurrentAngle() * (2048 / 360), 0)
        # For cone for future reference: self.arm.holdAtPercentage(0.0, 0.0, 0.145)
    
    def end(self, interrupted):
        wpilib.SmartDashboard.putBoolean("Moving Arm?", False)
        self.arm.holdAtPos()
        
    def isFinished(self):
        """
        Return whether or not the command is finished.
        """
            
        #return wpilib.Timer.getFPGATimestamp() - self.start >= 30
        return self.isDone