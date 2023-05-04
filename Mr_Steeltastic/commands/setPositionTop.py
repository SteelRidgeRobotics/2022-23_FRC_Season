import commands2
import wpilib
from subsystems.arm import Arm
import ctre
import constants

class SetPositionTop(commands2.CommandBase):
    """
    Moves the top motor into the given position.
    """
    def __init__(self, arm: Arm, topPos) -> None:
        
        super().__init__()
        
        self.arm = arm
        self.addRequirements([self.arm])

        wpilib.SmartDashboard.putBoolean("Moving Top?", False)
        self.topAngle = topPos
        self.arm.topMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.timer = wpilib.Timer()
        self.done = False
        
    def initialize(self) -> None:
        self.done = False
        self.arm.motorToPos(self.arm.topMotor, self.topAngle/constants.TOPRATIO)
        self.timer.start()
        wpilib.SmartDashboard.putBoolean("Moving Top?", True)
        wpilib.SmartDashboard.putString("Current Command", "PositionTop")

    def execute(self):
        wpilib.SmartDashboard.putNumber("Top Timer", self.timer.get())

        if not self.arm.topMotor.isMotorPos(self.topAngle/constants.TOPRATIO):
            if self.timer.get() >= 2:
                self.arm.motorToPos(self.arm.topMotor, self.topAngle/constants.TOPRATIO)
                self.timer.reset()
        else:
            self.done = True
    
    def end(self, interrupted):
        wpilib.SmartDashboard.putBoolean("Moving Top?", False)
        wpilib.SmartDashboard.putString("Current Command", "None")
        self.timer.stop()
        self.timer.reset()
        wpilib.SmartDashboard.putNumber("Top Time", self.timer.get())
        self.arm.topMotor.moveToPos(pos=self.arm.topMotor.motor.getSelectedSensorPosition(), angle=self.arm.globalTopAngle)
        
    def isFinished(self):
        """
        Return whether or not the command is finished.
        """
        return self.done