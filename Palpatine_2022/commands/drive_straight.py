import commands2
import constants
import wpilib
from subsystems.drivetrain import Drivetrain


class DriveStraight(commands2.CommandBase):
    def __init__(self, drive: Drivetrain, distance: float) -> None:
        super().__init__()

        self.drive = drive
        self.distance = distance
        # note: this targetpos is really more distance from the robot
        self.pos = constants.kunitsPerRotation * (
                self.distance / constants.kwheelCircumference)  # about 5 rotations for 8 feet

        self.rotations = 0
        self.addRequirements([self.drive])

    def execute(self) -> None:
        self.drive.magicDrive(float(self.pos))

        wpilib.SmartDashboard.putNumber("   ClosedLoopError (Left) - ",
                                        self.drive.frontLeft.getClosedLoopError(constants.kPIDLoopIdx))
        wpilib.SmartDashboard.putNumber("   Rotations (Left) - ", (
                self.drive.frontLeft.getSelectedSensorPosition() / constants.kunitsPerRotation))

        wpilib.SmartDashboard.putNumber("   ClosedLoopError (Right) - ",
                                        self.drive.frontRight.getClosedLoopError(constants.kPIDLoopIdx))
        wpilib.SmartDashboard.putNumber("   Rotations (Right) - ", (
                self.drive.frontRight.getSelectedSensorPosition() / constants.kunitsPerRotation))

    def end(self, interrupted: bool) -> None:
        self.drive.stopMotors()

    def isFinished(self) -> bool:
        return self.drive.isNotinMotion()
