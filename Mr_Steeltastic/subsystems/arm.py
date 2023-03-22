import wpilib
import commands2
import ctre
import constants
import math
import numpy

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
                 gearRatio: float, offset: float):

        self.motor = ctre.TalonFX(motorID)
        # self.encoder = ctre.CANCoder(encoderID)
        self.holdPercentage = holdPercentage
        self.gearRatio = gearRatio
        
        self.motor.setNeutralMode(ctre.NeutralMode.Brake)
        
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

        self.motor.setSelectedSensorPosition(0)

    def keepAtZero(self):
        
        self.motor.set(ctre.TalonFXControlMode.MotionMagic, 0)

    def moveToPos(self, pos, aRBFF=True):
        if aRBFF:
            feed_forward = self.holdPercentage * numpy.cos(math.radians(self.getCurrentAngle()))
            self.motor.set(ctre.TalonFXControlMode.MotionMagic, pos, 
                        ctre.DemandType.ArbitraryFeedForward, feed_forward)
        else:
            self.motor.set(ctre.TalonFXControlMode.MotionMagic, pos)

    def getCurrentAngle(self):
        
        return self.motor.getSelectedSensorPosition() * 360/2048

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
                                  constants.BASERATIO, 110432)
        
        self.midMotor = ArmMotor(constants.ARMMIDPORT, constants.ARMMIDHOLDPERCENT, constants.ARMMIDF, 
                                 constants.ARMMIDP, constants.ARMMIDD, 
                                 constants.ARMMIDCRUISEVEL, constants.ARMMIDACCEL, 
                                 constants.MIDDLERATIO, -91211)
        
        self.topMotor = ArmMotor(constants.ARMTOPPORT, constants.ARMTOPHOLDPERCENT, constants.ARMTOPF, 
                                 constants.ARMTOPP, constants.ARMTOPD, 
                                 constants.ARMTOPCRUISEVEL, constants.ARMTOPACCEL, 
                                 constants.TOPRATIO, 4362)
        
        self.grabberMotor = ArmMotor(constants.ARMGRABBERPORT, constants.ARMGRABBERHOLDPERCENT, constants.ARMGRABBERF, 
                                     constants.ARMGRABBERP, constants.ARMGRABBERD, 
                                     constants.ARMGRABBERCRUISEVEL, constants.ARMGRABBERACCEL, 
                                     constants.GRABBERRATIO, 0)
        
        self.grabberSolenoid = wpilib.DoubleSolenoid(constants.SOLENOIDMODULE, constants.SOLENOIDMODULETYPE, constants.GRABBERSOLENOIDIN, constants.GRABBERSOLENOIDOUT)

        self.grabberOpen = False
        self.grabberSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)

        self.moved = False
        
    def keepArmsAtZero(self):

        self.baseMotor.keepAtZero()
        self.midMotor.keepAtZero()
        self.topMotor.keepAtZero()
        self.grabberMotor.keepAtZero()

    def armToPos(self, base: int, mid: int, top: int, grabber: int):
        self.baseMotor.moveToPos(base * constants.BASERATIO, aRBFF=False)
        self.midMotor.moveToPos(mid * constants.MIDDLERATIO)
        self.topMotor.moveToPos(top * constants.TOPRATIO)
        self.grabberMotor.moveToPos(grabber * constants.GRABBERRATIO)

    def holdAtPercentage(self, base: float, mid: float, top: float):
        
        self.baseMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, base)
        self.midMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, mid)
        self.topMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, top)

    def holdAtPos(self):
        self.baseMotor.moveToPos(self.baseMotor.motor.getSelectedSensorPosition(), aRBFF=False)
        self.midMotor.moveToPos(self.midMotor.motor.getSelectedSensorPosition())
        self.topMotor.moveToPos(self.topMotor.motor.getSelectedSensorPosition())
        self.grabberMotor.moveToPos(self.grabberMotor.motor.getSelectedSensorPosition())

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

    