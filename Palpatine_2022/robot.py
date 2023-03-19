import commands2
import wpilib

from robotcontainer import RobotContainer


class MyRobot(commands2.TimedCommandRobot):

    def robotInit(self) -> None:
        '''Initialize things like subsystems'''
        # init the drive train (This is done in the robotcontainer)
        # self.drivetrain = Drivetrain(self)
        self.container = RobotContainer()
        self.autonomousCommand = self.container.getAutonomousCommand()

    def disabledInit(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""

    def disabledPeriodic(self) -> None:
        """This function is called periodically when disabled"""

    def autonomousInit(self) -> None:
        """This autonomous runs the autonomous command selected by your RobotContainer class."""

        self.autonomousCommand = self.container.getAutonomousCommand()

        if self.autonomousCommand:
            self.autonomousCommand.schedule()

    def autonomousPeriodic(self) -> None:
        """This function is called periodically during autonomous"""

    def teleopInit(self) -> None:
        """
        This makes sure that the autonomous stops running when 
        teleop starts running. If you want the autonomous to
        continue until interrupted by another command, remove
        this line or comment it out.
        """

        if self.autonomousCommand:
            self.autonomousCommand.cancel()

    def teleopPeriodic(self) -> None:
        """This function is called periodically during operator control"""

    def testInit(self) -> None:
        # Cancels all running commands at the start of test mode
        commands2.CommandScheduler.getInstance().cancelAll()


if __name__ == "__main__":
    wpilib.run(MyRobot)
