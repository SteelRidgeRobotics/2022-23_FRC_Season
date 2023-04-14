import math

import commands2
import constants
import conversions
import ctre
import wpilib
from subsystems.swerve_wheel import SwerveWheel


class SwerveDrive(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()
        # init motors
        self.leftFrontDirection = ctre.TalonFX(constants.kleftFrontDirectionID)
        self.leftFrontSpeed = ctre.TalonFX(constants.kleftFrontSpeedID)

        self.leftRearDirection = ctre.TalonFX(constants.kleftRearDirectionID)
        self.leftRearSpeed = ctre.TalonFX(constants.kleftRearSpeedID)

        self.rightFrontDirection = ctre.TalonFX(constants.krightFrontDirectionID)
        self.rightFrontSpeed = ctre.TalonFX(constants.krightFrontSpeedID)

        self.rightRearDirection = ctre.TalonFX(constants.krightRearDirectionID)
        self.rightRearSpeed = ctre.TalonFX(constants.krightRearSpeedID)

        # fix inverse
        self.leftFrontSpeed.setInverted(False)
        self.leftRearSpeed.setInverted(False)

        self.rightFrontSpeed.setInverted(True)
        self.rightRearSpeed.setInverted(True)

        self.leftFrontDirection.setInverted(False)
        self.leftRearDirection.setInverted(False)

        self.rightFrontDirection.setInverted(False)
        self.rightRearDirection.setInverted(False)

        # init swerve modules
        self.leftFrontSwerveModule = SwerveWheel(self.leftFrontDirection, self.leftFrontSpeed)
        self.leftRearSwerveModule = SwerveWheel(self.leftRearDirection, self.leftRearSpeed)

        self.rightFrontSwerveModule = SwerveWheel(self.rightFrontDirection, self.rightFrontSpeed)
        self.rightRearSwerveModule = SwerveWheel(self.rightRearDirection, self.rightRearSpeed)

        self.gyro = wpilib.ADIS16470_IMU()
        self.gyro.CalibrationTime(2)
        if wpilib.RobotBase.isReal():
            self.gyro.setYawAxis(wpilib.ADIS16470_IMU.IMUAxis.kX)
        
        self.PDP = wpilib.PowerDistribution(0, wpilib.PowerDistribution.ModuleType.kCTRE)

    def turnWheel(self, module: SwerveWheel, direction: float, magnitude: float):
        self.units = conversions.convertDegreesToTalonFXUnits(direction)
        if magnitude >= 1.0:
            magnitude = 1.0
        # find current angle
        currentAngle = conversions.convertTalonFXUnitsToDegrees(module.directionMotor.getSelectedSensorPosition())
        currentAngle /= constants.ksteeringGearRatio
        # see if the abs value is greater than 180
        if math.fabs(direction) >= 180.0:
            # find the abs value of the opposite angle
            opposAngle = math.fabs(direction) - 180.0
        else:
            # find the abs value of the opposite angle
            opposAngle = math.fabs(direction) + 180.0
        # print some stats for debugging
        wpilib.SmartDashboard.putNumber(" Original Angle -", direction)
        wpilib.SmartDashboard.putNumber(" Abs Opposit Angle -", opposAngle)
        # check if the joystick is in use
        if magnitude != 0.0:
            # this is to test that if 360 or zero is closer it goes to 0
            if (direction == 0.0 or direction == 180.0) and math.fabs(360 - currentAngle) <= math.fabs(
                    currentAngle - opposAngle):
                # this means that 360 or zero is the shortest distance
                # now we have to find if 0.0 is the direction or the opposite angle
                if direction == 0.0:
                    module.turn(self.units * constants.ksteeringGearRatio)
                    module.move(magnitude)
                else:
                    module.turn(conversions.convertDegreesToTalonFXUnits(opposAngle) * constants.ksteeringGearRatio)
                    module.move(-magnitude)
            # if the original angle is closer
            elif math.fabs(currentAngle - direction) <= math.fabs(currentAngle - opposAngle):
                # turn to the original angle
                module.turn(self.units * constants.ksteeringGearRatio)
                # move in the normal way
                module.move(magnitude)
            else:  # the opposite angle is closer
                # turn to the other angle
                module.turn(conversions.convertDegreesToTalonFXUnits(opposAngle) * constants.ksteeringGearRatio)
                # move in the opposite direction
                module.move(-magnitude)

    def translate(self, direction: float, magnitude: float):
        self.turnWheel(self.leftFrontSwerveModule, direction, magnitude)
        self.turnWheel(self.leftRearSwerveModule, direction, magnitude)
        self.turnWheel(self.rightFrontSwerveModule, direction, magnitude)
        self.turnWheel(self.rightRearSwerveModule, direction, magnitude)

    def turnInPlace(self, turnPower: float):
        self.turnWheel(self.leftFrontSwerveModule, 45.0, turnPower)
        self.turnWheel(self.rightFrontSwerveModule, 135.0, turnPower)
        self.turnWheel(self.rightRearSwerveModule, 225.0, turnPower)
        self.turnWheel(self.leftRearSwerveModule, 315.0, turnPower)

    def stopAllMotors(self):
        self.leftFrontSwerveModule.stopAllMotors()
        self.leftRearSwerveModule.stopAllMotors()
        self.rightFrontSwerveModule.stopAllMotors()
        self.rightRearSwerveModule.stopAllMotors()

    def showWheelStats(self):
        wpilib.SmartDashboard.putNumber(" LF Angle Error",
                                        self.leftFrontSwerveModule.directionMotor.getClosedLoopError(0))
        wpilib.SmartDashboard.putNumber(" LR Angle Error",
                                        self.leftRearSwerveModule.directionMotor.getClosedLoopError(0))
        wpilib.SmartDashboard.putNumber(" RF Angle Error",
                                        self.rightFrontSwerveModule.directionMotor.getClosedLoopError(0))
        wpilib.SmartDashboard.putNumber(" RR Angle Error",
                                        self.rightRearSwerveModule.directionMotor.getClosedLoopError(0))

        wpilib.SmartDashboard.putNumber(" LF Speed ", self.leftFrontSwerveModule.getVelocity())
        wpilib.SmartDashboard.putNumber(" LR Speed ", self.leftRearSwerveModule.getVelocity())
        wpilib.SmartDashboard.putNumber(" RF Speed ", self.rightFrontSwerveModule.getVelocity())
        wpilib.SmartDashboard.putNumber(" RR Speed ", self.rightRearSwerveModule.getVelocity())

        wpilib.SmartDashboard.putNumber(" PDP Channel 0", self.PDP.getCurrent(0))
        wpilib.SmartDashboard.putNumber(" PDP Channel 1", self.PDP.getCurrent(1))
        wpilib.SmartDashboard.putNumber(" PDP Channel 2", self.PDP.getCurrent(2))
        wpilib.SmartDashboard.putNumber(" PDP Channel 3", self.PDP.getCurrent(3))
        wpilib.SmartDashboard.putNumber(" PDP Channel 4", self.PDP.getCurrent(4))
        wpilib.SmartDashboard.putNumber(" PDP Channel 5", self.PDP.getCurrent(5))
        wpilib.SmartDashboard.putNumber(" PDP Channel 6", self.PDP.getCurrent(6))
        wpilib.SmartDashboard.putNumber(" PDP Channel 7", self.PDP.getCurrent(7))
        wpilib.SmartDashboard.putNumber(" PDP Channel 8", self.PDP.getCurrent(8))
        wpilib.SmartDashboard.putNumber(" PDP Channel 9", self.PDP.getCurrent(9))
        wpilib.SmartDashboard.putNumber(" PDP Channel 10", self.PDP.getCurrent(10))
        wpilib.SmartDashboard.putNumber(" PDP Channel 11", self.PDP.getCurrent(11))

    def getGyroAngle(self) -> float:
        return self.gyro.getAngle()

    def flushWheels(self):
        self.turnWheel(self.leftFrontSwerveModule, 0.0, 0.01)
        self.turnWheel(self.leftRearSwerveModule, 0.0, 0.01)
        self.turnWheel(self.rightFrontSwerveModule, 0.0, 0.01)
        self.turnWheel(self.rightRearSwerveModule, 0.0, 0.01)

        self.stopAllMotors()

    def moveWhileSpinning(self, leftx: float, lefty: float, turnPower: float):
        straff = -lefty * math.sin(self.getGyroAngle()) + leftx * math.cos(self.getGyroAngle())
        fwrd = lefty * math.cos(self.getGyroAngle()) + leftx * math.sin(self.getGyroAngle())
        a = straff - turnPower * (constants.klength / constants.kr)
        b = straff + turnPower * (constants.klength / constants.kr)
        c = fwrd - turnPower * (constants.kwidth / constants.kr)
        d = fwrd + turnPower * (constants.kwidth / constants.kr)

        frspeed = math.sqrt(b ** 2 + c ** 2)
        flspeed = math.sqrt(b ** 2 + d ** 2)
        rlspeed = math.sqrt(a ** 2 + d ** 2)
        rrspeed = math.sqrt(a ** 2 + c ** 2)

        frangle = math.atan2(b, c) * 180 / math.pi
        flangle = math.atan2(b, d) * 180 / math.pi
        rlangle = math.atan2(a, d) * 180 / math.pi
        rrangle = math.atan2(a, c) * 180 / math.pi

        # the block below checks for the highest speed that a wheel will be turning
        # if the highest speed is greater than one, we then make the largest value equal one, while keeping the ratios the same
        max = frspeed
        if flspeed > max:
            max = flspeed  # would use elif, but we can't gurantee that only one value will be larger than the front right wheel speed
        if rlspeed > max:
            max = rlspeed
        if rrspeed > max:
            max = rrspeed

        if max > 1:
            frspeed /= max
            flspeed /= max
            rlspeed /= max
            rrspeed /= max

        # make wheels turn and spin at the speeds and angles calculated above
        self.turnWheel(self.leftFrontSwerveModule, flangle, flspeed)
        self.turnWheel(self.leftRearSwerveModule, rlangle, rlspeed)
        self.turnWheel(self.rightFrontSwerveModule, frspeed, frspeed)
        self.turnWheel(self.rightRearSwerveModule, rrangle, rrspeed)

    def reset(self):
        self.gyro.reset()
        #self.gyro.calibrate()

        self.leftFrontDirection.setSelectedSensorPosition(0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)
        self.leftFrontSpeed.setSelectedSensorPosition(0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)

        self.leftRearDirection.setSelectedSensorPosition(0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)
        self.leftRearSpeed.setSelectedSensorPosition(0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)

        self.rightFrontDirection.setSelectedSensorPosition(0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)
        self.rightFrontSpeed.setSelectedSensorPosition(0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)

        self.rightRearDirection.setSelectedSensorPosition(0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)
        self.rightRearSpeed.setSelectedSensorPosition(0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)
