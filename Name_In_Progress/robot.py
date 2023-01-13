import wpilib
import wpilib.drive
import ctre

class Palpatine(wpilib.TimedRobot):

    def robotInit(self):

        self.driverController = wpilib.XboxController(0)
        self.gyro = wpilib.ADIS16470_IMU()
        self.gyro.setYawAxis(wpilib.ADIS16470_IMU.IMUAxis.kX)
        
        self.frontLeftMotor = ctre.WPI_TalonFX(0)
        self.rearLeftMotor = ctre.WPI_TalonFX(1)
        self.frontRightMotor = ctre.WPI_TalonFX(2)
        self.rearRightMotor = ctre.WPI_TalonFX(3)

        self.rearLeftMotor.follow(self.frontLeftMotor)
        self.rearRightMotor.follow(self.frontRightMotor)

        self.frontLeftMotor.setInverted(True)
        self.rearLeftMotor.setInverted(True)

    def teleopPeriodic(self):
        
        self.frontLeftMotor.set(ctre.TalonFXControlMode.PercentOutput, self.driverController.getLeftY())
        self.frontRightMotor.set(ctre.TalonFXControlMode.PercentOutput, self.driverController.getRightY())
        wpilib.SmartDashboard.putNumber("X", self.gyro.getAngle())

if __name__ == "__main__":
    
    wpilib.run(Palpatine)