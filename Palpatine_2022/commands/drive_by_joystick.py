import typing
import commands2
from subsystems.drivetrain import Drivetrain
import wpilib 

class DriveByJoystick(commands2.CommandBase):
    """
    This allows us to drive the robot with an xbox controller
    """
    def __init__(self, drive: Drivetrain, left_axis: typing.Callable[[], float], right_axis: typing.Callable[[], float], bumperRight: typing.Callable[[], bool], bumperLeft: typing.Callable[[], bool]) -> None:
    #def __init__(self, drive: Drivetrain, left_axis, right_axis) -> None:
        super().__init__()
        
        self.drive = drive
        self.left_axis = left_axis
        self.right_axis = right_axis
        self.bumperRight = bumperRight
        self.bumperLeft = bumperLeft
        self.percent = 1.0

        self.addRequirements([self.drive])
        
        self.slowFactor = 0.5
    
    #def initialize(self):
        # Called just before the command runs for the first time
        

    def execute(self) -> None:
        # Called repeatedly when this command is scheduled to run
        #self.drive.userDrive(self.driveController.getY()*-1 + self.driveController.getX(), self.driveController.getY()*-1 - self.driveController.getX())
        
        # when the one of the bumpers is pressed, halve the speed
        if self.bumperRight() or self.bumperLeft():
            self.percent = 0.5
            self.drive.userDrive(self.left_axis(), self.right_axis(), self.percent)
        # 
        #elif (self.bumperRight or self.bumperLeft) and self.slowFactor == 0.5:
        #    self.slowFactor = 1.0 
        else:
            self.percent = 1.0
            self.drive.userDrive(self.left_axis(), self.right_axis(), self.percent)
        
        #self.drive.userDrive(self.left_axis(), self.right_axis())
        wpilib.SmartDashboard.putNumber('   leftJoy - ', self.left_axis())
        wpilib.SmartDashboard.putNumber('   rightJoy - ', self.right_axis())
        wpilib.SmartDashboard.putNumber("  Left Velocity - ", self.drive.frontLeft.getSelectedSensorVelocity())
        wpilib.SmartDashboard.putNumber("  Right Velocity - ", self.drive.frontRight.getSelectedSensorVelocity())
        wpilib.SmartDashboard.putBoolean('  Right Bumper Pressed - ', self.bumperRight())
        wpilib.SmartDashboard.putBoolean('  Left Bumper Pressed - ', self.bumperLeft())
        wpilib.SmartDashboard.putNumber('   Speed Percentage - ', self.percent)

    def end(self, interrupted: bool) -> None:
    # 
        # Called once after isFinished returns True
        # Stop the drivetrain from moving any further
        self.drive.stopMotors()
        
    def isFinished(self) -> bool:
        # Make this return True when this command no longer needs to run execute()
        return False
"""
    def interrupted(self):
        # Called when another command which requres one or more of the same subsystems is scheduled to run
        self.end(message="Interrupted")
        """
