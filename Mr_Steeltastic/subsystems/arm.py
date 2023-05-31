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
                 gearRatio: float, offset: float, name: str):
        super().__init__()

        self.motor = ctre.TalonFX(motorID)
        self.motorID = motorID
        # self.encoder = ctre.CANCoder(encoderID) :(
        self.holdPercentage = holdPercentage
        self.gearRatio = gearRatio
        
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

        self.name = name
        self.currentTarget = 0

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

        self.currentTarget = pos

    def getCurrentAngle(self):
        return self.motor.getSelectedSensorPosition() * 360/2048
    
    def isMotorPos(self, pos: int) -> bool:
        roundedMotorPos = round(self.motor.getSelectedSensorPosition(), -2)
        roundedTarget = round(pos * self.gearRatio, -2)
        return roundedMotorPos == roundedTarget
    
    def isMotorPosInRange(self, pos: int, range=325) -> bool:
        roundedMotorPos = round(self.motor.getSelectedSensorPosition(), -2)
        roundedTarget = round(pos, -2)
        minTarget = roundedTarget - range
        maxTarget = roundedTarget + range
        return minTarget <= roundedMotorPos <= maxTarget
    
    def toPos(self, pos: int):
        """Moves the motor to a postition."""
        if self.motorID == 5: 
            self.moveToPos(pos=pos, angle=self.getCurrentAngle(), aRBFF=False)
        else:
            self.moveToPos(pos=pos, angle=self.getCurrentAngle(), aRBFF=True)

    def getCurrentTarget(self) -> int:
        return self.currentTarget
    
class Arm(commands2.SubsystemBase):

    def __init__(self):
        super().__init__()

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

    def motorToPos(self, motor: ArmMotor, pos: int):
        """
        Moves a single motor to a postition. If the motor is in position, returns true.
        
        DO NOT USE THIS!!! Instead get the single motor and call toPos()
        """
        motor_ratio = None
        if motor == self.baseMotor:
            motor_ratio = constants.BASERATIO
            self.baseMotor.moveToPos(pos=pos * motor_ratio, angle=self.globalBaseAngle, aRBFF=False)
        elif motor == self.midMotor:
            motor_ratio = constants.MIDDLERATIO
            self.midMotor.moveToPos(pos=pos * constants.MIDDLERATIO, angle=self.globalMidAngle)
        elif motor == self.topMotor:
            motor_ratio = constants.TOPRATIO
            self.topMotor.moveToPos(pos=pos * constants.TOPRATIO, angle=self.globalTopAngle)
        elif motor == self.grabberMotor:
            motor_ratio = constants.GRABBERRATIO
            self.grabberMotor.moveToPos(pos=pos * constants.GRABBERRATIO)

    def holdAtPos(self):
        self.baseMotor.moveToPos(pos=self.baseMotor.motor.getSelectedSensorPosition(), angle=self.globalBaseAngle, aRBFF=False)
        self.midMotor.moveToPos(pos=self.midMotor.motor.getSelectedSensorPosition(), angle=self.globalMidAngle)
        self.topMotor.moveToPos(pos=self.topMotor.motor.getSelectedSensorPosition(), angle=self.globalTopAngle)
        self.grabberMotor.moveToPos(pos=self.grabberMotor.motor.getSelectedSensorPosition())
        
    def toggleGrabber(self) -> None:
        if self.grabberOpen:
            self.grabberSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)

        else:
            self.grabberSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse)

        self.grabberOpen = not self.grabberOpen

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
        
class TickArm(commands2.CommandBase):
    
    def __init__(self, arm: Arm) -> None:
        super().__init__()

        self.arm = arm

    def initialize(self) -> None:
        for i in range(len(self.arm.motorList)):
            motor = self.arm.motorList[i]
            wpilib.SmartDashboard.putNumber(f"{motor.name} Pos", 0)
            wpilib.SmartDashboard.putNumber(f"{motor.name} Target", 0)
            wpilib.SmartDashboard.putBoolean(f"{motor.name} Inverted", False)

        

    def execute(self) -> None:
<<<<<<< Updated upstream
=======
        if not self.run:
            self.run = True # Has the command execute ever other tick, prevents the arm from shaking too much from constantly changing the Arb. FF value.
            return
>>>>>>> Stashed changes
        for i in range(len(self.arm.motorList)):
            motor = self.arm.motorList[i]
            wpilib.SmartDashboard.putNumber(f"{motor.name} Pos", motor.motor.getSelectedSensorPosition())
            wpilib.SmartDashboard.putNumber(f"{motor.name} Target", motor.getCurrentTarget())

<<<<<<< Updated upstream
=======
            # Update Arbitrary Feed Forward
            ticksPerDegree = (2048/360) * motor.gearRatio
            degrees = (current_pos - motor.maxHorizontal) / ticksPerDegree
            cosineScalar = math.cos(math.radians(degrees))

            arbitrary_feedforward = round(motor.holdPercentage * cosineScalar, 3)

            # Set target pos + arb. FF
            if motor.motorID != constants.ARMBASEPORT:
                motor.motor.set(ctre.TalonFXControlMode.MotionMagic, current_target, ctre.DemandType.ArbitraryFeedForward, arbitrary_feedforward)
            elif motor.motorID == constants.ARMBASEPORT:
                motor.motor.set(ctre.TalonFXControlMode.MotionMagic, current_target)

            wpilib.SmartDashboard.putNumber(f"FF {motor.name}", arbitrary_feedforward)
            wpilib.SmartDashboard.putBoolean(f"{motor.name} Inverted", motor.motor.getInverted())

>>>>>>> Stashed changes
        self.arm.updateGlobalAngles()

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool) -> None:
        pass

    