# Please don't test this, we need to simulate and work on the code more.

# To do: Robot needs to go back a moment when charging station starts to fall

import wpilib
import ctre

"""
Reminder of all the gyro axes:
X = Pitch
Y = Roll
Z = Yaw
"""

class Palpatine(wpilib.TimedRobot):

    def robotInit(self):

        # Create gyro, set axis to X (pitch, up and down)
        self.gyro = wpilib.ADIS16470_IMU()
        self.gyro.setYawAxis(wpilib.ADIS16470_IMU.IMUAxis.kX)

        # Create motors (this program will use tank drive)
        self.frontLeftMotor = ctre.WPI_TalonFX(0)
        self.rearLeftMotor = ctre.WPI_TalonFX(1)
        self.frontRightMotor = ctre.WPI_TalonFX(2)
        self.rearRightMotor = ctre.WPI_TalonFX(3)

        # Set rear motors to follow front motors
        self.rearLeftMotor.follow(self.frontLeftMotor)
        self.rearRightMotor.follow(self.frontRightMotor)

        # Invert right side of the robot
        self.frontRightMotor.setInverted(True)
        self.rearRightMotor.setInverted(True)

        # Timer
        self.timer = wpilib.Timer()

    def autonomousInit(self):
        
        self.timer.reset()
        self.timer.start()
        self.P = 0.125
        self.SETPOINT = 0
        self.SCALE_DOWN = 20

    def autonomousPeriodic(self):

        if self.timer.get() <= 2:

            self.frontLeftMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.5)
            self.frontRightMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.5)
        
        elif self.timer.get() <= 5:
            
            error = self.gyro.getAngle() - self.SETPOINT

            if abs(error) >= 2:

                power = (self.P * error) / self.SCALE_DOWN

                if abs(power) <= 0.25:
                
                    self.frontLeftMotor.set(ctre.TalonFXControlMode.PercentOutput, power)
                    self.frontRightMotor.set(ctre.TalonFXControlMode.PercentOutput, power)
        
        else:
            
            self.frontLeftMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.0)
            self.frontRightMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.0)

if __name__ == "__main__":

    wpilib.run(Palpatine)