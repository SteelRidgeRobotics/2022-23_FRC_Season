import math
import commands2
import ctre
import constants

def deadband(value):

    return 0 if abs(value) < constants.DEADBAND else value

class Drivetrain(commands2.SubsystemBase):

    def __init__(self):

        # call __init__() method of the commands2.SubsystemBase class
        super().__init__()

        # create motors
        self.frontLeft = ctre.WPI_TalonFX(0)
        self.backLeft = ctre.WPI_TalonFX(1)
        self.frontRight = ctre.WPI_TalonFX(2)
        self.backRight = ctre.WPI_TalonFX(3)

        # set followers
        self.backLeft.follow(self.frontLeft)
        self.backRight.follow(self.frontRight)

        # invert the left side of the robot
        self.frontLeft.setInverted(True)
        self.backLeft.setInverted(True)

        # configure feedback sensors (basically give it a timeout ms of 10 rather than 0). the timeoutms will wait to see if the config is successful, and then throw an error if something goes wrong
        self.frontLeft.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor, 0, constants.TIMEOUTMS)
        self.frontRight.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor, 0, constants.TIMEOUTMS)

        # nominal output (this is the minimum value these can be)
        self.frontLeft.configNominalOutputForward(0, constants.TIMEOUTMS)
        self.frontRight.configNominalOutputForward(0, constants.TIMEOUTMS)
        self.frontLeft.configNominalOutputReverse(0, constants.TIMEOUTMS)
        self.frontRight.configNominalOutputReverse(0, constants.TIMEOUTMS)

        # peak output (you can probably guess, but it's the max value)
        self.frontLeft.configPeakOutputForward(1, constants.TIMEOUTMS)
        self.frontRight.configPeakOutputForward(1, constants.TIMEOUTMS)
        self.frontLeft.configPeakOutputReverse(-1, constants.TIMEOUTMS)
        self.frontRight.configPeakOutputReverse(-1, constants.TIMEOUTMS)

        # slot idx and pid loop idx. there are two loops, primary and auxillary, we want to select the primary
        self.frontLeft.selectProfileSlot(0, 0)
        self.frontRight.selectProfileSlot(0, 0)
        self.backLeft.selectProfileSlot(0, 0)
        self.backRight.selectProfileSlot(0, 0)

        # configure the P, I, and D values of our motors
        self.frontLeft.config_kP(0, constants.P, constants.TIMEOUTMS) #please change these values later (value)
        self.frontLeft.config_kI(0, constants.I, constants.TIMEOUTMS)
        self.frontLeft.config_kD(0, constants.D, constants.TIMEOUTMS)
        self.frontLeft.config_kF(0, constants.F, constants.TIMEOUTMS)

        self.frontRight.config_kP(0, constants.P, constants.TIMEOUTMS)
        self.frontRight.config_kI(0, constants.I, constants.TIMEOUTMS)
        self.frontRight.config_kD(0, constants.D, constants.TIMEOUTMS)
        self.frontRight.config_kF(0, constants.F, constants.TIMEOUTMS)

        # configure the velocity our motion profile will plateau at, as well as the acceleration on our trapezoidal profile. for more information see here: https://v5.docs.ctr-electronics.com/en/stable/ch16_ClosedLoop.html
        self.frontLeft.configMotionCruiseVelocity(constants.CRUISEVELOCITY, constants.TIMEOUTMS)
        self.frontRight.configMotionCruiseVelocity(constants.CRUISEVELOCITY, constants.TIMEOUTMS)
        self.frontLeft.configMotionAcceleration(constants.CRUISEACCEL, constants.TIMEOUTMS)
        self.frontRight.configMotionAcceleration(constants.CRUISEACCEL, constants.TIMEOUTMS)

        # zero the sensors
        self.frontLeft.setSelectedSensorPosition(0, 0, constants.TIMEOUTMS)
        self.frontRight.setSelectedSensorPosition(0, 0, constants.TIMEOUTMS)

        # brake mode motors (no output, motors brake, it's like being on park instead of neutral)
        self.frontLeft.setNeutralMode(ctre.NeutralMode.Brake)
        self.backLeft.setNeutralMode(ctre.NeutralMode.Brake)
        self.frontRight.setNeutralMode(ctre.NeutralMode.Brake)
        self.backRight.setNeutralMode(ctre.NeutralMode.Brake)

    def arcadeDrive(self, leftJoy, rightJoy):
        """
        Drive the robot using arcade drive.
        """

        leftMotors = -leftJoy + rightJoy
        rightMotors = -leftJoy - rightJoy

        if abs(leftMotors) > 1:

            leftMotors = math.copysign(1, leftMotors)

        if abs(rightMotors) > 1:

            rightMotors = math.copysign(1, rightMotors)

        self.frontLeft.set(ctre.TalonFXControlMode.PercentOutput, deadband(leftMotors))
        self.frontRight.set(ctre.TalonFXControlMode.PercentOutput, deadband(rightMotors))

    def magicDrive(self, pos):
        """
        Drive the motors to a specific sensor position.
        """

        self.frontLeft.set(ctre.TalonFXControlMode.MotionMagic, pos)
        self.frontRight.set(ctre.TalonFXControlMode.MotionMagic, pos)