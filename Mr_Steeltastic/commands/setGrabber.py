import commands2
import wpilib
from subsystems.arm import Arm

class SetGrabber(commands2.CommandBase): 
    
    def __init__(self, arm: Arm, close: bool) -> None: 
        
        super().__init__()
        
        self.arm = Arm()
        self.close = close
        
        self.isDone = False
        
        self.addRequirements([self.arm])
    
    def execute(self) -> None:
        
        self.arm.setGrabber(self.close())
        self.isDone = True
        
    def end(self) -> None:
        
        pass
        
    def isFinished(self) -> None:
        
        return self.isDone