import commands2
from subsystems.arm import Arm
from setGrabber import SetGrabber
from poseArm import PoseArm

class PlaceCubeOnTop(commands2.SequentialCommandGroup):
    """
    Arm will place and score cube on the top of the grid
    """
    
    def __init__(self, arm: Arm):

        super().__init__()

        self.addCommands( # TODO: GET ARM POSES
            ## moveArmToAvoid
            PoseArm([0, 0, 0, 0, 0]),
            ## move to place
            PoseArm([0, 0, 0, 0, 0]),
            ## move down slightly to prevent bounce from cube
            PoseArm([0, 0, 0, 0, 0]),
            ## let go
            SetGrabber(arm, False),
            ## MoveArmToAvoid,
            PoseArm([0, 0, 0, 0, 0]),
            ## MoveArmToAvoid camera
            commands2.ParallelCommandGroup(PoseArm([0, 0, 0, 0, 0]), SetGrabber(arm, True)),
            ## move arm to resting position
            PoseArm([0, 0, 0, 0, 0])
            )