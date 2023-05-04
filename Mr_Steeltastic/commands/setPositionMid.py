import commands2
import wpilib
from subsystems.arm import Arm
import ctre
import constants

class SetPositionMid(commands2.CommandBase):
    """
    Moves the mid motor into the given position.
    """
    def __init__(self, arm: Arm, midPos) -> None:
        
        super().__init__()
        
        self.arm = arm
        self.addRequirements([self.arm])

        wpilib.SmartDashboard.putBoolean("Moving Mid?", False)
        self.midAngle = midPos
        self.arm.midMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.timer = wpilib.Timer()
        self.done = False
        
    def initialize(self) -> None:
        self.done = False
        self.arm.motorToPos(self.arm.midMotor, self.midAngle/constants.MIDDLERATIO)
        self.timer.start()
        wpilib.SmartDashboard.putBoolean("Moving Mid?", True)
        wpilib.SmartDashboard.putString("Current Command", "PositionMid")

    def execute(self):
        wpilib.SmartDashboard.putNumber("Mid Timer", self.timer.get())

        if not self.arm.midMotor.isMotorPos(self.midAngle/constants.MIDDLERATIO):
            if self.timer.get() >= 2:
                self.arm.motorToPos(self.arm.midMotor, self.midAngle/constants.MIDDLERATIO)
                self.timer.reset()
        else:
            self.done = True
    
    def end(self, interrupted):
        wpilib.SmartDashboard.putBoolean("Moving Mid?", False)
        wpilib.SmartDashboard.putString("Current Command", "None")
        self.timer.stop()
        self.timer.reset()
        wpilib.SmartDashboard.putNumber("Mid Time", 0)
        self.arm.midMotor.moveToPos(pos=self.arm.midMotor.motor.getSelectedSensorPosition(), angle=self.arm.globalMidAngle)
        
    def isFinished(self):
        """
        Return whether or not the command is finished.
        """
        return self.done