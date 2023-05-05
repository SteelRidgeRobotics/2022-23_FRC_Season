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