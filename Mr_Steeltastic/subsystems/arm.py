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
  
    def moveToAngle(self, angle):
        
        feedForward = self.holdPercentage * numpy.cos(math.radians(self.getCurrentAngle()))
        self.motor.set(ctre.TalonFXControlMode.MotionMagic, 
                       (angle * 2048/360) * self.gearRatio, 
                       ctre.DemandType.ArbitraryFeedForward, feedForward)

    def moveToPos(self, pos):
        
        feedForward = self.holdPercentage * numpy.cos(math.radians(self.getCurrentAngle()))
        self.motor.set(ctre.TalonFXControlMode.MotionMagic, pos, 
                       ctre.DemandType.ArbitraryFeedForward, feedForward)

    def getCurrentAngle(self):
        
        return self.motor.getSelectedSensorPosition() * 360/2048

class Arm(commands2.SubsystemBase):

    def __init__(self):
        
        super().__init__()

        # self.baseMotor = ArmMotor(constants.ARMBASEPORT, constants.BASEENCODERPORT, constants.ARMBASEHOLDPERCENT, constants.ARMBASEF, 
        #                           constants.ARMBASEP, constants.ARMBASED, 
        #                           constants.ARMBASECRUISEVEL, constants.ARMBASEACCEL, 
        #                           constants.BASERATIO, 0)
        
        # self.midMotor = ArmMotor(constants.ARMMIDPORT, constants.MIDENCODERPORT, constants.ARMMIDHOLDPERCENT, constants.ARMMIDF, 
        #                          constants.ARMMIDP, constants.ARMMIDD, 
        #                          constants.ARMMIDCRUISEVEL, constants.ARMMIDACCEL, 
        #                          constants.MIDDLERATIO, 0)
        
        # self.topMotor = ArmMotor(constants.ARMTOPPORT, constants.TOPENCODERPORT, constants.ARMTOPHOLDPERCENT, constants.ARMTOPF, 
        #                          constants.ARMTOPP, constants.ARMTOPD, 
        #                          constants.ARMTOPCRUISEVEL, constants.ARMTOPACCEL, 
        #                          constants.TOPRATIO, 0)
        
        # self.grabberMotor = ArmMotor(constants.ARMGRABBERPORT, constants.GRABBERENCODERPORT, constants.ARMGRABBERHOLDPERCENT, constants.ARMGRABBERF, 
        #                              constants.ARMGRABBERP, constants.ARMGRABBERD, 
        #                              constants.ARMGRABBERCRUISEVEL, constants.ARMGRABBERACCEL, 
        #                              constants.GRABBERRATIO, 0)

        self.baseMotor = ArmMotor(constants.ARMBASEPORT, constants.ARMBASEHOLDPERCENT, constants.ARMBASEF, 
                                  constants.ARMBASEP, constants.ARMBASED, 
                                  constants.ARMBASECRUISEVEL, constants.ARMBASEACCEL, 
                                  constants.BASERATIO, 0)
        
        self.midMotor = ArmMotor(constants.ARMMIDPORT, constants.ARMMIDHOLDPERCENT, constants.ARMMIDF, 
                                 constants.ARMMIDP, constants.ARMMIDD, 
                                 constants.ARMMIDCRUISEVEL, constants.ARMMIDACCEL, 
                                 constants.MIDDLERATIO, 0)
        
        self.topMotor = ArmMotor(constants.ARMTOPPORT, constants.ARMTOPHOLDPERCENT, constants.ARMTOPF, 
                                 constants.ARMTOPP, constants.ARMTOPD, 
                                 constants.ARMTOPCRUISEVEL, constants.ARMTOPACCEL, 
                                 constants.TOPRATIO, 0)
        
        self.grabberMotor = ArmMotor(constants.ARMGRABBERPORT, constants.ARMGRABBERHOLDPERCENT, constants.ARMGRABBERF, 
                                     constants.ARMGRABBERP, constants.ARMGRABBERD, 
                                     constants.ARMGRABBERCRUISEVEL, constants.ARMGRABBERACCEL, 
                                     constants.GRABBERRATIO, 0)
        
        self.wristMotor = ctre.TalonSRX(constants.ARMGRABBERWRISTPORT)
        # self.wristEncoder = ctre.CANCoder(constants.WRISTENCODERPORT)

        self.wristMotor.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder, 0, 10)

        self.wristMotor.setSelectedSensorPosition(0)

        self.wristMotor.configMotionCruiseVelocity(constants.ARMWRISTCRUISEVEL, 10)
        self.wristMotor.configMotionAcceleration(constants.ARMWRISTACCEL, 10)

        self.wristMotor.setSensorPhase(False)

        self.wristMotor.setNeutralMode(ctre.NeutralMode.Brake)

        self.grabberSolenoid = wpilib.DoubleSolenoid(constants.SOLENOIDMODULE, constants.SOLENOIDMODULETYPE, constants.GRABBERSOLENOIDIN, constants.GRABBERSOLENOIDOUT)

        self.grabberOpen = False
        self.grabberSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)
        
    def keepArmsAtZero(self):

        self.baseMotor.keepAtZero()
        self.midMotor.keepAtZero()
        self.topMotor.keepAtZero()
        self.grabberMotor.keepAtZero()
        #self.wristMotor.set(ctre.TalonFXControlMode.MotionMagic, 0)
        
    def moveArmToPose(self, base: float, mid: float, top: float, grabber: float, 
                      wrist: float):
        """
        Move the arm to a specific pose.
        Requires angles for the base, middle, top, grabber, and wrist motors.
        """

        self.baseMotor.moveToAngle(base)
        self.midMotor.moveToAngle(mid)
        self.topMotor.moveToAngle(top)
        self.grabberMotor.moveToAngle(grabber)
        self.wristMotor.set(ctre.TalonFXControlMode.MotionMagic, (wrist * 2048/360), 
                            ctre.DemandType.ArbitraryFeedForward, constants.ARMWRISTF)

    def ArmToPos(self, base: int, mid: int, top: int, grabber: int, wrist: int):
        self.baseMotor.moveToPos(base)
        self.midMotor.moveToPos(mid)
        self.topMotor.moveToPos(top)
        self.grabberMotor.moveToPos(grabber)
        #self.wristMotor.set(ctre.TalonFXControlMode.MotionMagic, wrist)

    def holdAtPercentage(self, base: float, mid: float, top: float, grabber: float):
        
        self.baseMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, base)
        self.midMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, mid)
        self.topMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, top)
        self.grabberMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, grabber)

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

    def getGrabberState(self):

        self.grabberSolenoid.get()

    def manualbaseMotor(self, leftJoy):
        
        self.baseMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, 
                                 deadband(leftJoy))

    def manualmidMotor(self, rightJoy):
        
        self.midMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, 
                                deadband(rightJoy))

    def manualtopMotor(self, rightTrigger):
        
        self.topMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, 
                                deadband(rightTrigger))
    
    def manualgrabberMotor(self, leftTrigger):

        self.grabberMotor.motor.set(ctre.TalonFXControlMode.PercentOutput, 
                                    deadband(leftTrigger))

    def manualwristMotor(self, percent):
        self.wristMotor.set(ctre.ControlMode.PercentOutput, percent)

    