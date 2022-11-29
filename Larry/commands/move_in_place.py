import typing
import commands2
from subsystems.swerve_drive import SwerveDrive
import wpilib
import conversions
import constants

class MoveInPlace(commands2.CommandBase):
    def __init__(self,  swerveDrive: SwerveDrive, rightx: typing.Callable[[], float]) -> None:
        super().__init__()
        self.drive = swerveDrive
        #self.units = conversions.convertDegreesToTalonFXUnits(conversions.convertJoystickInputToDegrees(x(), y()))
        self.x = rightx
        self.addRequirements([self.drive])

    def execute(self) -> None:
        self.drive.turnInPlace(conversions.deadband(self.x(), constants.kdeadband))
        wpilib.SmartDashboard.putNumber("Turn Power -", conversions.deadband(self.x(), constants.kdeadband))

    def end(self, interrupted: bool) -> None:
        self.drive.stopAllMotors()

    def isFinished(self) -> bool:
        return False