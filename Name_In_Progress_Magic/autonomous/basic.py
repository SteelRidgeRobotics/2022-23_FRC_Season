from magicbot import StateMachine, timed_state, state

from components.drivetrain import Drivetrain

class AutoBalance(StateMachine):

    MODE_NAME = "AutoBalance"
    DEFAULT = True
    
    drivetrain: Drivetrain

    @state(first=True, next_state="stop")
    def balance(self):
        
        if 1 + 1 == 2:

            power = self.drivetrain.pidController.calculate(self.drivetrain.gyro.getAngle(), 0.0)

            if abs(power) <= 0.5 and abs(power) >= 0.1:

                self.drivetrain.move(power, power)

    @state
    def stop(self):
        
        self.drivetrain.move(0.0, 0.0)
