import commands2
from subsystems.arm import Arm

class PoseArm(commands2.CommandBase):
    
    def __init__(self, arm: Arm, wantedPose) -> None:
        
        super().__init__()
        self.arm = Arm()
        self.wantedPose = wantedPose
        
    def execute(self) -> None:
        
        self.wantedPose = self.wantedPose()

        self.arm.moveArmToPose(self.wantedPose[0], self.wantedPose[1], self.wantedPose[2], self.wantedPose[3], self.wantedPose[4])
        
    def end(self) -> None:
        
        pass
    
    def isFinished(self) -> None:
        
        pass # probably something like checking the sensor positions of the motors and seeing if they match what we want
