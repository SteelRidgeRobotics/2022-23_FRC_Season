import commands2
import constants
from subsystems.drivetrain import Drivetrain

class DriveForward(commands2.CommandBase):

    def __init__(self, train: Drivetrain, distance: float):

        super().__init__()

        self.train = train
        

        self.addRequirements([self.train])

    def execute(self):

        
    
    def end(self, interrupted: bool):
        

    
    def isFinished(self):


