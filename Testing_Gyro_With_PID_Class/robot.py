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
        
        self.gyro.calibrate()
        self.pidController.reset()

    def autonomousInit(self):
        
        # Reset and start timer
        self.timer.reset()
        self.timer.start()

        # Keep track of whether robot has made it onto the charging station
        self.onChargeStation = False

    def autonomousPeriodic(self):

        wpilib.SmartDashboard.putNumber("Angle", self.gyro.getAngle())

        if self.gyro.getAngle() <= 7.5 and not self.onChargeStation:

            self.frontLeftMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.2)
            self.frontRightMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.2)
            
            wpilib.SmartDashboard.putString("Auto Status", "Driving to Station")

        elif self.timer.get() <= 10:

            self.onChargeStation = True

            power = self.pidController.calculate(self.gyro.getAngle(), 0.0)

            wpilib.SmartDashboard.putNumber("Requested Power", power)

            if abs(power) <= 0.5:

                self.frontLeftMotor.set(ctre.TalonFXControlMode.PercentOutput, power)
                self.frontRightMotor.set(ctre.TalonFXControlMode.PercentOutput, power)
                
                wpilib.SmartDashboard.putString("Auto Status", "PID Control")
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