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

        self.pidController = PIDController(0.0125, 0.0, 0.0)

        self.driverController = wpilib.XboxController(constants.DRIVERCONTROLLERPORT)

    def teleopPeriodic(self):

        self.drivetrain.move(self.driverController.getLeftY(), self.driverController.getRightY())

if __name__ == 'main':

    wpilib.run(Palpatine)