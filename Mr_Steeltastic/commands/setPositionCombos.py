import commands2
import wpilib
from subsystems.arm import Arm
import ctre
import constants

class SetPositionBaseMid(commands2.CommandBase):
    """
    Moves the base and mid motor into the given position.
    """
    def __init__(self, arm: Arm, basePos, midPos) -> None:
        
        super().__init__()
        
        self.arm = arm
        self.addRequirements([self.arm])

        wpilib.SmartDashboard.putBoolean("Moving Base?", False)
        wpilib.SmartDashboard.putBoolean("Moving Mid?", False)
        self.baseAngle = basePos
        self.midAngle = midPos
        self.arm.baseMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.midMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.timer = wpilib.Timer()
        
    def initialize(self) -> None:
        self.done = False
        self.arm.motorToPos(self.arm.baseMotor, self.baseAngle/constants.BASERATIO)
        self.arm.motorToPos(self.arm.midMotor, self.midAngle/constants.MIDDLERATIO)
        self.timer.start()
        self.midMotorDone = False
        self.baseMotorDone = False
        wpilib.SmartDashboard.putBoolean("Moving Base?", True)
        wpilib.SmartDashboard.putBoolean("Moving Mid?", True)
        wpilib.SmartDashboard.putString("Current Command", "PositionBaseMid")

    def execute(self):
        self.midMotorDone = False
        self.baseMotorDone = False
        wpilib.SmartDashboard.putNumber("Base Timer", self.timer.get())
        wpilib.SmartDashboard.putNumber("Mid Timer", self.timer.get())

        if not self.arm.baseMotor.isMotorPos(self.baseAngle/constants.BASERATIO):
            if self.timer.get() >= 2:
                self.arm.motorToPos(self.arm.baseMotor, self.baseAngle/constants.BASERATIO)
                self.timer.reset()
        else:
            self.baseMotorDone = True

        if not self.arm.midMotor.isMotorPos(self.midAngle/constants.MIDDLERATIO):
            if self.timer.get() >= 2:
                self.arm.motorToPos(self.arm.midMotor, self.midAngle/constants.MIDDLERATIO)
                self.timer.reset()
        else:
            self.midMotorDone = True

        if self.baseMotorDone and self.midMotorDone:
            self.done = True
    
    def end(self, interrupted):
        wpilib.SmartDashboard.putBoolean("Moving Base?", False)
        wpilib.SmartDashboard.putBoolean("Moving Mid?", False)
        wpilib.SmartDashboard.putString("Current Command", "None")
        self.timer.stop()
        wpilib.SmartDashboard.putNumber("Base Time", 0)
        wpilib.SmartDashboard.putNumber("Mid Time", 0)
        self.arm.baseMotor.moveToPos(pos=self.arm.baseMotor.motor.getSelectedSensorPosition(), angle=self.arm.globalBaseAngle)
        self.arm.midMotor.moveToPos(pos=self.arm.midMotor.motor.getSelectedSensorPosition(), angle=self.arm.globalMidAngle)
        
    def isFinished(self):
        """
        Return whether or not the command is finished.
        """
        return self.done
    
class SetPositionMidTop(commands2.CommandBase):
    """
    Moves the mid and top motor into the given position.
    """
    def __init__(self, arm: Arm, midPos, topPos) -> None:
        
        super().__init__()
        
        self.arm = arm
        self.addRequirements([self.arm])

        wpilib.SmartDashboard.putBoolean("Moving Mid?", False)
        wpilib.SmartDashboard.putBoolean("Moving Top?", False)
        self.midAngle = midPos
        self.topAngle = topPos
        self.arm.midMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.topMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.timer = wpilib.Timer()
        
    def initialize(self) -> None:
        self.done = False
        self.arm.motorToPos(self.arm.midMotor, self.midAngle/constants.MIDDLERATIO)
        self.arm.motorToPos(self.arm.topMotor, self.topAngle/constants.TOPRATIO)
        self.timer.start()
        self.midMotorDone = False
        self.topMotorDone = False
        wpilib.SmartDashboard.putBoolean("Moving Mid?", True)
        wpilib.SmartDashboard.putBoolean("Moving Top?", True)
        wpilib.SmartDashboard.putString("Current Command", "PositionMidTop")

    def execute(self):
        self.midMotorDone = False
        self.topMotorDone = False
        wpilib.SmartDashboard.putNumber("Mid Timer", self.timer.get())
        wpilib.SmartDashboard.putNumber("Top Timer", self.timer.get())

        if not self.arm.midMotor.isMotorPos(self.midAngle/constants.MIDDLERATIO):
            if self.timer.get() >= 2:
                self.arm.motorToPos(self.arm.midMotor, self.midAngle/constants.MIDDLERATIO)
                self.timer.reset()
        else:
            self.midMotorDone = True

        if not self.arm.topMotor.isMotorPos(self.topAngle/constants.TOPRATIO):
            if self.timer.get() >= 2:
                self.arm.motorToPos(self.arm.topMotor, self.topAngle/constants.TOPRATIO)
                self.timer.reset()
        else:
            self.topMotorDone = True

        if self.midMotorDone and self.topMotorDone:
            self.done = True
    
    def end(self, interrupted):
        wpilib.SmartDashboard.putBoolean("Moving Mid?", False)
        wpilib.SmartDashboard.putBoolean("Moving Top?", False)
        wpilib.SmartDashboard.putString("Current Command", "None")
        self.timer.stop()
        wpilib.SmartDashboard.putNumber("Mid Time", 0)
        wpilib.SmartDashboard.putNumber("Top Time", 0)
        self.arm.midMotor.moveToPos(pos=self.arm.midMotor.motor.getSelectedSensorPosition(), angle=self.arm.globalMidAngle)
        self.arm.topMotor.moveToPos(pos=self.arm.topMotor.motor.getSelectedSensorPosition(), angle=self.arm.globalTopAngle)
        
    def isFinished(self):
        """
        Return whether or not the command is finished.
        """
        return self.done
    
class SetPositionAll(commands2.CommandBase):
    """
    Moves the base motor into the given position.
    """
    def __init__(self, arm: Arm, basePos, midPos, topPos) -> None:
        
        super().__init__()
        
        self.arm = arm
        self.addRequirements([self.arm])

        wpilib.SmartDashboard.putBoolean("Moving Base?", False)
        wpilib.SmartDashboard.putBoolean("Moving Mid?", False)
        wpilib.SmartDashboard.putBoolean("Moving Top?", False)
        self.baseAngle = basePos
        self.midAngle = midPos
        self.topAngle = topPos
        self.arm.baseMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.midMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.topMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.timer = wpilib.Timer()
        self.baseMotorDone = False
        self.midMotorDone = False
        self.topMotorDone = False
        
    def initialize(self) -> None:
        self.baseMotorDone = False
        self.midMotorDone = False
        self.topMotorDone = False
        self.arm.motorToPos(self.arm.baseMotor, self.baseAngle/constants.BASERATIO)
        self.arm.motorToPos(self.arm.midMotor, self.midAngle/constants.MIDDLERATIO)
        self.arm.motorToPos(self.arm.topMotor, self.topAngle/constants.TOPRATIO)
        self.timer.start()
        wpilib.SmartDashboard.putBoolean("Moving Base?", True)
        wpilib.SmartDashboard.putBoolean("Moving Mid?", True)
        wpilib.SmartDashboard.putBoolean("Moving Top?", True)
        wpilib.SmartDashboard.putString("Current Command", "PositionAll")

    def execute(self):
        wpilib.SmartDashboard.putNumber("Combined Timer", self.timer.get())

        if not self.arm.baseMotor.isMotorPos(self.baseAngle/constants.BASERATIO):
            if self.timer.get() >= 2:
                self.arm.motorToPos(self.arm.baseMotor, self.baseAngle/constants.BASERATIO)
                self.timer.reset()
        else:
            self.baseMotorDone = True

        if not self.arm.midMotor.isMotorPos(self.midAngle/constants.MIDDLERATIO):
            if self.timer.get() >= 2:
                self.arm.motorToPos(self.arm.midMotor, self.midAngle/constants.MIDDLERATIO)
                self.timer.reset()
        else:
            self.midMotorDone = True

        if not self.arm.topMotor.isMotorPos(self.topAngle/constants.TOPRATIO):
            if self.timer.get() >= 2:
                self.arm.motorToPos(self.arm.topMotor, self.topAngle/constants.TOPRATIO)
                self.timer.reset()
        else:
            self.topMotorDone = True
    
    def end(self, interrupted):
        wpilib.SmartDashboard.putBoolean("Moving Arm?", False)
        wpilib.SmartDashboard.putBoolean("Moving Base?", False)
        wpilib.SmartDashboard.putBoolean("Moving Mid?", False)
        wpilib.SmartDashboard.putBoolean("Moving Top?", False)
        wpilib.SmartDashboard.putString("Current Command", "None")
        self.timer.stop()
        self.timer.reset()
        wpilib.SmartDashboard.putNumber("Base Time", 0)
        self.arm.holdAtPos()
        
    def isFinished(self):
        """
        Return whether or not the command is finished.
        """
        return self.baseMotorDone and self.midMotorDone and self.topMotorDone
    
class SetPositionAllInRange(commands2.CommandBase):
    """
    Moves the base motor into the given position.
    """
    def __init__(self, arm: Arm, basePos, midPos, topPos) -> None:
        
        super().__init__()
        
        self.arm = arm
        self.addRequirements([self.arm])

        wpilib.SmartDashboard.putBoolean("Moving Base?", False)
        wpilib.SmartDashboard.putBoolean("Moving Mid?", False)
        wpilib.SmartDashboard.putBoolean("Moving Top?", False)
        self.baseAngle = basePos
        self.midAngle = midPos
        self.topAngle = topPos
        self.arm.baseMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.midMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.topMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.timer = wpilib.Timer()
        self.baseMotorDone = False
        self.midMotorDone = False
        self.topMotorDone = False
        
    def initialize(self) -> None:
        self.baseMotorDone = False
        self.midMotorDone = False
        self.topMotorDone = False
        self.arm.motorToPos(self.arm.baseMotor, self.baseAngle/constants.BASERATIO)
        self.arm.motorToPos(self.arm.midMotor, self.midAngle/constants.MIDDLERATIO)
        self.arm.motorToPos(self.arm.topMotor, self.topAngle/constants.TOPRATIO)
        self.timer.start()
        wpilib.SmartDashboard.putBoolean("Moving Base?", True)
        wpilib.SmartDashboard.putBoolean("Moving Mid?", True)
        wpilib.SmartDashboard.putBoolean("Moving Top?", True)
        wpilib.SmartDashboard.putString("Current Command", "PositionAllRange")

    def execute(self):
        wpilib.SmartDashboard.putNumber("Combined Timer", self.timer.get())

        if not self.arm.baseMotor.isMotorPosInRange(self.baseAngle/constants.BASERATIO):
            if self.timer.get() >= 2:
                self.arm.motorToPos(self.arm.baseMotor, self.baseAngle/constants.BASERATIO)
                self.timer.reset()
        else:
            self.baseMotorDone = True

        if not self.arm.midMotor.isMotorPosInRange(self.midAngle/constants.MIDDLERATIO):
            if self.timer.get() >= 2:
                self.arm.motorToPos(self.arm.midMotor, self.midAngle/constants.MIDDLERATIO)
                self.timer.reset()
        else:
            self.midMotorDone = True

        if not self.arm.topMotor.isMotorPosInRange(self.topAngle/constants.TOPRATIO):
            if self.timer.get() >= 2:
                self.arm.motorToPos(self.arm.topMotor, self.topAngle/constants.TOPRATIO)
                self.timer.reset()
        else:
            self.topMotorDone = True
    
    def end(self, interrupted):
        wpilib.SmartDashboard.putBoolean("Moving Arm?", False)
        wpilib.SmartDashboard.putBoolean("Moving Base?", False)
        wpilib.SmartDashboard.putBoolean("Moving Mid?", False)
        wpilib.SmartDashboard.putBoolean("Moving Top?", False)
        wpilib.SmartDashboard.putString("Current Command", "None")
        self.timer.stop()
        self.timer.reset()
        wpilib.SmartDashboard.putNumber("Base Time", 0)
        self.arm.holdAtPos()
        
    def isFinished(self):
        """
        Return whether or not the command is finished.
        """
        return self.baseMotorDone and self.midMotorDone and self.topMotorDone

class SetPositionCubePickup(commands2.CommandBase):
    """
    Moves the base motor into the given position.
    """
    def __init__(self, arm: Arm) -> None:
        
        super().__init__()
        
        self.arm = arm
        self.addRequirements([self.arm])

        wpilib.SmartDashboard.putBoolean("Moving Base?", False)
        wpilib.SmartDashboard.putBoolean("Moving Mid?", False)
        wpilib.SmartDashboard.putBoolean("Moving Top?", False)
        self.baseAngle = 44500
        self.midAngle = -8750
        self.topAngle = 8821
        self.arm.baseMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.midMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.topMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.timer = wpilib.Timer()
        self.baseMotorDone = False
        self.midMotorDone = False
        self.topMotorDone = False
        
    def initialize(self) -> None:
        self.baseMotorDone = False
        self.midMotorDone = False
        self.topMotorDone = False
        self.baseMidMotorSent = False
        self.arm.motorToPos(self.arm.topMotor, self.topAngle/constants.TOPRATIO)
        self.timer.start()
        wpilib.SmartDashboard.putBoolean("Moving Base?", False)
        wpilib.SmartDashboard.putBoolean("Moving Mid?", False)
        wpilib.SmartDashboard.putBoolean("Moving Top?", True)
        wpilib.SmartDashboard.putString("Current Command", "CubePickup")

    def execute(self):
        wpilib.SmartDashboard.putNumber("Timer", self.timer.get())

        if not self.arm.topMotor.isMotorPosInRange(self.topAngle/constants.TOPRATIO, range=8750):
            if self.timer.get() >= 3:
                self.arm.motorToPos(self.arm.topMotor, self.topAngle/constants.TOPRATIO)
        else:
            self.topMotorDone = True

        if self.topMotorDone and not self.baseMidMotorSent:
            self.arm.motorToPos(self.arm.baseMotor, self.baseAngle/constants.BASERATIO)
            self.arm.motorToPos(self.arm.midMotor, self.midAngle/constants.MIDDLERATIO)
            self.baseMidMotorSent = True

        if self.arm.midMotor.isMotorPosInRange(self.midAngle/constants.MIDDLERATIO):
            self.midMotorDone = True
        
        if self.arm.baseMotor.isMotorPosInRange(self.baseAngle/constants.BASERATIO):
            self.baseMotorDone = True

    
    def end(self, interrupted):
        wpilib.SmartDashboard.putBoolean("Moving Arm?", False)
        wpilib.SmartDashboard.putBoolean("Moving Base?", False)
        wpilib.SmartDashboard.putBoolean("Moving Mid?", False)
        wpilib.SmartDashboard.putBoolean("Moving Top?", False)
        wpilib.SmartDashboard.putString("Current Command", "None")
        self.timer.stop()
        self.timer.reset()
        wpilib.SmartDashboard.putNumber("Base Time", 0)
        self.arm.holdAtPos()
        
    def isFinished(self):
        """
        Return whether or not the command is finished.
        """
        return self.baseMotorDone and self.midMotorDone and self.topMotorDone