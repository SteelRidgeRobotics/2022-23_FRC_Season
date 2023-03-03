import commands2
from subsystems.arm import Arm
from setGrabber import SetGrabber

class PickUpObject(commands2.SequentialCommandGroup):
    """
    Arm will pick up object in front of it
    """
    
    def __init__(self, arm: Arm):

        super().__init__()

        # self.addCommands(
        #     ## move to arm to position command
        #     commands2.ParallelCommandGroup(MoveArm, SetGrabber(arm, False)),
        #     SetGrabber(arm, True)
        #     # MoveArmToAvoid
        #     # MoveArmToRestingPosition
        #     )