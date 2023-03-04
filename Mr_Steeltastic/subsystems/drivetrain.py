import math
import wpilib
import wpimath.controller
import commands2
import ctre
import constants

def deadband(value):

    return 0 if abs(value) < constants.DEADBAND else value

class Drivetrain(commands2.SubsystemBase):
    """
    Class to drive the robot chassis.
    """

    def __init__(self):

        # call __init__() method of the commands2.SubsystemBase class
        super().__init__()

        # create motors
        self.FLMotor = ctre.TalonFX(0)
        self.BLMotor = ctre.TalonFX(1)
        self.FRMotor = ctre.TalonFX(2)
        self.BRMotor = ctre.TalonFX(3)

        # set followers
        self.BLMotor.follow(self.FLMotor)
        self.BRMotor.follow(self.FRMotor)

        # invert the left side of the robot
        self.FLMotor.setInverted(True)
        self.BLMotor.setInverted(True)

        # configure feedback sensors (basically give it a timeout ms of 10 rather than 0). the timeoutms will wait to see if the config is successful, and then throw an error if something goes wrong
        self.FLMotor.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor, 0, constants.TIMEOUTMS)
        self.FRMotor.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor, 0, constants.TIMEOUTMS)

        # nominal output (this is the minimum value these can be)
        self.FLMotor.configNominalOutputForward(0, constants.TIMEOUTMS)
        self.FRMotor.configNominalOutputForward(0, constants.TIMEOUTMS)
        self.FLMotor.configNominalOutputReverse(0, constants.TIMEOUTMS)
        self.FRMotor.configNominalOutputReverse(0, constants.TIMEOUTMS)

        # peak output (you can probably guess, but it's the max value)
        self.FLMotor.configPeakOutputForward(1, constants.TIMEOUTMS)
        self.FRMotor.configPeakOutputForward(1, constants.TIMEOUTMS)
        self.FLMotor.configPeakOutputReverse(-1, constants.TIMEOUTMS)
        self.FRMotor.configPeakOutputReverse(-1, constants.TIMEOUTMS)

        # slot idx and pid loop idx. there are two loops, primary and auxillary, we want to select the primary
        self.FLMotor.selectProfileSlot(0, 0)
        self.FRMotor.selectProfileSlot(0, 0)
        self.BLMotor.selectProfileSlot(0, 0)
        self.BRMotor.selectProfileSlot(0, 0)

        # configure the P, I, and D values of our motors
        self.FLMotor.config_kP(0, constants.MMP, constants.TIMEOUTMS) #please change these values later (value)
        self.FLMotor.config_kI(0, constants.MMI, constants.TIMEOUTMS)
        self.FLMotor.config_kD(0, constants.MMD, constants.TIMEOUTMS)
        self.FLMotor.config_kF(0, constants.MMF, constants.TIMEOUTMS)

        self.FRMotor.config_kP(0, constants.MMP, constants.TIMEOUTMS)
        self.FRMotor.config_kI(0, constants.MMI, constants.TIMEOUTMS)
        self.FRMotor.config_kD(0, constants.MMD, constants.TIMEOUTMS)
        self.FRMotor.config_kF(0, constants.MMF, constants.TIMEOUTMS)

        # configure the velocity our motion profile will plateau at, as well as the acceleration on our trapezoidal profile. for more information see here: https://v5.docs.ctr-electronics.com/en/stable/ch16_ClosedLoop.html
        self.FLMotor.configMotionCruiseVelocity(constants.CRUISEVELOCITY, constants.TIMEOUTMS)
        self.FRMotor.configMotionCruiseVelocity(constants.CRUISEVELOCITY, constants.TIMEOUTMS)
        self.FLMotor.configMotionAcceleration(constants.CRUISEACCEL, constants.TIMEOUTMS)
        self.FRMotor.configMotionAcceleration(constants.CRUISEACCEL, constants.TIMEOUTMS)

        # zero the sensors
        self.FLMotor.setSelectedSensorPosition(0, 0, constants.TIMEOUTMS)
        self.FRMotor.setSelectedSensorPosition(0, 0, constants.TIMEOUTMS)

        # brake mode motors (no output, motors brake, it's like being on park instead of neutral)
        self.FLMotor.setNeutralMode(ctre.NeutralMode.Brake)
        self.BLMotor.setNeutralMode(ctre.NeutralMode.Brake)
        self.FRMotor.setNeutralMode(ctre.NeutralMode.Brake)
        self.BRMotor.setNeutralMode(ctre.NeutralMode.Brake)

        # PIDController for balancing on the charge station
        self.pidController = wpimath.controller.PIDController(constants.MMP, constants.MMI, constants.MMD)

        # Gyroscope to keep track of robot pitch
        self.gyro = wpilib.ADIS16470_IMU()
        self.gyro.setYawAxis(self.gyro.IMUAxis.kX)

        self.onChargeStation = False


    def arcadeDrive(self, leftJoy, rightJoy):
        """
        Drive the robot using arcade drive.
        """

        leftMotors = -leftJoy + rightJoy
        rightMotors = -leftJoy - rightJoy

        if abs(leftMotors) > 1 or abs(rightMotors) > 1:

            if abs(leftMotors) > abs(rightMotors):

                leftMotors /= leftMotors
                rightMotors /= leftMotors

            else:

                leftMotors /= rightMotors
                rightMotors /= rightMotors

        self.FLMotor.set(ctre.TalonFXControlMode.PercentOutput, deadband(leftMotors))
        self.FRMotor.set(ctre.TalonFXControlMode.PercentOutput, deadband(rightMotors))