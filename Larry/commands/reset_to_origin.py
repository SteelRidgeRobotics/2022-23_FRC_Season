import commands2

class ResetToOrigin(commands2.CommandBase):

    def __init__(self):
        pass

    def initialize(self) -> None:
        return super().initialize()
    
    def execute(self) -> None:
        pass

    def end(self, interrupted: bool) -> None:
        return super().end(interrupted)
    
    def isFinished(self) -> bool:
        return super().isFinished()