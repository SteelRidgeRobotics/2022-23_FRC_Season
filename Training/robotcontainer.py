import wpilib
import commands2
import constants
#import ctre
from wpilib import XboxController
from commands2.button import JoystickButton
from Subsystems.drivetrain import DriveTrain
from Commands.drive_by_joystick import DriveByJoystick

class RobotContainer:
    def __init__(self) -> None:
        self.driverController = XboxController(constants.kdriverControllerPort)


        self.timer = wpilib.Timer

        #subsystems
        self.drive = DriveTrain()

        #chooser
        self.chooser = wpilib.SendableChooser()

        #wpilib.SmartDashboard.putData("Autonomous", self.chooser)
        
        self.drive.setDefaultCommand(DriveByJoystick(self.drive,lambda:-self.driverController.getLeftY()+self.driverController.getRightY(),lambda:-self.driverController.getLeftY()-self.driverController.getRightY(),lambda:self.driverController.getRightBumper(),lambda:self.driverController.getLeftBumper()))


    '''def getAutonomousCommand(self) -> commands2.Command:
        return self.chooser.getSelected()'''