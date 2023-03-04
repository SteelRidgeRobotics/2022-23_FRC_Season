import commands2
from subsystems.arm import Arm
from setGrabber import SetGrabber
from poseArm import PoseArm

class PickUpObject(commands2.SequentialCommandGroup):
    """
    Arm will pick up object in front of it
    """
    
    def __init__(self, arm: Arm):

        super().__init__()

        self.addCommands( # TODO: GET ARM POSES
            ## moveArmToAvoid
            PoseArm([0, 0, 0, 0, 0]),
            ## move to position
            commands2.ParallelCommandGroup(PoseArm([0, 0, 0, 0, 0]), SetGrabber(arm, False)),
            ## grab object
            SetGrabber(arm, True),
            ## MoveArmToAvoid,
            PoseArm([0, 0, 0, 0, 0]),
            ## MoveArmToRestingPosition
            PoseArm([0, 0, 0, 0, 0])
            )