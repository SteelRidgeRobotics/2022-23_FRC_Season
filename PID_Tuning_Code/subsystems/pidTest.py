import commands2
import ctre
from wpilib import SmartDashboard
from constants import *


class PidTest(commands2.SubsystemBase):

    def __init__(self) -> None:
        super().__init__()

        # initalize motors
        self.motor0 = ctre.TalonFX(0)
        self.motor1 = ctre.TalonFX(1)
        self.motor2 = ctre.TalonFX(2)
        self.motor3 = ctre.TalonFX(3)
        self.motor4 = ctre.TalonFX(4)
        self.motor5 = ctre.TalonFX(5)
        self.motor6 = ctre.TalonFX(6)
        self.motor7 = ctre.TalonFX(7)

        # configure encoders
        self.motor1.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor, 0, ktimeoutMs)
        self.motor2.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor, 0, ktimeoutMs)
        self.motor3.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor, 0, ktimeoutMs)
        self.motor4.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor, 0, ktimeoutMs)
        self.motor5.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor, 0, ktimeoutMs)
        self.motor6.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor, 0, ktimeoutMs)
        self.motor7.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor, 0, ktimeoutMs)

        # create motors as list
        self.motors = [self.motor0, self.motor1, self.motor2, self.motor3, self.motor4, self.motor5, self.motor6, self.motor7]
        
        self.testingMotor = self.motors[0]

        # Config default and sensor positions all motors in the list
        for i in range(len(self.motors)):
            self.motors[i].configFactoryDefault()

            self.motors[i].setSelectedSensorPosition(0.0)

        self.putToSmartDashboard()

        self.flush()

    def initSmartDashboard(self) -> None:
        SmartDashboard.putNumber("Motor Port",0)

    def putToSmartDashboard(self) -> None:
        """This method puts values to the smartdashboard."""
        
        self.testingMotor = self.motors[int(SmartDashboard.getNumber("Motor Port", 0))]

        # Put boolean to "reset" values, PIDF values & a velocity setpoint
        SmartDashboard.putBoolean("Flush", False)
        SmartDashboard.putNumber("kP", 0)
        SmartDashboard.putNumber("kI", 0)
        SmartDashboard.putNumber("kD", 0)
        SmartDashboard.putNumber("kF", 0)

        SmartDashboard.putNumber("Cruise Velocity", 0)
        SmartDashboard.putNumber("Cruise Accel", 0)

        SmartDashboard.putNumber("Setpoint", 0)
        SmartDashboard.putBoolean("Inverted", False)

    def flush(self) -> None:
        self.testingMotor = self.motors[int(SmartDashboard.getNumber("Motor Port", 0))]

        # create names for smartdashboard, sets Talons to velocity control mode for tuning and prints when values are updated to the stream
        self.testingMotor.setInverted(SmartDashboard.getBoolean("Inverted", False))

        self.testingMotor.config_kF(0, SmartDashboard.getNumber("kF", 0), ktimeoutMs)
        self.testingMotor.config_kP(0, SmartDashboard.getNumber("kP", 0), ktimeoutMs)
        self.testingMotor.config_kI(0, SmartDashboard.getNumber("kI", 0), ktimeoutMs)
        self.testingMotor.config_kD(0, SmartDashboard.getNumber("kD", 0), ktimeoutMs)

    
        self.testingMotor.configMotionCruiseVelocity(SmartDashboard.getNumber("Cruise Velocity", 0), ktimeoutMs)
        self.testingMotor.configMotionAcceleration(SmartDashboard.getNumber("Cruise Accel", 0), ktimeoutMs)

        self.testingMotor.set(ctre.TalonFXControlMode.MotionMagic, SmartDashboard.getNumber("Setpoint", 0))

        SmartDashboard.putBoolean("Flush", False)

    def putMotorValuesToSmartDashboard(self) -> None:
        """This method puts motor values to the smartdashboard."""

        self.testingMotor = self.motors[int(SmartDashboard.getNumber("Motor Port", 0))]

        # create names for smartdashboard & targets/errors
        SmartDashboard.putNumber("Motor Port", self.testingMotor.getDeviceID())
        SmartDashboard.putBoolean("Flush", False)

        ctre.TalonFX.getClosedLoopError

        SmartDashboard.putNumber("Closed Loop Error", self.testingMotor.getClosedLoopError())

    def periodic(self) -> None:
        """This method runs periodically to check whether to flush or not and continues to update the smartdashboard."""

        if SmartDashboard.getBoolean("Flush", False):
            self.flush()

        self.putMotorValuesToSmartDashboard()
