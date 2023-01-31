import wpilib
import constants
import commands2
from subsystems.drivetrain import Drivetrain
from commands.stationCorrection import DriveForward
from commands.joystickDrive import JoystickDrive

class RobotContainer:

    def __init__(self):

        self.driverController = wpilib.XboxController(0)
        self.train = Drivetrain()

        self.chooser = wpilib.SendableChooser()

        driveForward = DriveForward(self.train, constants.FEETTODRIVE)

        self.chooser.setDefaultOption("Drive Forward", driveForward)

        self.train.setDefaultCommand(JoystickDrive(self.train, lambda: self.driverController.getLeftY(), lambda: self.driverController.getRightX(), lambda: self.driverController.getLeftBumper(), lambda: self.driverController.getRightBumper))

    def getAutonomousCommand(self) -> commands2.CommandBase:

        return self.chooser.getSelected()