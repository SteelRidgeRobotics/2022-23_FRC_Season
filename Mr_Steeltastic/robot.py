import math
import wpilib
import commands2
from robotcontainer import RobotContainer

class Steeltastic(commands2.TimedCommandRobot):

    def robotInit(self):

        self.container = RobotContainer()
        self.autoCommand = self.container.getAutonomousCommand()

    def robotPeriodic(self):

        commands2.CommandScheduler.getInstance().run()
    
    def autonomousInit(self):

        self.autoCommand = self.container.getAutonomousCommand()

        if self.autoCommand:

            self.autoCommand.schedule()

    def autonomousPeriodic(self):

        pass

    def teleopInit(self):

        if self.autoCommand:

            self.autoCommand.cancel()

    def teleopPeriodic(self):

        pass

    def testInit(self):

        commands2.CommandScheduler.getInstance().cancelAll()

if __name__ == "__main__":

    wpilib.run(Steeltastic)