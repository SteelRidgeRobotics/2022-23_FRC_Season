import commands2
import ctre
from subsystems.arm import Arm, ArmMotor
import wpilib

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

        wpilib.SmartDashboard.putBoolean(
            "Moving " + self.motor.name, False)

    def initialize(self) -> None:
        self.done = False
        self.timer.start()

        self.motor.moveToPos(self.pos)

        wpilib.SmartDashboard.putBoolean(f"Moving {self.motor.name}", True)
        wpilib.SmartDashboard.putString(
            "Current Command", f"SetPosition {self.motor.name}")

    def execute(self):
        if not self.motor.isMotorPosInRange(self.pos):
            if self.timer.get() >= 2:
                self.motor.moveToPos(self.pos)
                self.timer.reset()
        else:
            self.done = True

    def end(self, interrupted):
        wpilib.SmartDashboard.putBoolean(f"Moving {self.motor.name}", False)
        wpilib.SmartDashboard.putString("Current Command", "None")
        self.timer.stop()
        self.timer.reset()
        self.motor.moveToPos(self.motor.motor.getSelectedSensorPosition())

    def isFinished(self):
        """
        Return whether or not the command is finished.
        """
        return self.done


class InvertSafelyThenSetPos(commands2.CommandBase):
    """
    Sets the motor pos to 0, inverts it, then sets the correct position.

    THE POSITION YOU PASS IN IS INVERTED IN THE INIT. IT SHOULD NOT BE NEGATIVE.
    """

    def __init__(self, motor: ArmMotor, invert: bool, pos: int) -> None:
        super().__init__()

        self.motor = motor
        self.invert = invert
        self.pos = pos
        self.done = False

        self.has_inverted = False

    def initialize(self) -> None:
        self.done = False

        self.has_inverted = False

        self.motor.moveToPos(0)

    def execute(self) -> None:
        if self.motor.motor.getInverted() == self.invert and not self.has_inverted:
            self.done = True

        if self.motor.isMotorPosInRange(0) and not self.has_inverted:
            self.motor.motor.setInverted(self.invert)
            self.motor.moveToPos(-self.pos)
            self.has_inverted = True

        if self.motor.isMotorPosInRange(self.pos) and self.has_inverted:
            self.done = True

    def end(self, interrupted) -> None:
        self.motor.moveToPos(-self.pos)

    def isFinished(self):
        return self.done


class SetPositionAll(commands2.ParallelCommandGroup):
    def __init__(self, arm: Arm, basePos, midPos, topPos):
        super().__init__()
        self.addCommands(
            SetPosition(arm.baseMotor, basePos),
            SetPosition(arm.midMotor, midPos),
            SetPosition(arm.topMotor, topPos),
            SetPosition(arm.grabberMotor, 0)
        )


class ToggleArmCoast(commands2.CommandBase):
    """
    Sets all arm motors to coast (this lets us move the arm when disabled)
    """

    def __init__(self, arm: Arm) -> None:
        super().__init__()

        self.arm = arm
        self.addRequirements([self.arm])
        self.isInCoast = False
        self.done = False

    def initialize(self) -> None:
        self.done = False

    def execute(self):

        if self.isInCoast:
            self.arm.baseMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
            self.arm.midMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
            self.arm.topMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
            self.arm.grabberMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
            wpilib.SmartDashboard.putBoolean("In Coast", False)

        else:
            self.arm.baseMotor.motor.setNeutralMode(ctre.NeutralMode.Coast)
            self.arm.midMotor.motor.setNeutralMode(ctre.NeutralMode.Coast)
            self.arm.topMotor.motor.setNeutralMode(ctre.NeutralMode.Coast)
            self.arm.grabberMotor.motor.setNeutralMode(ctre.NeutralMode.Coast)
            wpilib.SmartDashboard.putBoolean("In Coast", True)

        self.isInCoast = not self.isInCoast
        self.done = True

    def isFinished(self) -> bool:
        return self.done


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
            InvertSafelyThenSetPos(arm.topMotor, False, 0),
            SetPositionAll(arm, 0, -30340, 0)
        )


class PlaceCubeMid(commands2.SequentialCommandGroup):
    def __init__(self, arm: Arm):
        super().__init__()
        self.addCommands(
            MoveBackToHome(arm),
            SetPosition(arm.midMotor, -110912),
            SetPosition(arm.baseMotor, -4964),
            commands2.WaitCommand(0.5),
            InvertSafelyThenSetPos(arm.topMotor, True, 5115)
        )


class MoveCubePickup(commands2.SequentialCommandGroup):
    def __init__(self, arm: Arm):
        super().__init__()
        self.addCommands(
            SetPositionAll(arm, 0, -30340, 0),
            SetPosition(arm.topMotor, 8821),
            SetPosition(arm.midMotor, -
                        8750).alongWith(SetPosition(arm.baseMotor, 44500))
        )

class WaveArm(commands2.SequentialCommandGroup):
    def __init__(self, arm: Arm):
        super().__init__()
        self.addCommands(
            MoveBackToHome(arm),
            SetPosition(arm.midMotor, -45000).alongWith(SetPosition(arm.topMotor, 3900)),
            commands2.WaitCommand(0.75),
            SetPosition(arm.grabberMotor, -3215),
            commands2.WaitCommand(0.25),
            SetPosition(arm.grabberMotor, 3215),
            commands2.WaitCommand(0.25),
            SetPosition(arm.grabberMotor, -3215),
            commands2.WaitCommand(0.25),
            SetPosition(arm.grabberMotor, 3215),
            commands2.WaitCommand(0.25),
            SetPosition(arm.grabberMotor, -3215),
            commands2.WaitCommand(0.25),
            SetPosition(arm.grabberMotor, 3215),
            commands2.WaitCommand(0.25),
            SetPosition(arm.grabberMotor, 0),
            commands2.WaitCommand(1.25),
            MoveBackToHome(arm)
        )
