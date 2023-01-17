import wpilib
import ctre

"""
Reminder for all the gyro axes:
X = Pitch
Y = Roll
Z = Yaw
"""

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

        self.frontRightMotor.setInverted(True)
        self.rearRightMotor.setInverted(True)
        
        self.timer = wpilib.Timer()
        
    def autonomousInit(self):

        self.timer.start()

    def autonomousPeriodic(self):
        
        pass
        
        
if __name__ == "__main__":
    
    wpilib.run(Palpatine)
