import commands2
import wpilib
from robotcontainer import RobotContainer
from subsystems.vision import cameraLaunch

class MrSteeltastic(commands2.TimedCommandRobot):

    def robotInit(self):

        self.container = RobotContainer()
        self.autoCommand = self.container.getAutonomousCommand()
        cameraLaunch()

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

        # wpilib.SmartDashboard.putValue("Solenoid", self.container.arm.grabberSolenoid.get())
        pass

    def testInit(self):

        commands2.CommandScheduler.getInstance().cancelAll()


if __name__ == "__main__":
    wpilib.run(MrSteeltastic)
