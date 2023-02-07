from magicbot import StateMachine, timed_state, state

from components.drivetrain import Drivetrain

class AutoBalance(StateMachine):

    MODE_NAME = "AutoBalance"
    DEFAULT = True
    
    drivetrain: Drivetrain

    @timed_state(duration=10.0, first=True, next_state="stop")
    def balance(self):
        
        power = self.drivetrain.pidController.calculate(self.drivetrain.gyro.getAngle(), 0.0)

        if abs(power) <= 0.5 and abs(power) >= 0.1:

            self.drivetrain.move(power, power)
