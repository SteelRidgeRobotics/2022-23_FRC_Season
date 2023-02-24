import wpilib
import constants
import commands2
from subsystems.drivetrain import Drivetrain
from commands.stationCorrection import StationCorrection
from commands.joystickDrive import JoystickDrive

class RobotContainer:

    def __init__(self):

        self.driverController = wpilib.PS4Controller(0)
        self.train = Drivetrain()

        self.chooser = wpilib.SendableChooser()

        driveForward = StationCorrection(self.train)

        self.chooser.setDefaultOption("Drive Forward", driveForward)

        self.train.setDefaultCommand(JoystickDrive(self.train, lambda: self.driverController.getLeftY(), lambda: self.driverController.getRightX(), lambda: self.driverController.getL1Button(), lambda: self.driverController.getR1Button()))

    def getAutonomousCommand(self) -> commands2.CommandBase:

        return self.chooser.getSelected()