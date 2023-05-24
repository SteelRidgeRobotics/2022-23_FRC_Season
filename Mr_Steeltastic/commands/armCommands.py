import commands2
import constants
import ctre
import wpilib
from subsystems.arm import Arm, ArmMotor

"""
COMMANDS
"""

class SetPosition(commands2.CommandBase):
    def __init__(self, motor: ArmMotor, pos):
        super().__init__()
        self.motor = motor
        self.pos = pos
        self.addRequirements([self.motor])
        self.timer = wpilib.Timer()
        self.done = False

        wpilib.SmartDashboard.putBoolean("Moving " + self.motor.name + "?", False)
    
    def initialize(self) -> None:
        self.done = False
        self.timer.start()

        self.motor.toPos(self.pos)

        wpilib.SmartDashboard.putBoolean(f"Moving {self.motor.name}?", True)
        wpilib.SmartDashboard.putString("Current Command", f"Position{self.motor.name}")

    def execute(self):
        if not self.motor.isMotorPosInRange(self.pos):
            if self.timer.get() >= 2:
                self.motor.toPos(self.pos)
                self.timer.reset()
        else:
            self.done = True
    
    def end(self, interrupted):
        wpilib.SmartDashboard.putBoolean(f"Moving {self.motor.name}?", False)
        wpilib.SmartDashboard.putString("Current Command", "None")
        self.timer.stop()
        self.timer.reset()
        self.motor.toPos(self.motor.motor.getSelectedSensorPosition())
        
    def isFinished(self):
        """
        Return whether or not the command is finished.
        """
        return self.done
    
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

        if not self.arm.topMotor.isMotorPosInRange(self.topAngle/constants.TOPRATIO):
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
    
"""
COMMAND GROUPS
"""

class SetPositionBaseMid(commands2.ParallelCommandGroup):
    def __init__(self, arm: Arm, basePos, midPos):
        super().__init__()
        self.addCommands(
            SetPosition(arm.baseMotor, basePos),
            SetPosition(arm.midMotor, midPos)
            )
        
class SetPositionMidTop(commands2.ParallelCommandGroup):
    def __init__(self, arm: Arm, midPos, topPos):
        super().__init__()
        self.addCommands(
            SetPosition(arm.midMotor, midPos), 
            SetPosition(arm.topMotor, topPos)
        )

class SetPositionAll(commands2.ParallelCommandGroup):
    def __init__(self, arm: Arm, basePos, midPos, topPos):
        super().__init__()
        self.addCommands(
            SetPosition(arm.baseMotor, basePos),
            SetPosition(arm.midMotor, midPos), 
            SetPosition(arm.topMotor, topPos),
            SetPosition(arm.grabberMotor, 0)
        )

"""
CONTROLLER-CALLED COMMAND GROUPS (commands groups that run from controller inputs)
"""

class MoveToOrigin(commands2.SequentialCommandGroup):
    def __init__(self, arm: Arm):
        super().__init__()
        self.addCommands(
            MoveBackToHome(arm),
            SetPositionAll(arm, 0, 0, 0)
        )

class MoveBackToHome(commands2.SequentialCommandGroup):
    def __init__(self, arm: Arm):
        super().__init__()
        self.addCommands(
            SetPositionAll(arm, 0, -30340, 0)
            #SetPosition(arm.topMotor, 0).alongWith(SetPositionBaseMid(arm, 0, -30340))
        )
        
class PlaceCubeMid(commands2.SequentialCommandGroup):
    def __init__(self, arm: Arm):
        super().__init__()
        self.addCommands(
            MoveBackToHome(arm),
            SetPositionMidTop(arm, -140912, 5115),
            SetPosition(arm.baseMotor, -4964),
            commands2.WaitCommand(0.5),
            SetPosition(arm.topMotor, 5115)
        )

class MoveCubePickup(commands2.SequentialCommandGroup):
    def __init__(self, arm: Arm):
        super().__init__()
        self.addCommands(
            SetPositionAll(arm, 0, -30340, 0),
            SetPositionCubePickup(arm)
        )
