import ctre
import magicbot
import wpilib
from wpimath.controller import PIDController

import components.drivetrain
import constants


class Palpatine(magicbot.MagicRobot):
    drivetrain: components.drivetrain.Drivetrain

    # arm: components.arm.Arm

    def createObjects(self):

        # Drivetrain

        self.FLMotor = ctre.WPI_TalonFX(constants.FLMOTORPORT)
        self.BLMotor = ctre.WPI_TalonFX(constants.BLMOTORPORT)
        self.FRMotor = ctre.WPI_TalonFX(constants.FRMOTORPORT)
        self.BRMotor = ctre.WPI_TalonFX(constants.BRMOTORPORT)

        self.gyro = wpilib.ADIS16470_IMU()

        self.pidController = PIDController(constants.P, constants.I, constants.D)

        # Arm

        # self.baseArm = components.arm.ArmLength(constants.BASEMOTORPORT, constants.BASECCWSWITCHPORT, constants.BASECWSWITCHPORT)
        # self.middleArm = components.arm.ArmLength(constants.MIDDLEMOTORPORT, constants.MIDDLECCWSWITCHPORT, constants.MIDDLECWSWITCHPORT)
        # self.topArm = components.arm.ArmLength(constants.TOPMOTORPORT, constants.TOPCCWSWITCHPORT, constants.TOPCWSWITCHPORT)
        # self.wristMotor = ctre.WPI_TalonFX(constants.WRISTMOTORPORT)
        # self.grabberMotor = ctre.WPI_TalonSRX(constants.GRABBERMOTORPORT)

        self.driverController = wpilib.XboxController(constants.DRIVERCONTROLLERPORT)

    def disabledInit(self):

        self.gyro.calibrate()

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
