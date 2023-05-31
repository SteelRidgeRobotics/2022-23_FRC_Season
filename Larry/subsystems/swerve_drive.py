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

        # set to default so we set everything in the code
        self.leftFrontSpeed.configFactoryDefault()
        self.leftRearSpeed.configFactoryDefault()

        self.rightFrontSpeed.configFactoryDefault()
        self.rightRearSpeed.configFactoryDefault()

        self.leftFrontDirection.configFactoryDefault()
        self.leftRearDirection.configFactoryDefault()

        self.rightFrontDirection.configFactoryDefault()
        self.rightRearDirection.configFactoryDefault()

        # init CAN coders
        self.flCANcoder = ctre.CANCoder(constants.kflCANcoderID, "")
        self.rlCANcoder = ctre.CANCoder(constants.krlCANcoderID, "")
        self.frCANcoder = ctre.CANCoder(constants.kfrCANcoderID, "")
        self.rrCANcoder = ctre.CANCoder(constants.krrCANcoderID, "")

        # ensure that CAN coders will boot to abs sensor instead of 0
        self.flCANcoder.configSensorInitializationStrategy(
            ctre.SensorInitializationStrategy.BootToAbsolutePosition,
            constants.ktimeoutMs)
        
        self.rlCANcoder.configSensorInitializationStrategy(
            ctre.SensorInitializationStrategy.BootToAbsolutePosition,
            constants.ktimeoutMs)
        
        self.frCANcoder.configSensorInitializationStrategy(
            ctre.SensorInitializationStrategy.BootToAbsolutePosition,
            constants.ktimeoutMs)
        
        self.rrCANcoder.configSensorInitializationStrategy(
            ctre.SensorInitializationStrategy.BootToAbsolutePosition,
            constants.ktimeoutMs)

        # making CAN coders read clockwise
        self.flCANcoder.configSensorDirection(True, constants.ktimeoutMs)
        self.rlCANcoder.configSensorDirection(True, constants.ktimeoutMs)
        self.frCANcoder.configSensorDirection(True, constants.ktimeoutMs)
        self.rrCANcoder.configSensorDirection(True, constants.ktimeoutMs)

        # offsets for CAN coders
        self.flCANcoder.configMagnetOffset(constants.kflCANoffset)
        self.rlCANcoder.configMagnetOffset(constants.krlCANoffset)
        self.frCANcoder.configMagnetOffset(constants.kfrCANoffset)
        self.rrCANcoder.configMagnetOffset(constants.krrCANoffset)


        # fix inverse
        self.leftFrontSpeed.setInverted(False)
        self.leftRearSpeed.setInverted(False)

        self.rightFrontSpeed.setInverted(False)
        self.rightRearSpeed.setInverted(False)

        self.leftFrontDirection.setInverted(False)
        self.leftRearDirection.setInverted(False)

        self.rightFrontDirection.setInverted(False)
        self.rightRearDirection.setInverted(False)

        # init swerve modules
        self.leftFrontSwerveModule = SwerveWheel(self.leftFrontDirection, 
                                                 self.leftFrontSpeed, 
                                                 self.flCANcoder)
        
        self.leftRearSwerveModule = SwerveWheel(self.leftRearDirection, 
                                                self.leftRearSpeed, 
                                                self.rlCANcoder)

        self.rightFrontSwerveModule = SwerveWheel(self.rightFrontDirection, 
                                                  self.rightFrontSpeed, 
                                                  self.frCANcoder)
        
        self.rightRearSwerveModule = SwerveWheel(self.rightRearDirection, 
                                                 self.rightRearSpeed, 
                                                 self.rrCANcoder)

        # getting offsets for movement while the robot was off
        """
        self.leftFrontDirection.configIntegratedSensorOffset(self.leftFrontSwerveModule.getAbsAngle())
        self.leftRearDirection.configIntegratedSensorOffset(self.leftRearSwerveModule.getAbsAngle())

        self.rightFrontDirection.configIntegratedSensorOffset(self.rightFrontSwerveModule.getAbsAngle())
        self.rightRearDirection.configIntegratedSensorOffset(self.rightRearSwerveModule.getAbsAngle())
        """
        self.gyro = wpilib.ADIS16470_IMU()
        self.gyro.CalibrationTime(2)
        if wpilib.RobotBase.isReal():
            self.gyro.setYawAxis(wpilib.ADIS16470_IMU.IMUAxis.kX)
        
        # self.PDP = wpilib.PowerDistribution((0, wpilib.PowerDistribution.ModuleType.kCTRE))

    def turnWheel(self, module: SwerveWheel, direction: float, 
                  magnitude: float):
        
        self.units = conversions.convertDegreesToTalonFXUnits(direction)

        if magnitude >= 1.0:
            magnitude = 1.0
        elif magnitude <= -1.0:
            magnitude = -1.0

        # find current angle
        currentAngle = conversions.convertTalonFXUnitsToDegrees(
            (module.directionMotor.getSelectedSensorPosition()
             /constants.ksteeringGearRatio))
        # currentAngle = module.getAbsAngle()
        # currentAngle = conversions.flipCANangle(
        # (module.CANcoder.getAbsolutePosition()))

        """
        # see if the abs value is greater than 180
        if math.fabs(direction) >= 180.0:
            # find the abs value of the opposite angle
            opposAngle = math.fabs(direction) - 180.0
        else:
            # find the abs value of the opposite angle
            opposAngle = math.fabs(direction) + 180.0
        """
        
        if direction < 0:
            opposAngle = direction + 180
            negAngle = 360 + direction
        elif direction > 0:
            opposAngle = direction - 180
            negAngle = direction - 360
            
        else:
            if conversions.sign(direction) == -1:
                opposAngle = -180
                negAngle = 0
            else:
                opposAngle = 180
                negAngle = 0

        # print some stats for debugging
        wpilib.SmartDashboard.putNumber(" Abs Opposite Angle -", opposAngle)
        wpilib.SmartDashboard.putNumber(" Neg Angle -", negAngle)
        # check if the joystick is in use
        if magnitude != 0.0:
            ## turn the wheel
            module.turn(constants.ksteeringGearRatio 
                        * conversions.convertDegreesToTalonFXUnits(
                            (conversions.getclosest(currentAngle, 
                                                    direction, magnitude)[0])))
            
            ## spin the wheel
            module.move(conversions.getclosest(currentAngle, 
                                               direction, magnitude)[1])

            ## put stats to smart dashboard
            wpilib.SmartDashboard.putNumber(" Wanted Angle -", direction)

            wpilib.SmartDashboard.putNumber(
                "RevComp", conversions.giveRevCompensation(currentAngle, 
                                                           direction))
            
            wpilib.SmartDashboard.putNumber("REVOLUTIONS", 
                                            conversions.getRevolutions(
                                                (currentAngle)))
            
            wpilib.SmartDashboard.putNumber("Given Angle", 
                                            conversions.getclosest(
                                                currentAngle, 
                                                direction, magnitude)[0])
            
            wpilib.SmartDashboard.putNumber("Current Angle", currentAngle)

    def translate(self, direction: float, magnitude: float):
        """
        move the robot without changing orientation
        """
        self.turnWheel(self.leftFrontSwerveModule, direction, magnitude)
        self.turnWheel(self.leftRearSwerveModule, direction, magnitude)
        self.turnWheel(self.rightFrontSwerveModule, direction, magnitude)
        self.turnWheel(self.rightRearSwerveModule, direction, magnitude)

    def turnInPlace(self, turnPower: float):
        """
        rotate robot without changing its spot
        """
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

        wpilib.SmartDashboard.putNumber(
            " LR Speed ", self.leftRearSwerveModule.getVelocity())
        
        wpilib.SmartDashboard.putNumber(
            " RF Speed ", self.rightFrontSwerveModule.getVelocity())
        
        wpilib.SmartDashboard.putNumber(
            " RR Speed ", self.rightRearSwerveModule.getVelocity())
        
        wpilib.SmartDashboard.putNumber(
            " LF CAN ", self.leftFrontSwerveModule.getAbsAngle())
        
        wpilib.SmartDashboard.putNumber(
            " LR CAN ", self.leftRearSwerveModule.getAbsAngle())
        
        wpilib.SmartDashboard.putNumber(
            " RF CAN ", self.rightFrontSwerveModule.getAbsAngle())
        
        wpilib.SmartDashboard.putNumber(
            " RR CAN ", self.rightRearSwerveModule.getAbsAngle())
        
        wpilib.SmartDashboard.putNumber(
            " RF ERROR ", (self.leftFrontSwerveModule.getAbsAngle() 
                           - self.rightFrontSwerveModule.getAbsAngle()))
        
        wpilib.SmartDashboard.putNumber(
            " LR ERROR ", (self.leftFrontSwerveModule.getAbsAngle() 
                           - self.leftRearSwerveModule.getAbsAngle()))

    def getGyroAngle(self) -> float:

        return self.gyro.getAngle()
    
    def getWheelOffsets(self):
        # get initial wheel angles
        self.lfOffset = self.leftFrontSwerveModule.getAbsAngle()
        self.lrOffset = self.leftRearSwerveModule.getAbsAngle()
        self.rfOffset = self.rightFrontSwerveModule.getAbsAngle()
        self.rrOffset = self.rightRearSwerveModule.getAbsAngle()

    def flushWheels(self):

        self.turnWheel(self.leftFrontSwerveModule, 
                       self.leftFrontSwerveModule.getAbsAngle(), 0.1)
        
        self.turnWheel(self.leftRearSwerveModule, 
                       self.leftRearSwerveModule.getAbsAngle(), 0.1)
   
        self.turnWheel(self.leftRearSwerveModule, 
                       self.leftRearSwerveModule.getAbsAngle(), 0.1)
        
        self.turnWheel(self.rightRearSwerveModule, 
                       self.rightRearSwerveModule.getAbsAngle(), 0.1)

    def moveWhileSpinning(self, leftx: float, lefty: float, turnPower: float):

        straff = (-lefty * math.sin(self.getGyroAngle()) 
                  + leftx * math.cos(self.getGyroAngle()))
        
        fwrd = (lefty * math.cos(self.getGyroAngle()) 
                + leftx * math.sin(self.getGyroAngle()))
        
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

        # the block below checks for the highest speed that a wheel will be 
        # turning
        # if the highest speed is greater than one, we then make the largest 
        # value equal one, while keeping the ratios the same
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

        self.leftFrontDirection.setSelectedSensorPosition(
            0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)
        
        self.leftFrontSpeed.setSelectedSensorPosition(
            0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)

        self.leftRearDirection.setSelectedSensorPosition(
            0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)
        
        self.leftRearSpeed.setSelectedSensorPosition(
            0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)

        self.rightFrontDirection.setSelectedSensorPosition(
            0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)
        
        self.rightFrontSpeed.setSelectedSensorPosition(
            0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)

        self.rightRearDirection.setSelectedSensorPosition(
            0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)
        
        self.rightRearSpeed.setSelectedSensorPosition(
            0.0, constants.kPIDLoopIdx, constants.ktimeoutMs)

