import typing
import commands2
from subsystems.swerve_drive import SwerveDrive
import constants
import conversions
import math

class Translate(commands2.CommandBase):
    def __init__(self,  swerveDrive: SwerveDrive, x: typing.Callable[[], float], y: typing.Callable[[], float]) -> None:
        super().__init__()
        self.drive = swerveDrive
        self.x = x
        self.y = y
        self.addRequirements([self.drive])

    def execute(self) -> None:
        self.angle = conversions.convertJoystickInputToDegrees(conversions.deadband(self.x(), constants.kdeadband), conversions.deadband(self.y(), constants.kdeadband))
        self.magnitude = math.hypot(conversions.deadband(self.x(), constants.kdeadband), conversions.deadband(self.y(), constants.kdeadband))
        self.drive.translate(self.angle, self.magnitude)
        

    def end(self, interrupted: bool) -> None:
        self.drive.stopAllMotors()

    def isFinished(self) -> bool:
        return False