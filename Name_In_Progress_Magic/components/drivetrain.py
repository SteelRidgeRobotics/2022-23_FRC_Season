import ctre
import magicbot
import wpilib
from wpimath.controller import PIDController


class Drivetrain:
    FLMotor: ctre.WPI_TalonFX
    BLMotor: ctre.WPI_TalonFX
    FRMotor: ctre.WPI_TalonFX
    BRMotor: ctre.WPI_TalonFX

    gyro: wpilib.ADIS16470_IMU

    pidController: PIDController

    left = magicbot.will_reset_to(0)
    right = magicbot.will_reset_to(0)

    def setup(self):
        self.BLMotor.follow(self.FLMotor)
        self.BRMotor.follow(self.FRMotor)

        self.FLMotor.setInverted(True)
        self.BLMotor.setInverted(True)

        self.FLMotor.setNeutralMode(ctre.NeutralMode.Brake)
        self.BLMotor.setNeutralMode(ctre.NeutralMode.Brake)
        self.FRMotor.setNeutralMode(ctre.NeutralMode.Brake)
        self.BRMotor.setNeutralMode(ctre.NeutralMode.Brake)

        self.gyro.configCalTime(self.gyro.CalibrationTime._512ms)
        self.gyro.setYawAxis(wpilib.ADIS16470_IMU.IMUAxis.kX)
        self.gyro.calibrate()

        self.pidController.reset()

    def move(self, left, right):
        self.left = left
        self.right = right

    def execute(self):
        self.FLMotor.set(ctre.TalonFXControlMode.PercentOutput, self.left)
        self.FRMotor.set(ctre.TalonFXControlMode.PercentOutput, self.right)
