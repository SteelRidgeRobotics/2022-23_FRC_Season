import wpilib
import constants
import commands2
import commands2.button
from subsystems.drivetrain import Drivetrain
from commands.stationCorrection import StationCorrection
from commands.joystickDrive import JoystickDrive

class RobotContainer:

    def __init__(self):

        self.driverController = wpilib.XboxController(constants.DRIVERCONTROLLERPORT)

        self.train = Drivetrain()

        self.chooser = wpilib.SendableChooser()

        stationCorrection = StationCorrection(self.train)

        self.chooser.setDefaultOption("Drive Forward", stationCorrection)

        self.train.setDefaultCommand(JoystickDrive(self.train, lambda: self.driverController.getLeftY(), lambda: self.driverController.getRightX(), lambda: self.driverController.getLeftBumper(), lambda: self.driverController.getRightBumper()))


    def getAutonomousCommand(self) -> commands2.CommandBase:

        return self.chooser.getSelected()