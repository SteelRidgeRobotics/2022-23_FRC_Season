import commands2
import ctre
from subsystems.arm import Arm
from wpilib import SmartDashboard


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
            SmartDashboard.putBoolean("In Coast", False)

        else:
            self.arm.baseMotor.motor.setNeutralMode(ctre.NeutralMode.Coast)
            self.arm.midMotor.motor.setNeutralMode(ctre.NeutralMode.Coast)
            self.arm.topMotor.motor.setNeutralMode(ctre.NeutralMode.Coast)
            self.arm.grabberMotor.motor.setNeutralMode(ctre.NeutralMode.Coast)
            SmartDashboard.putBoolean("In Coast", True)

        self.isInCoast = not self.isInCoast
        self.done = True

    def isFinished(self) -> bool:
        return self.done

