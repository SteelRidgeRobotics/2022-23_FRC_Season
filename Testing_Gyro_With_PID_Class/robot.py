import wpilib
from wpimath.controller import PIDController
import ctre

class Palpatine(wpilib.TimedRobot):

    def robotInit(self):

        # XboxController
        self.controller = wpilib.XboxController(0)

        # Create gyro, set axis to X (pitch, up and down)
        self.gyro = wpilib.ADIS16470_IMU()
        self.gyro.configCalTime(self.gyro.CalibrationTime._512ms)
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

        # PID controller that will do our calculations for us
        self.pidController = PIDController(0.0125, 0.0, 0.0)

        # Reset the PID controller
        self.pidController.reset()

        # Timer
        self.timer = wpilib.Timer()

    def disabledInit(self):
        
        # Calibrate the gyro and reset the PID controller
        self.gyro.calibrate()
        self.pidController.reset()

    def autonomousInit(self):
        
        # Reset and start timer
        self.timer.reset()
        self.timer.start()

        # Keep track of whether robot has made it onto the charging station
        self.onChargeStation = False

    def autonomousPeriodic(self):

        # Put the current angle the gyro is giving us on SmartDashboard
        wpilib.SmartDashboard.putNumber("Angle", self.gyro.getAngle())

        # We can reasonably assume the robot is on the charge station once the gyro angle is more than 7.5 degrees, we'll run this code before that happens (unless the robot's already made it on)
        if self.gyro.getAngle() <= 7.5 and not self.onChargeStation:
            
            # Drive the robot forward relatively slowly
            self.frontLeftMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.2)
            self.frontRightMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.2)
            
            # The current auto status is driving to station
            wpilib.SmartDashboard.putString("Auto Status", "Driving to Station")

        # When robot is on charge station, we'll give it until it's been 10 seconds in autonomous to get balanced.
        elif self.timer.get() <= 10:
            
            # Set the variable for robot being on the charge station to true so that the previous code doesn't run
            self.onChargeStation = True

            # Calculate power using the PID controller based on the gyro's angle vs. our setpoint of 0
            power = self.pidController.calculate(self.gyro.getAngle(), 0.0)

            # Put requested power on SmartDashboard (may not be accepted if it's too high for our means)
            wpilib.SmartDashboard.putNumber("Requested Power", power)

            # If the power is between -0.5 and 0.5 (don't want the robot going too fast) we run this code.
            if abs(power) <= 0.5:
                
                # Set motor output to the power we got from earlier
                self.frontLeftMotor.set(ctre.TalonFXControlMode.PercentOutput, power)
                self.frontRightMotor.set(ctre.TalonFXControlMode.PercentOutput, power)
                
                # Currently our auto status is PID Control.
                wpilib.SmartDashboard.putString("Auto Status", "PID Control")
            
            # Also, put whether the power was accepted
            wpilib.SmartDashboard.putBoolean("Power Accepted", power <= 0.5)
        
        # If the time is past 10 seconds run this
        else:
            
            # Set motor power to 0 so the robot stops
            self.frontLeftMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.0)
            self.frontRightMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.0)

            # Currently our auto status is stopped.
            wpilib.SmartDashboard.putString("Auto Status", "Stopped")
    
    # Some basic tank drive
    def teleopPeriodic(self):

        self.frontLeftMotor.set(-self.controller.getLeftY())
        self.frontRightMotor.set(-self.controller.getLeftY())

        # Put angle on SmartDashboard (so we can check it before we test autonomous)
        wpilib.SmartDashboard.putNumber("Angle", self.gyro.getAngle())

if __name__ == "__main__":
    
    wpilib.run(Palpatine)