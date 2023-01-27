import commands2
import constants
from subsystems.drivetrain import Drivetrain

class DriveForward(commands2.CommandBase):

    def __init__(self, train: Drivetrain, distance: float):

        super().__init__()

        self.train = train
        self.distance = distance
        self.pos = constants.TALONFXUNITSREV * (self.distance / constants.WHEELCIRCUMFERENCEFEET)

        self.addRequirements([self.train])

    def execute(self):

        self.train.magicDrive(self.pos)
    
    def end(self, interrupted: bool):
        
        self.train.arcadeDrive(0.0, 0.0)
    
    def isFinished(self):

        return self.train.frontLeft.getSelectedSensorPosition() != 0 and self.train.frontLeft.getSelectedSensorVelocity() == 0 and self.train.frontRight.getSelectedSensorPosition() != 0 and self.train.frontRight.getSelectedSensorVelocity() == 0

