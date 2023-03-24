import commands2
from subsystems.arm import Arm
import wpilib
import ctre
import constants

class MoveArmUp(commands2.CommandBase):

    def __init__(self, arm: Arm) -> None:
        
        super().__init__()
        
        self.arm = arm
        self.addRequirements([self.arm])

        wpilib.SmartDashboard.putBoolean("Moving Arm?", False)
    
        # self.grabber = grabber
        
        self.start = 0.0
    def initialize(self) -> None:
        self.done = False
        self.moved = False
    def execute(self):
        self.arm.baseMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.midMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.topMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.grabberMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        #self.arm.baseMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, -0.5)
        #self.arm.holdAtPercentage(-0.135, -0.105, 0.125)
        wpilib.SmartDashboard.putBoolean("Moving Arm?", True)
        #self.arm.armToPos((-30 * (2048 / 360)), (-120 * (2048 / 360)), (0 * (2048 / 360)), 0) 
        self.arm.armToPosSimulataneously(0, (-40*(2048 / 360)), 0, 0) 
        if self.arm.baseMotor.motor.getSelectedSensorVelocity() != 0 or self.arm.midMotor.motor.getSelectedSensorVelocity() != 0 or self.arm.topMotor.motor.getSelectedSensorVelocity() != 0:
            self.moved = True
        if self.moved and self.arm.baseMotor.motor.getSelectedSensorVelocity() == 0 and self.arm.midMotor.motor.getSelectedSensorVelocity() == 0 and self.arm.topMotor.motor.getSelectedSensorVelocity() == 0:
            self.done = True
        # For cone for future reference: self.arm.holdAtPercentage(0.0, 0.0, 0.145)
    
    def end(self, interrupted):
        wpilib.SmartDashboard.putBoolean("Moving Arm?", False)
        self.arm.holdAtPos()
        
    def isFinished(self):
        """
        Return whether or not the command is finished.
        """
            
        #return wpilib.Timer.getFPGATimestamp() - self.start >= 30
        return self.done