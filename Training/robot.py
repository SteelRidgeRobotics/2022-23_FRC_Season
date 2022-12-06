import wpilib
from robotcontainer import RobotContainer
import commands2
class MyRobot(commands2.TimedCommandRobot):


    def robotInit(self) -> None:
        self.container = RobotContainer()
        #self.autonomousCommand = self.container.getAutonomousCommand()

    def disabledInit(self) -> None:
        """come back to this later"""
    
    def disabledPeriodic(self) -> None:
        """a"""
    
    '''def autonomousInit(self) -> None:
        self.autonomousCommand = self.container.getAutonomousCommand()

        if self.autonomousCommand:
            self.autonomousCommand.schedule()
    
    def teleopInit(self) -> None:
        if self.autonomousCommand:
            self.autonomousCommand.cancel()'''
    
    def teleopPeriodic(self) -> None:
        """come back later"""
    
    def testInit(self) -> None:
        commands2.CommandScheduler.getInstance().cancelAll()
    
if __name__ == "__main__":
    wpilib.run(MyRobot)