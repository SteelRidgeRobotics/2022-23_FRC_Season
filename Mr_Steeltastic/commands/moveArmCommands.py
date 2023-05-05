import commands2
from subsystems.arm import Arm
from commands.setPositionCombos import SetPositionBaseMid, SetPositionAll, SetPositionAllInRange, SetPositionCubePickup, SetPositionMidTop
from commands.setPositions import *

class MoveBackToHome(commands2.SequentialCommandGroup):
    def __init__(self, arm: Arm):
        super().__init__()
        self.addCommands(
            SetPositionAll(arm, 0, -30340, 0)
            )
"""
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
            """
class PlaceCubeMid(commands2.SequentialCommandGroup):
    def __init__(self, arm: Arm):
        super().__init__()
        self.addCommands(
            SetPositionAllInRange(arm, 0, -30340, 0),
            SetPositionMidTop(arm, -117375, 5110),
            SetPositionBase(arm, -27652)
        )
        
class MoveBackToOrigin(commands2.SequentialCommandGroup):
    def __init__(self, arm: Arm):
        super().__init__()
        self.addCommands(
            SetPositionAllInRange(arm, 0, -30340, 0),
            commands2.WaitCommand(0.25),
            SetPositionAll(arm, 0, 0, 0)
        )

class MoveCubePickup(commands2.SequentialCommandGroup):
    def __init__(self, arm: Arm):
        super().__init__()
        self.addCommands(
            SetPositionAllInRange(arm, 0, -30340, 0),
            SetPositionCubePickup(arm)
        )