import commands2
import ctre
from wpilib import SmartDashboard


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
        self.motors = [self.motor0, self.motor1, self.motor2, self.motor3, self.motor4, self.motor5
                      self.motor6, self.motor7]
        
        self.testingMotor = self.motors[0]

        # Config default and sensor positions all motors in the list
        for i in range(len(self.motors)):
            self.motor.configFactoryDefault()

            self.motor.setSelectedSensorPosition(0.0)

        self.putToSmartDashboard()

        self.flush()

    def initSmartDashboard(self) -> None:
        SmartDashboard.putNumber("Motor Port",0)

    def putToSmartDashboard(self) -> None:
        """This method puts values to the smartdashboard."""
        
        self.testingMotor = self.motors[SmartDashboard.getNumber("Motor Port")]

        # create motor names for smartdashboard & show whether motors are inverted
        for self.motor in self.motors:
            self.motorName = "Motor " + str(self.motor.getDeviceID()) + " "

            # SmartDashboard.putBoolean(self.motorName + "inverted", self.motor.getInverted())
            SmartDashboard.putNumber(str(self.motorName + "Port"), self.motor.getDeviceID())
        # Put boolean to "reset" values, PIDF values & a velocity setpoint
        SmartDashboard.putBoolean("Flush", False)
        SmartDashboard.putNumber("kP", 0)
        SmartDashboard.putNumber("kI", 0)
        SmartDashboard.putNumber("kD", 0)
        SmartDashboard.putNumber("kF", 0)
        SmartDashboard.putNumber("Setpoint", 0)

    def flush(self) -> None:
        """This method resets values on the smartdashboard."""

        self.motors = [self.motor1, self.motor2, self.motor3, self.motor4]

        self.motor = [ctre.TalonFX, ctre.TalonFX, ctre.TalonFX, ctre.TalonFX]

        # create names for smartdashboard, sets Talons to velocity control mode for tuning and prints when values are updated to the stream
        for self.motor in self.motors:
            self.motorName = "Motor " + str(self.motor.getDeviceID()) + " "

            self.motor.config_kF(0, SmartDashboard.getNumber("kF", 0), ktimeoutMs)
            self.motor.config_kP(0, SmartDashboard.getNumber("kP", 0), ktimeoutMs)
            self.motor.config_kI(0, SmartDashboard.getNumber("kI", 0), ktimeoutMs)
            self.motor.config_kD(0, SmartDashboard.getNumber("kD", 0), ktimeoutMs)
            self.motor.set(ctre.ControlMode.Velocity, SmartDashboard.getNumber("Setpoint", 0))

            print("Updated " + str(self.motor.getDeviceID()))

        SmartDashboard.putBoolean("Flush", False)

    def putMotorValuesToSmartDashboard(self) -> None:
        """This method puts motor values to the smartdashboard."""

        self.testingMotor = self.motors[SmartDashboard.getNumber("Motor Port")]

        # create names for smartdashboard & targets/errors

        SmartDashboard.putNumber(self.motorName + "target", self.testingMotor.getClosedLoopTarget())
        SmartDashboard.putNumber(self.motorName + "velocity", self.testingMotor.getSelectedSensorVelocity())
        SmartDashboard.putNumber(self.motorName + "error", self.testingMotor.getClosedLoopError())

    def periodic(self) -> None:
        """This method runs periodically to check whether to flush or not and continues to update the smartdashboard."""

        if SmartDashboard.getBoolean("Flush", False):
            self.flush()

        self.putMotorValuesToSmartDashboard()
