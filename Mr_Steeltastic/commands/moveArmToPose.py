import commands2
from subsystems.arm import Arm
from commands.moveArmCommands import MoveArmUp
from commands.setPositions import SetPositions

class MoveArmToPose(commands2.SequentialCommandGroup):
    def __init__(self, arm: Arm):
        super().__init__()
        self.addCommands(
            MoveArmUp(arm),
            commands2.WaitCommand(0.5),
            SetPositions(arm, 44500, -8750, 8821, 0)
            )