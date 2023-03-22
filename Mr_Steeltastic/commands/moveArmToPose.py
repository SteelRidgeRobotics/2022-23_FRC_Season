import commands2
from subsystems.arm import Arm
from commands.moveArmup import MoveArmUp

class MoveArmToPose(commands2.SequentialCommandGroup):
    def __init__(self, arm: Arm):
        super().__init__()
        self.addCommands(
            MoveArmUp(arm),
            MoveArmToPose(arm)
            )