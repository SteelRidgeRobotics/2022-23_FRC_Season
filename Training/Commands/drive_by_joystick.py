import typing
import commands2
from Subsystems.drivetrain import DriveTrain
import wpilib
from constants import *
import math

def deadband(value) -> float:
    if math.fabs(value) <= kdeadband:
        return 0
    else:
        return value

class DriveByJoystick(commands2.CommandBase):
    #This allows us to drive via an xbox controller
    def __init__(self, drive: DriveTrain, left_axis: typing.Callable[[], float], right_axis: typing.Callable[[], float], bumperRight: typing.Callable[[], bool], bumperLeft: typing.Callable[[], bool]) -> None:
        super().__init__()

        self.drive = drive
        self.left_axis = left
        _axis
        self.right_axis = right_axis
        self.bumperRight = bumperRight
        self.bumperLeft = bumperLeft
        self.percent = 1.0

        self.addRequirements([self.drive])

        self.slowFactor = 0.5

    def execute(self) -> None:
        #self.leftJoy = 
        '''come back to this later'''
        if self.bumperRight() or self.bumperLeft():
            self.percent = self.slowFactor
            
        
        else:
            self.percent = 1.0
        left = deadband(self.left_axis())
        right = deadband(self.right_axis())
        self.drive.userDrive(left, right, self.percent)

        wpilib.SmartDashboard.putNumber('leftJoy - ', self.left_axis())
        wpilib.SmartDashboard.putNumber('rightJoy - ', self.right_axis())
        wpilib.SmartDashboard.putNumber('Left Velocity - ', self.drive.frontLeft.getSelectedSensorVelocity())
        wpilib.SmartDashboard.putNumber('Right Velocity - ', self.drive.frontRight.getSelectedSensorVelocity())
        wpilib.SmartDashboard.putNumber('Left Bumper Pressed - ', self.bumperLeft())
        wpilib.SmartDashboard.putNumber('Right Bumper Pressed - ', self.bumperRight())
        wpilib.SmartDashboard.putNumber('Speed Percent - ', self.percent)
    
    def end(self,interrupted:bool) -> None:
        self.drive.stopMotors()
    
    def isFinished(self) -> bool:
        return False