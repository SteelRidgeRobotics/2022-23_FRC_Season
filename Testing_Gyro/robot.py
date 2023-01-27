# Please don't test this, we need to simulate the code more.

import wpilib
import ctre
import math

"""
Reminder of all the gyro axes:
X = Pitch
Y = Roll
Z = Yaw
"""

class Palpatine(wpilib.TimedRobot):

    def robotInit(self):

        # mom said it's my turn to play on the xbox
        self.driverController = wpilib.XboxController(0)
        
        # Create gyro, set axis to X (pitch, up and down)
        self.gyro = wpilib.ADIS16470_IMU()
        self.gyro.setYawAxis(self.gyro.IMUAxis.kX)

        # Create motors (this program will use tank drive)
        self.frontLeftMotor = ctre.WPI_TalonFX(0)
        self.rearLeftMotor = ctre.WPI_TalonFX(1)
        self.frontRightMotor = ctre.WPI_TalonFX(2)
        self.rearRightMotor = ctre.WPI_TalonFX(3)

        # Set rear motors to follow front motors
        self.rearLeftMotor.follow(self.frontLeftMotor)
        self.rearRightMotor.follow(self.frontRightMotor)

        # Invert right side of the robot
        self.frontLeftMotor.setInverted(True)
        self.rearLeftMotor.setInverted(True)

        self.frontLeftMotor.setNeutralMode(ctre.NeutralMode.Brake)
        self.rearLeftMotor.setNeutralMode(ctre.NeutralMode.Brake)
        self.frontRightMotor.setNeutralMode(ctre.NeutralMode.Brake)
        self.rearRightMotor.setNeutralMode(ctre.NeutralMode.Brake)

    def teleopPeriodic(self):
        
        left = self.driverController.getLeftY()
        right = self.driverController.getRightX()

        if abs(left) <= 0.1:
            left = 0
        if abs(right) <= 0.1:
            right = 0

        leftMotors = -left + right
        rightMotors = -left - right

        if abs(leftMotors) > 1.0:
            leftMotors = math.copysign(1.0, leftMotors)

        if abs(rightMotors) > 1.0:
            rightMotors = math.copysign(1.0, rightMotors)


        self.frontLeftMotor.set(rightMotors)
        self.frontRightMotor.set(leftMotors)

        wpilib.SmartDashboard.putNumber("X", self.gyro.getAngle())
        wpilib.SmartDashboard.putNumber("For", leftMotors)
        wpilib.SmartDashboard.putNumber("RCW", rightMotors)

if __name__ == "__main__":

    wpilib.run(Palpatine)
