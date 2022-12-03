import wpilib
import commands2
import constants
#import ctre
from wpilib import XboxController
from commands2.button import JoystickButton

class RobotContainer:
    def __init__(self) -> None:
        self.driverController = XboxController(constants.kdriverControllerPort)


        self.timer = wpilib.Timer

        #subsystems


        #chooser
        self.chooser = wpilib.SendableChooser()

        wpilib.SmartDashboard.putData("Autonomous", self.chooser)


    def getAutonomousCommand(self) -> commands2.Command:
        return self.chooser.getSelected()