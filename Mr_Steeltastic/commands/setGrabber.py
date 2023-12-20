import commands2
import wpilib
from subsystems.arm import Arm


class SetGrabber(commands2.CommandBase):

    def __init__(self, arm: Arm) -> None:
        super().__init__()

        self.arm = arm
        self.isDone = False

    def execute(self) -> None:
        self.arm.toggleGrabber()
        self.isDone = True
        wpilib.SmartDashboard.putBoolean("Grabber", self.arm.grabberOpen)

    def isFinished(self) -> None:
        return self.isDone
