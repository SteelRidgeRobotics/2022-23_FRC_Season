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
from commands.poseArm import PoseArm

class RobotContainer:

    def __init__(self):

        self.driverController = wpilib.XboxController(constants.DRIVERCONTROLLERPORT)
        self.functionsController = wpilib.XboxController(constants.FUNCTIONSCONTROLLERPORT)

        self.train = Drivetrain()

        self.arm = Arm()

        self.chooser = wpilib.SendableChooser()

        stationCorrection = StationCorrection(self.train, self.arm)

        self.chooser.setDefaultOption("Drive Forward", stationCorrection)

        self.train.setDefaultCommand(JoystickDrive(self.train, lambda: self.driverController.getLeftY(), lambda: self.driverController.getRightX(), lambda: self.driverController.getLeftBumper(), lambda: self.driverController.getRightBumper()))

        self.arm.setDefaultCommand(KeepAtZero(self.arm))

        # JoystickButton(self.functionsController, wpilib.XboxController.Button.kB).whenPressed(PoseArm(self.arm, [0, 0, 0, 0, 0]))
        JoystickButton(self.driverController, wpilib.XboxController.Button.kB).whenPressed(ArmTest(self.arm))
        
    def getAutonomousCommand(self) -> commands2.CommandBase:

        return self.chooser.getSelected()