import commands2
import ctre
import wpilib

import constants
from commands.drive_by_guitar import DriveByGuitar
from commands.drive_straight import DriveStraight
from subsystems.drivetrain import Drivetrain

from guitar import Guitar

class RobotContainer:
    def __init__(self) -> None:
        self.driverController = Guitar(constants.kdriverControllerPort)

        self.frontLeft = ctre.TalonFX(constants.kfrontLeft)
        self.backLeft = ctre.TalonFX(constants.kbackLeft)
        self.frontRight = ctre.TalonFX(constants.kfrontRight)
        self.backRight = ctre.TalonFX(constants.kbackRight)

        self.timer = wpilib.Timer

        # subsystems
        self.drive = Drivetrain()

        # chooser
        self.chooser = wpilib.SendableChooser()

        # Add commands to autonomous command chooser
        self.driveStraight = DriveStraight(self.drive, constants.kdistanceToTravel)
        self.chooser.setDefaultOption("Drive Straight", self.driveStraight)

        wpilib.SmartDashboard.putData("Autonomous", self.chooser)

        # ARCADE, OBJECTIVELY WAY BETTER - Pickle_Face5 & Wyatt
        self.drive.setDefaultCommand(DriveByGuitar(self.drive, self.driverController))

    def getAutonomousCommand(self) -> commands2.Command:
        return self.chooser.getSelected()
