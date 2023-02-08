import wpilib
from wpimath.controller import PIDController
import magicbot
import ctre
import constants
import components.drivetrain

class Palpatine(magicbot.MagicRobot):

    drivetrain: components.drivetrain.Drivetrain

    def createObjects(self):

        self.FLMotor = ctre.WPI_TalonFX(constants.FLMOTORPORT)
        self.BLMotor = ctre.WPI_TalonFX(constants.BLMOTORPORT)
        self.FRMotor = ctre.WPI_TalonFX(constants.FRMOTORPORT)
        self.BRMotor = ctre.WPI_TalonFX(constants.BRMOTORPORT)

        self.gyro = wpilib.ADIS16470_IMU()

        self.pidController = PIDController(constants.P, constants.I, constants.D)

        self.driverController = wpilib.XboxController(constants.DRIVERCONTROLLERPORT)

    def disabledPeriodic(self):

        pass

    def autonomousInit(self):

        pass

    def teleopInit(self):

        pass
    
    def teleopPeriodic(self):

        left = self.driverController.getLeftY()
        right = self.driverController.getLeftY()
        
        if abs(left) <= constants.DEADBAND:
            
            left = 0.0
        
        if abs(right) <= constants.DEADBAND:
            
            right = 0.0

        self.drivetrain.move(left, right)

if __name__ == '__main__':

    wpilib.run(Palpatine)