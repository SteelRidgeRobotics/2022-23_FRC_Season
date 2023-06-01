import commands2
import constants
import ctre
import math
import wpilib

def deadband(value):

    return 0 if abs(value) < constants.DEADBAND else value

class ArmMotor(commands2.SubsystemBase):

    """
    Motor for arm ;)
    """
    def __init__(self, motorID: int, holdPercentage: float, feedForward: float, 
                 armP: float, armD: float, cruiseVel: float, accel: float, 
                 gearRatio: float, offset: float, name: str, maxHorizontal: int):
        super().__init__()

        self.motor = ctre.TalonFX(motorID)
        self.motorID = motorID
        # self.encoder = ctre.CANCoder(encoderID) :(
        self.holdPercentage = holdPercentage
        self.gearRatio = gearRatio
        self.maxHorizontal = maxHorizontal
        
        self.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.motor.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)
        self.motor.config_kF(0, feedForward, 10)
        self.motor.config_kP(0, armP, 10)
        self.motor.config_kD(0, armD, 10)
        self.motor.configMotionCruiseVelocity(cruiseVel, 10)
        self.motor.configMotionAcceleration(accel, 10)
        self.motor.setSensorPhase(False)
        self.motor.configIntegratedSensorOffset(offset)
        self.motor.configSupplyCurrentLimit(currLimitConfigs=ctre.SupplyCurrentLimitConfiguration(True, 40.0, 30.0, 2.0))
        self.motor.enableVoltageCompensation(True)
        self.motor.configVoltageCompSaturation(11.8)
        self.motor.setInverted(False)

        self.name = name
        self.currentTarget = 0

    def keepAtZero(self):
        self.motor.set(ctre.TalonFXControlMode.MotionMagic, 0)

    def moveToPos(self, pos: int):
        self.currentTarget = pos
    
    def isMotorPosInRange(self, pos: int, range=325) -> bool:
        roundedMotorPos = round(self.motor.getSelectedSensorPosition(), -2)
        roundedTarget = round(pos, -2)
        minTarget = roundedTarget - range
        maxTarget = roundedTarget + range
        return minTarget <= roundedMotorPos <= maxTarget

    def getCurrentTarget(self) -> int:
        return self.currentTarget
    
class Arm(commands2.SubsystemBase):

    def __init__(self):
        super().__init__()

        self.baseMotor = ArmMotor(constants.ARMBASEPORT, constants.ARMBASEHOLDPERCENT, constants.ARMBASEF, 
                                  constants.ARMBASEP, constants.ARMBASED, 
                                  constants.ARMBASECRUISEVEL, constants.ARMBASEACCEL, 
                                  constants.BASERATIO, 110432, "Base", 0)
        
        self.midMotor = ArmMotor(constants.ARMMIDPORT, constants.ARMMIDHOLDPERCENT, constants.ARMMIDF, 
                                 constants.ARMMIDP, constants.ARMMIDD, 
                                 constants.ARMMIDCRUISEVEL, constants.ARMMIDACCEL, 
                                 constants.MIDDLERATIO, -91211, "Mid", -15978)
        
        self.topMotor = ArmMotor(constants.ARMTOPPORT, constants.ARMTOPHOLDPERCENT, constants.ARMTOPF, 
                                 constants.ARMTOPP, constants.ARMTOPD, 
                                 constants.ARMTOPCRUISEVEL, constants.ARMTOPACCEL, 
                                 constants.TOPRATIO, 4362, "Top", 4138)
        
        self.grabberMotor = ArmMotor(constants.ARMGRABBERPORT, constants.ARMGRABBERHOLDPERCENT, constants.ARMGRABBERF, 
                                     constants.ARMGRABBERP, constants.ARMGRABBERD, 
                                     constants.ARMGRABBERCRUISEVEL, constants.ARMGRABBERACCEL, 
                                     constants.GRABBERRATIO, 0, "Grabber", 0)
        
        self.grabberSolenoid = wpilib.DoubleSolenoid(constants.SOLENOIDMODULE, constants.SOLENOIDMODULETYPE, constants.GRABBERSOLENOIDIN, constants.GRABBERSOLENOIDOUT)

        self.grabberOpen = False
        self.grabberSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)

        self.motorList = [self.baseMotor, self.midMotor, self.topMotor, self.grabberMotor]

    def keepArmsAtZero(self):
        self.baseMotor.keepAtZero()
        self.midMotor.keepAtZero()
        self.topMotor.keepAtZero()
        self.grabberMotor.keepAtZero()
        
    def toggleGrabber(self) -> None:
        if self.grabberOpen:
            self.grabberSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)

        else:
            self.grabberSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse)

        self.grabberOpen = not self.grabberOpen
        
    def manualMotor(self, motor: ArmMotor, am: float):
        motor.motor.set(ctre.TalonFXControlMode.PercentOutput, am)
        
class TickArm(commands2.CommandBase):
    
    def __init__(self, arm: Arm) -> None:
        super().__init__()

        self.arm = arm
        self.run = True

    def initialize(self) -> None:
        for i in range(len(self.arm.motorList)):
            motor = self.arm.motorList[i]
            wpilib.SmartDashboard.putNumber(f"{motor.name} Pos", 0)
            wpilib.SmartDashboard.putNumber(f"{motor.name} Target", 0)

    def execute(self) -> None:
        if not self.run:
            self.run = True
            return
        for i in range(len(self.arm.motorList)):
            motor = self.arm.motorList[i]
            current_pos = motor.motor.getSelectedSensorPosition()
            wpilib.SmartDashboard.putNumber(f"{motor.name} Pos", current_pos)
            current_target = motor.getCurrentTarget()
            wpilib.SmartDashboard.putNumber(f"{motor.name} Target", motor.getCurrentTarget())

            # Update Arbitrary Feed Forward
            ticksPerDegree = (2048/360) * motor.gearRatio
            degrees = (current_pos - motor.maxHorizontal) / ticksPerDegree
            cosineScalar = math.cos(math.radians(degrees))
            
            # Reverse the feed forward for the top motor when the mid motor is flipped over (mainly for cube place mid)
            if motor.motorID == constants.ARMTOPPORT and self.arm.midMotor.motor.getSelectedSensorPosition() < -81630: # -81630 is the mid motor straight upwards
                    arbitrary_feedforward = round((motor.holdPercentage * -1) * cosineScalar, 3)
            else:
                arbitrary_feedforward = round(motor.holdPercentage * cosineScalar, 3)

            if motor.motorID == constants.ARMBASEPORT:
                motor.motor.set(ctre.TalonFXControlMode.MotionMagic, current_target)
            else:
                motor.motor.set(ctre.TalonFXControlMode.MotionMagic, current_target, ctre.DemandType.ArbitraryFeedForward, arbitrary_feedforward)
                wpilib.SmartDashboard.putNumber(f"FF {motor.name}", arbitrary_feedforward)

        self.run = False

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool) -> None:
        pass
