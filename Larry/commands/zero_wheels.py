import typing

import commands2
import constants
import conversions
import wpilib
from subsystems.swerve_drive import SwerveDrive


class ZeroWheels(commands2.CommandBase):


    def __init__(self, swerveDrive: SwerveDrive) -> None:
        

        super().__init__()
        self.drive = swerveDrive

        self.addRequirements([self.drive])

    def execute(self) -> None:

        self.drive.translate(0, 0.25)

    def end(self, interrupted: bool) -> None:

        self.drive.stopAllMotors()

    def isFinished(self) -> bool:
        wpilib.SmartDashboard.putBoolean("Zero Wheels done?", (
                self.drive.leftFrontSwerveModule.isNotinMotion() 
                and self.drive.leftRearSwerveModule.isNotinMotion()
                and self.drive.rightFrontSwerveModule.isNotinMotion()
                and self.drive.rightRearSwerveModule.isNotinMotion()))
        
        return (self.drive.leftFrontSwerveModule.isNotinMotion() 
                and self.drive.leftRearSwerveModule.isNotinMotion()
                and self.drive.rightFrontSwerveModule.isNotinMotion()
                and self.drive.rightRearSwerveModule.isNotinMotion())