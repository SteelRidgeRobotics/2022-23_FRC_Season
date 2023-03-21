import commands2
import wpilib
from commands2.button import JoystickButton

import constants
from commands.armTest import ArmTest
from commands.joystickDrive import JoystickDrive
from commands.keepAtZero import KeepAtZero
from commands.stationCorrectionMobility import StationCorrection
from commands.timedDrive import TimedDrive
from subsystems.arm import Arm
from subsystems.drivetrain import Drivetrain
from commands.joystickControlArm import JoystickControlArm


class RobotContainer:

    def __init__(self):
        self.driverController = wpilib.XboxController(constants.DRIVERCONTROLLERPORT)
        self.functionsController = wpilib.XboxController(constants.FUNCTIONSCONTROLLERPORT)

        self.train = Drivetrain()

        self.arm = Arm()

        self.chooser = wpilib.SendableChooser()

        stationCorrection = StationCorrection(self.train, self.arm)

        self.chooser.setDefaultOption("Auto Charging Station", stationCorrection)
        self.chooser.addOption("Timed Drive", TimedDrive(self.train))

        wpilib.SmartDashboard.putData("Autonomoues", self.chooser)

        self.train.setDefaultCommand(JoystickDrive(self.train, lambda: self.driverController.getLeftY(),
                                                   lambda: self.driverController.getRightX(),
                                                   lambda: self.driverController.getLeftBumper(),
                                                   lambda: self.driverController.getRightBumper(),
                                                   lambda: self.driverController.getAButtonReleased()))

        self.arm.setDefaultCommand(KeepAtZero(self.arm))

        self.arm.setDefaultCommand(JoystickControlArm(self.arm, lambda: self.functionsController.getLeftBumper(), lambda: self.functionsController.getRightBumper(), lambda: self.functionsController.getLeftY(), lambda: -self.functionsController.getRightY(), lambda: self.functionsController.getRightTriggerAxis(), lambda: self.functionsController.getLeftTriggerAxis(), lambda: self.functionsController.getXButton(), lambda: self.functionsController.getYButton()))

        # JoystickButton(self.functionsController, wpilib.XboxController.Button.kB).whenPressed(PoseArm(self.arm, [0, 0, 0, 0, 0]))

        # JoystickButton(self.driverController, wpilib.XboxController.Button.kB).whenPressed(ArmTest(self.arm))
        # JoystickButton(self.driverController, wpilib.XboxController.Button.kA).whenPressed(SetGrabber(self.arm, lambda: self.driverController.getAButton()))

        JoystickButton(self.driverController, wpilib.XboxController.Button.kB).whenPressed(ArmTest(self.arm))
        # JoystickButton(self.driverController, wpilib.XboxController.Button.kA).whenPressed(SetGrabber(self.arm))

    def getAutonomousCommand(self) -> commands2.CommandBase:
        return self.chooser.getSelected()
