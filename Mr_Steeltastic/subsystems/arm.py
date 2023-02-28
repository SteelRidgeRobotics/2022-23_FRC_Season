import wpilib
import commands2
import ctre
import constants
import numpy

class ArmMotor:

    def __init__(self, motorID: int, holdPercentage: float, feedForward: float, armP: float, armD: float, cruiseVel: float, accel: float, gearRatio: float):

        self.motor = ctre.TalonFX(motorID)
        self.holdPercentage = holdPercentage
        self.gearRatio = gearRatio
        
        self.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.motor.configForwardLimitSwitchSource(ctre.LimitSwitchSource.RemoteTalon, ctre.LimitSwitchNormal.NormallyOpen, motorID, 10)
        self.motor.configReverseLimitSwitchSource(ctre.LimitSwitchSource.RemoteTalon, ctre.LimitSwitchNormal.NormallyOpen, motorID, 10)
        self.motor.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)
        
        self.motor.config_kF(feedForward)
        self.motor.config_kP(armP) 
        self.motor.config_kD(armD)
        self.motor.configMotionCruiseVelocity(cruiseVel)
        self.motor.configMotionAcceleration(accel)
        
        self.motor.setSensorPhase(False)
        
    def moveToAngle(self, angle):
        
        feedForward = self.holdPercentage * numpy.cos(self.getCurrentAngle())
        self.motor.set(ctre.TalonFXControlMode.MotionMagic, (angle * 2048/360) * self.gearRatio, ctre.DemandType.ArbitraryFeedForward, feedForward)

    def getCurrentAngle(self):
        
        return self.motor.getSelectedSensorPosition() * 360/2048



class Arm(commands2.SubsystemBase):

    def __init__(self):

        super().__init__()
        self.baseMotor = ArmMotor(constants.ARMBASEPORT, 0.75, constants.ARMBASEF, constants.ARMBASEP, constants.ARMBASED, constants.ARMBASECRUISEVEL, constants.ARMBASEACCEL, constants.BASERATIO)
        self.midMotor = ArmMotor(constants.ARMMIDPORT, 0.5, constants.ARMMIDF, constants.ARMMIDP, constants.ARMMIDD, constants.ARMMIDCRUISEVEL, constants.ARMMIDACCEL, constants.MIDDLERATIO)
        self.topMotor = ArmMotor(constants.ARMTOPPORT, 0.25, constants.ARMTOPF, constants.ARMTOPP, constants.ARMTOPD, constants.ARMTOPCRUISEVEL, constants.ARMTOPACCEL, constants.TOPRATIO)
        self.grabberMotor = ArmMotor(constants.ARMGRABBERPORT, 0.1, constants.ARMGRABBERF, constants.ARMGRABBERP, constants.ARMGRABBERD, constants.ARMGRABBERCRUISEVEL, constants.ARMGRABBERACCEL, constants.GRABBERRATIO)
        self.wristMotor = ctre.TalonSRX(constants.ARMGRABBERWRISTPORT)

        self.wristMotor.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder)

        self.wristMotor.configMotionCruiseVelocity(constants.ARMWRISTCRUISEVEL)
        self.wristMotor.configMotionAcceleration(constants.ARMWRISTACCEL)

        self.wristMotor.setSensorPhase(False)
        # self.grabberSolenoid = wpilib.DoubleSolenoid(constants.SOLENOIDMODULE, constants.SOLENOIDMODULETYPE, constants.GRABBERSOLENOIDIN, constants.GRABBERSOLENOIDOUT)
        
    
    def moveArmToPose(self, base: float, mid: float, top: float, grabber: float, wrist: float):
        """
        Move the arm to a specific pose.
        Requires angles for the base, middle, top, grabber, and wrist motors.
        """
        self.baseMotor.moveToAngle(base)
        self.midMotor.moveToAngle(mid)
        self.topMotor.moveToAngle(top)
        self.grabberMotor.moveToAngle(grabber)
        self.wristMotor.set(ctre.TalonFXControlMode.MotionMagic, (wrist * 2048/360), ctre.DemandType.ArbitraryFeedForward, constants.ARMWRISTF)

    # def closeGrabber(self, bool: bool):
    #     """
    #     Tell the grabber to open or close
    #     Requires a boolean to say whether to open or close the grabber.
    #     True closes the grabber, False opens it.
    #     """
    #     if bool:
    #         self.grabberSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)
    #     else:
    #         self.grabberSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
    
    # def getGrabberState(self):
    #     self.grabberSolenoid.get()