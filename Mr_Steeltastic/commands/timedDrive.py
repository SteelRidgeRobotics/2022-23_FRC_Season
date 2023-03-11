import commands2
import wpilib
import ctre
from subsystems.drivetrain import Drivetrain

class TimedDrive(commands2.CommandBase):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__()

        self.train = drivetrain
        self.timer = wpilib.Timer

        self.addRequirements([self.train])

        self.startTime = 0.0
        self.done = False
    def initialize(self) -> None:
        self.startTime = wpilib.Timer.getFPGATimestamp()
        #self.timer.reset()

        self.train.arcadeDrive(0.0, 0.0)

        #wpilib.SmartDashboard.putNumber("Time", self.timer.get())

    def execute(self) -> None:
        self.train.arcadeDrive(-0.25, 0.0)
    
    def end(self, interrupted: bool):
        self.train.arcadeDrive(0.0, 0.0)

    def isFinished(self) -> bool:
        return wpilib.Timer.getFPGATimestamp() - self.startTime >= 2.0
