import math
import wpilib
import commands2
from subsystems.drivetrain import Drivetrain

class JoystickDrive(commands2.CommandBase):

    def __init__(self, train: Drivetrain, left, right, leftBumper, rightBumper):
        
        super().__init__()

        self.train = train

        self.leftFunc = left
        self.rightFunc = right
        self.leftBumperFunc = leftBumper
        self.rightBumperFunc = rightBumper

        self.addRequirements([self.train])

    def execute(self):
        
        self.left = self.leftFunc()
        self.right = self.rightFunc()
        self.leftBumper = self.leftBumperFunc()
        self.rightBumper = self.rightBumperFunc()
        
        wpilib.SmartDashboard.putNumberArray("LRJoy", [self.left, self.leftBumper, self.right, self.rightBumper])

        if self.leftBumper or self.rightBumper:
            
            self.left *= 0.5
            self.right *= 0.5

        self.train.arcadeDrive(self.left, self.right, False)

        wpilib.SmartDashboard.putNumber("Gyro Angle", self.train.gyro.getAngle())

    def end(self, interrupted):

        self.train.arcadeDrive(0.0, 0.0, False)

    def isFinished(self):

        return False