import wpilib
import commands2
from subsystems.drivetrain import Drivetrain

class JoystickDrive(commands2.CommandBase):

    def __init__(self, train: Drivetrain, left, right, leftBumper, rightBumper):
        
        super().__init__()

        self.train = train
        self.left = left()
        self.right = right()
        self.leftBumper = leftBumper
        self.rightBumper = rightBumper
        
        if self.left > 1 or self.right > 1:

            self.left /= max(self.left, self.right)
            self.right /= max(self.left, self.right)

        self.addRequirements([self.train])

    def execute(self):
        
        if self.leftBumper or self.rightBumper:
            
            self.left *= 0.5
            self.right *= 0.5

        self.train.arcadeDrive(self.left, self.right)

        wpilib.SmartDashboard.putNumberArray("LR", [self.left, self.right])

    def end(self, interrupted):

        self.train.arcadeDrive(0.0, 0.0)

    def isFinished(self):

        return False
