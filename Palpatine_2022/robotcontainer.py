import wpilib
import commands2
import constants
import ctre
from wpilib import XboxController
from commands.drive_by_joystick import DriveByJoystick
from commands.drive_straight import DriveStraight
from subsystems.drivetrain import Drivetrain

#hi
class RobotContainer:
    def __init__(self) -> None:
        # driver controller
        self.driverController = XboxController(constants.kdriverControllerPort)
        
        self.frontLeft = ctre.TalonFX(constants.kfrontLeft)
        self.backLeft = ctre.TalonFX(constants.kbackLeft)
        self.frontRight = ctre.TalonFX(constants.kfrontRight)
        self.backRight = ctre.TalonFX(constants.kbackRight)


        self.timer = wpilib.Timer
        
        
        #subsystems
        self.drive = Drivetrain()
        
        # chooser
        self.chooser = wpilib.SendableChooser()
        
        # Add commands to autonomous command chooser
        self.driveStraight = DriveStraight(self.drive, constants.kdistanceToTravel)
        self.chooser.setDefaultOption("Drive Straight", self.driveStraight)

        wpilib.SmartDashboard.putData("Autonomous", self.chooser)

       

        

        
                
        #self.configureButtonBindings()  
        
        #self.drive.setDefaultCommand(DriveByJoystick(self.drive, lambda: -self.driverController.getLeftY(), lambda: -self.driverController.getRightY(), lambda: self.driverController.getRightBumper(), lambda: self.driverController.getLeftBumper()))
        
        
        #self.drive.setDefaultCommand(DriveByJoystick(self.drive, lambda: -self.driverController.getLeftY(), lambda: -self.driverController.getRightY()))
        
        #ARCADE, OBJECTIVELY WAY BETTER - Pickle_Face5 & Wyatt
        self.drive.setDefaultCommand(DriveByJoystick(self.drive, 
        lambda: self.forwardSum(), 
        lambda: self.reverseSum(), 
        lambda: self.driverController.getRightBumper(), 
        lambda: self.driverController.getLeftBumper()))

    def forwardSum(self) -> float: # It took more than 2 and a half hours to get this to work, I swear if this stops working I'm going to commit a crime
        leftY, rightX = self.addDeadZoneAndSpeedLimit(self.driverController.getLeftY(), self.driverController.getRightX())
        return -leftY + rightX

    def reverseSum(self) -> float:
        leftY, rightX = self.addDeadZoneAndSpeedLimit(self.driverController.getLeftY(), self.driverController.getRightX())
        return -leftY - rightX

    def addDeadZoneAndSpeedLimit(self, leftYParam: float, rightXParam: float) -> tuple:
        leftY = leftYParam
        rightX = rightXParam
        wpilib.SmartDashboard.putNumber('trueLeftJoy - ', leftY)
        wpilib.SmartDashboard.putNumber('trueRightJoy - ', rightX)
        if (abs(leftY) <= constants.controllerDeadZoneLeft):
            leftY = 0
        if (abs(rightX) <= constants.controllerDeadZoneRight):
            rightX = 0
        return leftY, rightX

        
    #def configureButtonBindings(self):



    def getAutonomousCommand(self) -> commands2.Command:
        return self.chooser.getSelected()
