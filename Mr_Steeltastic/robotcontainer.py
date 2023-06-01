import commands2
import wpilib
from commands2.button import JoystickButton

import constants
from commands.joystickDrive import JoystickDrive
from commands.autoDock import StationCorrectionMobility
from commands.timedDrive import TimedDrive
from subsystems.arm import Arm, TickArm
from subsystems.drivetrain import Drivetrain
from commands.autoDock import StationCorrection
from commands.setGrabber import SetGrabber
from commands.armCommands import *
from guitar import Guitar


class RobotContainer:

    def __init__(self):

        self.driverController = wpilib.XboxController(
            constants.DRIVERCONTROLLERPORT)
        if constants.USINGGUITARCONTROLLER:
            self.functionsController = Guitar(
                constants.FUNCTIONSCONTROLLERPORT)
        else:
            self.functionsController = wpilib.XboxController(
                constants.FUNCTIONSCONTROLLERPORT)

        self.train = Drivetrain()

        self.arm = Arm()

        self.chooser = wpilib.SendableChooser()

        stationCorrectionMobility = StationCorrectionMobility(
            self.train, self.arm)
        autoDoc = StationCorrection(self.train, self.arm)

        self.chooser.setDefaultOption("Auto Charge Station", autoDoc)
        self.chooser.addOption("Mobility Charging Station",
                               stationCorrectionMobility)
        self.chooser.addOption("Timed Drive", TimedDrive(self.train))

        wpilib.SmartDashboard.putData("Autonomoose", self.chooser)

        self.train.setDefaultCommand(JoystickDrive(self.train, lambda: self.driverController.getLeftY(),
                                                   lambda: self.driverController.getRightX(),
                                                   lambda: self.driverController.getLeftBumper(),
                                                   lambda: self.driverController.getRightBumper(),
                                                   lambda: self.driverController.getAButtonReleased())
                                     .alongWith(TickArm(self.arm)))
        if constants.USINGGUITARCONTROLLER:
            JoystickButton(self.functionsController, Guitar.Button.kRed).whenPressed(
                MoveCubePickup(self.arm))
            JoystickButton(self.functionsController, Guitar.Button.kBlue).whenPressed(
                SetGrabber(self.arm))
            JoystickButton(self.functionsController, Guitar.Button.kYellow).whenPressed(
                MoveBackToHome(self.arm))
            JoystickButton(self.functionsController, Guitar.Button.kStar).whenPressed(
                MoveToOrigin(self.arm))
            JoystickButton(self.functionsController, Guitar.Button.kOrange).whenPressed(
                PlaceCubeMid(self.arm))
            if constants.TESTCOMMANDS:
                JoystickButton(self.functionsController, Guitar.Button.kVol).whenPressed(
                    ToggleArmCoast(self.arm))
        else:
            JoystickButton(self.functionsController, wpilib.XboxController.Button.kB).whenPressed(
                MoveCubePickup(self.arm))
            JoystickButton(self.functionsController, wpilib.XboxController.Button.kA).whenPressed(
                SetGrabber(self.arm))
            JoystickButton(self.functionsController, wpilib.XboxController.Button.kY).whenPressed(
                MoveBackToHome(self.arm))
            JoystickButton(self.functionsController, wpilib.XboxController.Button.kX).whenPressed(
                MoveToOrigin(self.arm))
            JoystickButton(self.functionsController, wpilib.XboxController.Button.kStart).whenPressed(
                PlaceCubeMid(self.arm))

    def getAutonomousCommand(self) -> commands2.CommandBase:

        return self.chooser.getSelected()
