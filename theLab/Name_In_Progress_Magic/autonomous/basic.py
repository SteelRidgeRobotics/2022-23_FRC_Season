from components.drivetrain import Drivetrain
from magicbot import AutonomousStateMachine, timed_state, state
from wpilib import SmartDashboard


class AutoBalance(AutonomousStateMachine):
    MODE_NAME = "AutoBalance"
    DEFAULT = True

    drivetrain: Drivetrain

    @state(first=True)
    def driveForward(self):

        SmartDashboard.putBoolean("Second Phase?", False)

        self.drivetrain.move(-0.2, -0.2)

        if self.drivetrain.gyro.getAngle() >= 7.5:
            self.next_state("balance")

    @timed_state(duration=10.0)
    def balance(self):

        SmartDashboard.putBoolean("Second Phase?", True)

        power = (self.drivetrain.pidController.calculate(self.drivetrain.gyro.getAngle(), 0.0))

        SmartDashboard.putNumber("Power", power)
        SmartDashboard.putNumber("Angle", self.drivetrain.gyro.getAngle())

        if abs(power) <= 0.4 and abs(power) >= 0.1:
            self.drivetrain.move(power, power)
