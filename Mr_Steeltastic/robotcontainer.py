import wpilib
import constants
import commands2
from commands2.button import JoystickButton
from subsystems.drivetrain import Drivetrain
from subsystems.arm import Arm
from commands.stationCorrection import StationCorrection
from commands.joystickDrive import JoystickDrive
from commands.armTest import ArmTest
from commands.keepAtZero import KeepAtZero

class RobotContainer:

    def __init__(self):

        self.driverController = wpilib.XboxController(constants.DRIVERCONTROLLERPORT)

        self.train = Drivetrain()

        self.arm = Arm()

        self.chooser = wpilib.SendableChooser()

        stationCorrection = StationCorrection(self.train, self.arm)

        self.chooser.setDefaultOption("Drive Forward", stationCorrection)

        self.train.setDefaultCommand(JoystickDrive(self.train, lambda: self.driverController.getLeftY(), lambda: self.driverController.getRightX(), lambda: self.driverController.getLeftBumper(), lambda: self.driverController.getRightBumper()))

        self.arm.setDefaultCommand(KeepAtZero(self.arm))

        # JoystickButton(self.driverController, wpilib.XboxController.Button.kB).whenPressed(ArmTest(self.arm, -15))

        
    def getAutonomousCommand(self) -> commands2.CommandBase:

        return self.chooser.getSelected()