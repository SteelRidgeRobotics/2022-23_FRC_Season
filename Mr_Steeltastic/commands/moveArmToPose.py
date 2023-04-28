import commands2
from subsystems.arm import Arm
from commands.moveArmCommands import MoveArmUp
#from commands.setPositions import SetPositions
from commands.setPositionCombos import SetPositionBaseMid
from commands.setPositionTop import SetPositionTop

class MoveArmToPose(commands2.SequentialCommandGroup):
    def __init__(self, arm: Arm):
        super().__init__()
        self.addCommands(
            MoveArmUp(arm),
            commands2.WaitCommand(0.3),
            SetPositionTop(arm, 8821),
            SetPositionBaseMid(arm, 44500, -8750)
            )