import commands2
from subsystems.pidTest import PidTest
from wpilib import SmartDashboard


class GetPIDValues(commands2.CommandBase):
    def __init__(self, pid: PidTest) -> None:
        super().__init__()
        self.pid = pid

        self.addRequirements([self.pid])

    
    def execute(self) -> None:
        self.pid.periodic()
    
    def end(self, interrupted: bool) -> None:
        print()
        
    def isFinished(self) -> bool:
        return False
