import commands2
import wpilib
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

        self.train.arcadeDrive(0.0, 0.0, True)

    def execute(self) -> None:
        self.train.arcadeDrive(-0.25, 0.0, True)

    def end(self, interrupted: bool):
        self.train.arcadeDrive(0.0, 0.0, False)

    def isFinished(self) -> bool:
        return wpilib.Timer.getFPGATimestamp() - self.startTime >= 2.0
