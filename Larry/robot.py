import wpilib
from robotcontainer import RobotContainer
import commands2
#vision setup

class MyRobot(commands2.TimedCommandRobot):
   def robotInit(self) -> None:
        #initialize robotcontainer
        self.container = RobotContainer()
        #autonomous
        #self.autonomousCommand = self.container.getAutonomousCommand()
        #launch camera
        
   def disabledInit(self) -> None:
      """Things to do once disabled (only occurs once when disabled)"""
     
   def disabledPeriodic(self) -> None:
      """Things to do when disabled (repeated)"""
        
   def autonomousInit(self) -> None:
     
      """self.autonomousCommand = self.container.getAutonomousCommand()

      if self.autonomousCommand:
         self.autonomousCommand.schedule()"""
      
   def teleopInit(self) -> None:
      """
      if self.autonomousCommand:
          self.autonomousCommand.cancel()
      """
   def testInit(self) -> None:
      #cancel all running commands at the once you enter test mode
      commands2.CommandScheduler.getInstance().cancelAll()
          
if __name__ == "__main__":
   wpilib.run(MyRobot)
