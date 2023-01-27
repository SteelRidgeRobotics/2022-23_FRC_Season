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
        
        self.addRequirements([self.train])

    def execute(self):
        
        if self.leftBumper or self.rightBumper:
            
            self.left *= 0.5
            self.right *= 0.5

        self.train.arcadeDrive(self.left, self.right)

    def end(self, interrupted):

        self.train.arcadeDrive(0.0, 0.0)

    def isFinished(self):

        return False
