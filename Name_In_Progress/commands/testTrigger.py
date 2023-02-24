import commands2
import wpilib

class TestTrigger(commands2.CommandBase):

    def __init__(self):
        
        super().__init__()

    def execute(self):
        
        wpilib.SmartDashboard.putBoolean("Command Runs", True)

    def end(self, interrupted):

        pass

    def isFinished(self):

        return False