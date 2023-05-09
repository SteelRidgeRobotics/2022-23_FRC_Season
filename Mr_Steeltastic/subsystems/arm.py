import wpilib
import commands2
import ctre
import constants
import math

def deadband(value):

    return 0 if abs(value) < constants.DEADBAND else value

class ArmMotor:

    """
    Motor for arm ;)
    """

    # def __init__(self, motorID: int, encoderID: int, holdPercentage: float, feedForward: float, 
    #              armP: float, armD: float, cruiseVel: float, accel: float, 
    #              gearRatio: float, offset: float):
        
    def __init__(self, motorID: int, holdPercentage: float, feedForward: float, 
                 armP: float, armD: float, cruiseVel: float, accel: float, 
                 gearRatio: float, offset: float, name: str):

        self.motor = ctre.TalonFX(motorID)
        self.motorID = motorID
        # self.encoder = ctre.CANCoder(encoderID)
        self.holdPercentage = holdPercentage
        self.gearRatio = gearRatio
        
        self.motor.setNeutralMode(ctre.NeutralMode.Coast)
        
        #self.motor.configForwardLimitSwitchSource(ctre.LimitSwitchSource.RemoteTalon, ctre.LimitSwitchNormal.NormallyOpen, motorID, 10)
        #self.motor.configReverseLimitSwitchSource(ctre.LimitSwitchSource.RemoteTalon, ctre.LimitSwitchNormal.NormallyOpen, motorID, 10)
        
        self.motor.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)
        
        self.motor.config_kF(0, feedForward, 10)
        self.motor.config_kP(0, armP, 10)
        self.motor.config_kD(0, armD, 10)

        self.motor.configMotionCruiseVelocity(cruiseVel, 10)
        self.motor.configMotionAcceleration(accel, 10)
        
        self.motor.setSensorPhase(False)
        self.motor.configIntegratedSensorOffset(offset)

        #self.motor.setSelectedSensorPosition(0)
        self.motor.configSupplyCurrentLimit(currLimitConfigs=ctre.SupplyCurrentLimitConfiguration(True, 40.0, 30.0, 2.0))
        self.motor.enableVoltageCompensation(True)
        self.motor.configVoltageCompSaturation(11.8)

        self.name = name

    def keepAtZero(self):
        
        self.motor.set(ctre.TalonFXControlMode.MotionMagic, 0)


    def moveToPos(self, **kwargs):
        pos = kwargs.get("pos", self.motor.getSelectedSensorPosition())
        angle = kwargs.get("angle", self.getCurrentAngle())
        aRBFF = kwargs.get("aRBFF", True)

        if aRBFF:
            feed_forward = self.holdPercentage * math.cos(math.radians(angle))
            self.motor.set(ctre.TalonFXControlMode.MotionMagic, pos, 
                        ctre.DemandType.ArbitraryFeedForward, feed_forward)
        else:
            self.motor.set(ctre.TalonFXControlMode.MotionMagic, pos)

    def getCurrentAngle(self):
        
        return self.motor.getSelectedSensorPosition() * 360/2048
    
    def isMotorPos(self, pos: int) -> bool:
        roundedMotorPos = round(self.motor.getSelectedSensorPosition(), -2)
        roundedTarget = round(pos * self.gearRatio, -2)
        wpilib.SmartDashboard.putNumber("test", roundedMotorPos)
        wpilib.SmartDashboard.putNumber("test2", roundedTarget)
        return roundedMotorPos == roundedTarget
    
    def isMotorPosInRange(self, pos: int, range=325) -> bool:
        roundedMotorPos = round(self.motor.getSelectedSensorPosition(), -2)
        roundedTarget = round(pos * self.gearRatio, -2)
        minTarget = roundedTarget - range
        maxTarget = roundedTarget + range
        wpilib.SmartDashboard.putNumber("test", roundedMotorPos)
        wpilib.SmartDashboard.putNumber("test2", roundedTarget)
        return minTarget <= roundedMotorPos <= maxTarget
    
    def toPos(self, pos: int):
        """Moves the motor to a postition."""
        wpilib.SmartDashboard.putNumber(self.name + ' Motor Target', pos * self.gearRatio)
        if self.motorID == 5: 
            self.moveToPos(pos=pos * self.gearRatio, angle=self.getCurrentAngle(), aRBFF=False)
        else:
            self.moveToPos(pos=pos * self.gearRatio, angle=self.getCurrentAngle())

        wpilib.SmartDashboard.putNumber(self.name + ' Motor Pos', self.motor.getSelectedSensorPosition())
    
class Arm(commands2.SubsystemBase):

    def __init__(self):
        
        super().__init__()
        self.cycleList = [[0, 0, 0], 
                          [-11244, -148657, 3608],
                         ]

        self.cycleIndex = 0

        self.baseMotor = ArmMotor(constants.ARMBASEPORT, constants.ARMBASEHOLDPERCENT, constants.ARMBASEF, 
                                  constants.ARMBASEP, constants.ARMBASED, 
                                  constants.ARMBASECRUISEVEL, constants.ARMBASEACCEL, 
                                  constants.BASERATIO, 110432, "Base")
        
        self.midMotor = ArmMotor(constants.ARMMIDPORT, constants.ARMMIDHOLDPERCENT, constants.ARMMIDF, 
                                 constants.ARMMIDP, constants.ARMMIDD, 
                                 constants.ARMMIDCRUISEVEL, constants.ARMMIDACCEL, 
                                 constants.MIDDLERATIO, -91211, "Mid")
        
        self.topMotor = ArmMotor(constants.ARMTOPPORT, constants.ARMTOPHOLDPERCENT, constants.ARMTOPF, 
                                 constants.ARMTOPP, constants.ARMTOPD, 
                                 constants.ARMTOPCRUISEVEL, constants.ARMTOPACCEL, 
                                 constants.TOPRATIO, 4362, "Top")
        
        self.grabberMotor = ArmMotor(constants.ARMGRABBERPORT, constants.ARMGRABBERHOLDPERCENT, constants.ARMGRABBERF, 
                                     constants.ARMGRABBERP, constants.ARMGRABBERD, 
                                     constants.ARMGRABBERCRUISEVEL, constants.ARMGRABBERACCEL, 
                                     constants.GRABBERRATIO, 0, "Grabber")
        
        self.grabberSolenoid = wpilib.DoubleSolenoid(constants.SOLENOIDMODULE, constants.SOLENOIDMODULETYPE, constants.GRABBERSOLENOIDIN, constants.GRABBERSOLENOIDOUT)

        self.grabberOpen = False
        self.grabberSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)

        self.moved = False

        self.globalBaseAngle = 0
        self.globalMidAngle = 0
        self.globalTopAngle = 0

        self.motorList = [self.baseMotor, self.midMotor, self.topMotor, self.grabberMotor]
        
    def updateGlobalAngles(self):

        self.globalBaseAngle = self.baseMotor.getCurrentAngle()
        self.globalMidAngle = self.globalBaseAngle + self.midMotor.getCurrentAngle()
        self.globalTopAngle = self.globalMidAngle + self.topMotor.getCurrentAngle()

    def keepArmsAtZero(self):
        self.baseMotor.keepAtZero()
        self.midMotor.keepAtZero()
        self.topMotor.keepAtZero()
        self.grabberMotor.keepAtZero()

    def armToPos(self, base: int, mid: int, top: int, grabber: int):
        
        self.grabberMotor.moveToPos(pos=self.grabberMotor.motor.getSelectedSensorPosition())

        wpilib.SmartDashboard.putNumber('Base Motor Target', base * constants.BASERATIO)
        wpilib.SmartDashboard.putNumber('Mid Motor Target', mid * constants.MIDDLERATIO)
        wpilib.SmartDashboard.putNumber('Top Motor Target', top * constants.TOPRATIO)

        wpilib.SmartDashboard.putNumber('Base Motor Pos', self.baseMotor.motor.getSelectedSensorPosition())
        wpilib.SmartDashboard.putNumber('Mid Motor Pos', self.midMotor.motor.getSelectedSensorPosition())
        wpilib.SmartDashboard.putNumber('Top Motor Pos', self.topMotor.motor.getSelectedSensorPosition())

        if round(self.topMotor.motor.getSelectedSensorPosition(), -2) == round(top * constants.TOPRATIO, -2) or self.topMotor.motor.getSelectedSensorVelocity() == 0:
            self.topMotor.moveToPos(pos=self.topMotor.motor.getSelectedSensorPosition(), angle=self.globalTopAngle)
            wpilib.SmartDashboard.putBoolean("Top Motor Good?", True)
            if round(self.midMotor.motor.getSelectedSensorPosition(), -2) == round(mid * constants.MIDDLERATIO, -2) or self.midMotor.motor.getSelectedSensorVelocity() == 0:
                self.midMotor.moveToPos(pos=self.midMotor.motor.getSelectedSensorPosition(), angle=self.globalMidAngle)
                wpilib.SmartDashboard.putBoolean("Mid Motor Good?", True)
                if round(self.baseMotor.motor.getSelectedSensorPosition(), -2) != round(base * constants.BASERATIO, -2) or self.baseMotor.motor.getSelectedSensorVelocity() == 0:
                    wpilib.SmartDashboard.putBoolean("Base Motor Good?", False)
                    self.baseMotor.moveToPos(pos=base * constants.BASERATIO, angle=self.globalBaseAngle, aRBFF=False)
                else:
                    wpilib.SmartDashboard.putBoolean("Base Motor Good?", True)
                    return True
            else:
                wpilib.SmartDashboard.putBoolean("Mid Motor Good?", False)
                self.midMotor.moveToPos(pos=mid * constants.MIDDLERATIO, angle=self.globalMidAngle)
        else:
            wpilib.SmartDashboard.putBoolean("Top Motor Good?", False)
            self.topMotor.moveToPos(pos=top * constants.TOPRATIO, angle=self.globalTopAngle)

        return False
    
    def motorToPos(self, motor: ArmMotor, pos: int):
        """Moves a single motor to a postition. If the motor is in position, returns true."""
        motor_ratio = None
        if motor == self.baseMotor:
            motor_ratio = constants.BASERATIO
            wpilib.SmartDashboard.putNumber('Base Motor Target', pos * motor_ratio)
            self.baseMotor.moveToPos(pos=pos * motor_ratio, angle=self.globalBaseAngle, aRBFF=False)
        elif motor == self.midMotor:
            motor_ratio = constants.MIDDLERATIO
            wpilib.SmartDashboard.putNumber('Mid Motor Target', pos * motor_ratio)
            self.midMotor.moveToPos(pos=pos * constants.MIDDLERATIO, angle=self.globalMidAngle)
        elif motor == self.topMotor:
            motor_ratio = constants.TOPRATIO
            wpilib.SmartDashboard.putNumber('Top Motor Target', pos * motor_ratio)
            self.topMotor.moveToPos(pos=pos * constants.TOPRATIO, angle=self.globalTopAngle)
        elif motor == self.grabberMotor:
            motor_ratio = constants.GRABBERRATIO
            wpilib.SmartDashboard.putNumber('Grabber Motor Target', pos * motor_ratio)
            self.grabberMotor.moveToPos(pos=pos * constants.GRABBERRATIO)

        wpilib.SmartDashboard.putNumber('Base Motor Pos', self.baseMotor.motor.getSelectedSensorPosition())
        wpilib.SmartDashboard.putNumber('Mid Motor Pos', self.midMotor.motor.getSelectedSensorPosition())
        wpilib.SmartDashboard.putNumber('Top Motor Pos', self.topMotor.motor.getSelectedSensorPosition())
    
    def armToPosSimulataneously(self, base: int, mid: int, top: int, grabber: int):

        wpilib.SmartDashboard.putNumber('Base Motor Target', base * constants.BASERATIO)
        wpilib.SmartDashboard.putNumber('Mid Motor Target', mid * constants.MIDDLERATIO)
        wpilib.SmartDashboard.putNumber('Top Motor Target', top * constants.TOPRATIO)

        wpilib.SmartDashboard.putNumber('Base Motor Pos', self.baseMotor.motor.getSelectedSensorPosition())
        wpilib.SmartDashboard.putNumber('Mid Motor Pos', self.midMotor.motor.getSelectedSensorPosition())
        wpilib.SmartDashboard.putNumber('Top Motor Pos', self.topMotor.motor.getSelectedSensorPosition())
        
        self.grabberMotor.moveToPos(pos=grabber * constants.GRABBERRATIO)
        self.baseMotor.moveToPos(pos=base * constants.BASERATIO, aRBFF=False, angle=self.globalBaseAngle)
        self.midMotor.moveToPos(pos=mid * constants.MIDDLERATIO, angle=self.globalMidAngle)
        self.topMotor.moveToPos(pos=top * constants.TOPRATIO, angle=self.globalTopAngle)

    def holdAtPercentage(self, base: float, mid: float, top: float):

        wpilib.SmartDashboard.putNumber('Base Motor Target', base * constants.BASERATIO)
        wpilib.SmartDashboard.putNumber('Mid Motor Target', mid * constants.MIDDLERATIO)
        wpilib.SmartDashboard.putNumber('Top Motor Target', top * constants.TOPRATIO)

        wpilib.SmartDashboard.putNumber('Base Motor Pos', self.baseMotor.motor.getSelectedSensorPosition())
        wpilib.SmartDashboard.putNumber('Mid Motor Pos', self.midMotor.motor.getSelectedSensorPosition())
        wpilib.SmartDashboard.putNumber('Top Motor Pos', self.topMotor.motor.getSelectedSensorPosition())

        self.baseMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, base)
        self.midMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, mid)
        self.topMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, top)

    def holdAtPos(self):

        wpilib.SmartDashboard.putNumber('Base Motor Pos', self.baseMotor.motor.getSelectedSensorPosition())
        wpilib.SmartDashboard.putNumber('Mid Motor Pos', self.midMotor.motor.getSelectedSensorPosition())
        wpilib.SmartDashboard.putNumber('Top Motor Pos', self.topMotor.motor.getSelectedSensorPosition())

        wpilib.SmartDashboard.putNumber('Base Motor Target', self.baseMotor.motor.getSelectedSensorPosition())
        wpilib.SmartDashboard.putNumber('Mid Motor Target', self.midMotor.motor.getSelectedSensorPosition())
        wpilib.SmartDashboard.putNumber('Top Motor Target', self.topMotor.motor.getSelectedSensorPosition())

        self.baseMotor.moveToPos(pos=self.baseMotor.motor.getSelectedSensorPosition(), angle=self.globalBaseAngle, aRBFF=False)
        self.midMotor.moveToPos(pos=self.midMotor.motor.getSelectedSensorPosition(), angle=self.globalMidAngle)
        self.topMotor.moveToPos(pos=self.topMotor.motor.getSelectedSensorPosition(), angle=self.globalTopAngle)
        self.grabberMotor.moveToPos(pos=self.grabberMotor.motor.getSelectedSensorPosition())
        
    def setGrabber(self, bool: bool): # Soon (TM)
        """
        Tell the grabber to open or close
        Requires a boolean to say whether to open or close the grabber.
        True closes the grabber, False opens it.
        """
        
        if bool:
        
            self.grabberSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)
        
        else:
        
            self.grabberSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
        
    def toggleGrabber(self) -> None:

        if self.grabberOpen:

            self.grabberSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)

        else:

            self.grabberSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse)

        self.grabberOpen = not self.grabberOpen

    def toggleArm(self) -> None: # This doesn't work oopsie

        if self.moved:

            self.armToPos(0, (-40 * (2048/360)), 0, 0)
            self.moved = False

        else:

            self.armToPos(-11244/constants.BASERATIO, -148657/constants.MIDDLERATIO, 3608/constants.TOPRATIO, 0) # Cube place (Mid)
            self.moved = True

    def getGrabberState(self):

        self.grabberSolenoid.get()

    def manualBaseMotor(self, leftJoy):
        
        self.baseMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, 
                                 deadband(leftJoy))

    def manualMidMotor(self, rightJoy):
        
        self.midMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, 
                                deadband(rightJoy))

    def manualTopMotor(self, rightTrigger):
        
        self.topMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, 
                                deadband(rightTrigger))
    
    def manualGrabberMotor(self, leftTrigger):

        self.grabberMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, 
                                    deadband(leftTrigger))

    