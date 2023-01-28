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

        # XboxController
        self.controller = wpilib.XboxController(0)

        # Create gyro, set axis to X (pitch, up and down)
        self.gyro = wpilib.ADIS16470_IMU()
        self.gyro.configCalTime(self.gyro.CalibrationTime._1s)
        self.gyro.setYawAxis(wpilib.ADIS16470_IMU.IMUAxis.kX)

        self.gyro.calibrate()

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

        # Brake mode (robot stops with no output)
        self.frontLeftMotor.setNeutralMode(ctre.NeutralMode.Brake)
        self.rearLeftMotor.setNeutralMode(ctre.NeutralMode.Brake)
        self.frontRightMotor.setNeutralMode(ctre.NeutralMode.Brake)
        self.rearRightMotor.setNeutralMode(ctre.NeutralMode.Brake)

        # Timer
        self.timer = wpilib.Timer()

    def disabledInit(self):
        
        self.gyro.calibrate()

    def autonomousInit(self):
        
        # Reset and start timer
        self.timer.reset()
        self.timer.start()

        # Some constants. These would normally be in constants.py
        self.P = 0.2
        self.I = 0.01

        self.SCALE_DOWN = 20

        # Sum of all error (integral)
        self.integral = 0

        # Keep track of whether robot has made it onto the charging station
        self.onChargeStation = False

    def autonomousPeriodic(self):

        wpilib.SmartDashboard.putNumber("Angle", self.gyro.getAngle())

        if self.gyro.getAngle() <= 7.5 and not self.onChargeStation:

            self.frontLeftMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.2)
            self.frontRightMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.2)
            
            wpilib.SmartDashboard.putString("Auto Status", "Driving to Station")

        elif self.timer.get() <= 12:

            self.onChargeStation = True

            error = self.gyro.getAngle()

            self.integral += error / self.SCALE_DOWN

            power = (self.P * (error / self.SCALE_DOWN)) + (self.I * self.integral)

            wpilib.SmartDashboard.putNumber("Requested Power", power)

            if abs(power) <= 0.625:

                self.frontLeftMotor.set(ctre.TalonFXControlMode.PercentOutput, power)
                self.frontRightMotor.set(ctre.TalonFXControlMode.PercentOutput, power)
                
                wpilib.SmartDashboard.putString("Auto Status", "PID Control")
                wpilib.SmartDashboard.putNumber("Error", error)
                wpilib.SmartDashboard.putBoolean("Power Accepted", power <= 0.625)
        
        else:
            
            self.frontLeftMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.0)
            self.frontRightMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.0)

            wpilib.SmartDashboard.putString("Auto Status", "Stopped")
        
    def teleopPeriodic(self):

        self.frontLeftMotor.set(-self.controller.getLeftY())
        self.frontRightMotor.set(-self.controller.getLeftY())

        wpilib.SmartDashboard.putNumber("Angle", self.gyro.getAngle())


if __name__ == "__main__":
    
    wpilib.run(Palpatine)