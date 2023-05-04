import commands2
import wpilib
from subsystems.arm import Arm
import ctre
import constants

class SetPositionBase(commands2.CommandBase):
    """
    Moves the base motor into the given position.
    """
    def __init__(self, arm: Arm, basePos) -> None:
        
        super().__init__()
        
        self.arm = arm
        self.addRequirements([self.arm])

        wpilib.SmartDashboard.putBoolean("Moving Base?", False)
        self.baseAngle = basePos
        self.arm.baseMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.timer = wpilib.Timer()
        self.done = False
        
    def initialize(self) -> None:
        self.done = False
        self.arm.motorToPos(self.arm.baseMotor, self.baseAngle/constants.BASERATIO)
        self.timer.start()
        self.timer.reset()
        wpilib.SmartDashboard.putBoolean("Moving Base?", True)
        wpilib.SmartDashboard.putString("Current Command", "PositionBase")

    def execute(self):
        wpilib.SmartDashboard.putNumber("Base Timer", self.timer.get())

        if not self.arm.baseMotor.isMotorPos(self.baseAngle/constants.BASERATIO):
            if self.timer.get() >= 2:
                self.arm.motorToPos(self.arm.baseMotor, self.baseAngle/constants.BASERATIO)
                self.timer.reset()
        else:
            self.done = True
    
    def end(self, interrupted):
        wpilib.SmartDashboard.putBoolean("Moving Arm?", False)
        wpilib.SmartDashboard.putBoolean("Moving Base?", False)
        wpilib.SmartDashboard.putString("Current Command", "None")
        self.timer.stop()
        wpilib.SmartDashboard.putNumber("Base Time", 0)
        self.arm.baseMotor.moveToPos(pos=self.arm.baseMotor.motor.getSelectedSensorPosition(), angle=self.arm.globalBaseAngle)
        
    def isFinished(self):
        """
        Return whether or not the command is finished.
        """
        return self.done
