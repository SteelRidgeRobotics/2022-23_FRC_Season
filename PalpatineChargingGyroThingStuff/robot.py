import wpilib
import ctre

class Palpatine(wpilib.TimedRobot):

    def robotInit(self):

        self.driverController = wpilib.XboxController(0)
        
        self.frontLeft = ctre.WPI_TalonFX(0)
        self.backLeft = ctre.WPI_TalonFX(1)
        self.frontRight = ctre.WPI_TalonFX(2)
        self.backRight = ctre.WPI_TalonFX(3)

        self.gyro = wpilib.ADIS16470_IMU()
        