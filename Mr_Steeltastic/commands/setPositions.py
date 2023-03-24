import commands2
import wpilib
from subsystems.arm import Arm
import ctre
import constants
## create command class that enters numbers into the HoldAtPercentage method of
#  the Arm object.
class SetPositions(commands2.CommandBase):

    def __init__(self, arm: Arm, basePos, midPos, topPos, grabberAngle) -> None:
        
        super().__init__()
        
        self.arm = arm
        self.addRequirements([self.arm])

        wpilib.SmartDashboard.putBoolean("Moving Arm?", False)

        self.baseAngle = basePos
        self.midAngle = midPos
        self.topAngle = topPos
        self.grabberAngle = grabberAngle

        self.moved = False

        self.arm.baseMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.midMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.topMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.grabberMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)

        #self.arm.armToPos(0, (-40 * (2048/360)), 0, 0)
        
        
    def initialize(self) -> None:
        self.done = False
        self.moved = False

    def execute(self):
        wpilib.SmartDashboard.putBoolean("Close Enough", False)
        #self.arm.baseMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, -0.5)
        #self.arm.holdAtPercentage(-0.135, -0.105, 0.125)
        wpilib.SmartDashboard.putBoolean("Moving Arm?", True)
        #self.arm.armToPos((-30 * (2048 / 360)), (-120 * (2048 / 360)), (0 * (2048 / 360)), 0) 
        #self.arm.toggleArm()
        if self.arm.armToPos(self.baseAngle/constants.BASERATIO, self.midAngle/constants.MIDDLERATIO, self.topAngle/constants.TOPRATIO, 0):
            self.done = True
        #self.arm.armToPos(57077/constants.BASERATIO, -33794/constants.MIDDLERATIO, -252/constants.TOPRATIO, 0) #Cube pick up
        
        #wpilib.SmartDashboard.putNumber("Mid Motor Pos", self.arm.midMotor.motor.getSelectedSensorPosition())

        #self.arm.armToPos((-30 * (2048 / 360)), (-30*(2048 / 360)), 0, 0) 

        #self.arm.armToPos(self.arm.baseMotor.getCurrentAngle() * (2048 / 360), (-45 * (2048 / 360)), self.arm.topMotor.getCurrentAngle() * (2048 / 360), 0)
        # For cone for future reference: self.arm.holdAtPercentage(0.0, 0.0, 0.145)
            #wpilib.SmartDashboard.putValue("Pos", self.arm.baseMotor.motor.getSelectedSensorPosition())
            #wpilib.SmartDashboard.putValue("Active Traj Pos", self.arm.baseMotor.motor.getActiveTrajectoryPosition())
    
    def end(self, interrupted):
        wpilib.SmartDashboard.putBoolean("Moving Arm?", False)
        self.arm.holdAtPos()
        
    def isFinished(self):
        """
        Return whether or not the command is finished.
        """
            
        #return wpilib.Timer.getFPGATimestamp() - self.start >= 30
        return self.done