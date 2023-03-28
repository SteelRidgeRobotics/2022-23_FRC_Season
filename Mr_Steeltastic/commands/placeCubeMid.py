import commands2
from subsystems.arm import Arm
from commands.moveArmup import MoveArmUp
from commands.setPositions import SetPositions

class PlaceCubeMid(commands2.SequentialCommandGroup):
    def __init__(self, arm: Arm):
        super().__init__()
        self.addCommands(
            MoveArmUp(arm),
            commands2.WaitCommand(0.25),
            #SetPositions(arm, 46835, -10093, 7705, 0),
            #commands2.WaitCommand(0.5), # 6684
            SetPositions(arm, -27652, -117375, 5110, 12145),
            commands2.WaitCommand(0.25),
            SetPositions(arm, -27652, -117375, 5110, 12145),
            )