import wpilib
import ctre

class Palpatine(wpilib.TimedRobot):

    def robotInit(self):

        self.driverController = wpilib.XboxController(0)
        
        self.frontLeft = ctre.WPI_TalonFX(0)
        self.backLeft = ctre.WPI_TalonFX(1)
        self.frontRight = ctre.WPI_TalonFX(2)
        self.backRight = ctre.WPI_TalonFX(3)

        self.frontLeft.setNeutralMode(ctre.NeutralMode.Brake)
        self.backLeft.setNeutralMode(ctre.NeutralMode.Brake)
        self.frontRight.setNeutralMode(ctre.NeutralMode.Brake)
        self.backRight.setNeutralMode(ctre.NeutralMode.Brake)

        self.backLeft.follow(self.frontLeft)
        self.backRight.follow(self.frontRight)

        self.frontLeft.setInverted(True)
        self.backLeft.setInverted(True)

        self.frontLeft.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor, 0, 10)
        self.frontRight.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor, 0, 10)

        self.frontLeft.configNominalOutputForward(0, 10)
        self.frontRight.configNominalOutputForward(0, 10)
        self.frontLeft.configNominalOutputReverse(0, 10)
        self.frontRight.configNominalOutputReverse(0, 10)
        
        self.frontLeft.configPeakOutputForward(1, 10)
        self.frontRight.configPeakOutputForward(1, 10)
        self.frontLeft.configPeakOutputReverse(-1, 10)
        self.frontRight.configPeakOutputReverse(-1, 10)

        self.frontLeft.selectProfileSlot(0, 0)
        self.frontRight.selectProfileSlot(0, 0)
        self.backLeft.selectProfileSlot(0, 0)
        self.backRight.selectProfileSlot(0, 0)

        self.frontLeft.config_kP(0, 0.375, 10)
        self.frontLeft.config_kI(0, 0.0, 10)
        self.frontLeft.config_kD(0, 0.0, 10)
        self.frontLeft.config_kF(0, 0.05, 10)

        self.frontRight.config_kP(0, 0.375, 10)
        self.frontRight.config_kI(0, 0.0, 10)
        self.frontRight.config_kD(0, 0.0, 10)
        self.frontRight.config_kF(0, 0.05, 10)

        self.frontLeft.configMotionCruiseVelocity(15000, 10)
        self.frontRight.configMotionCruiseVelocity(15000, 10)
        self.frontLeft.configMotionAcceleration(6000, 10)
        self.frontRight.configMotionAcceleration(6000, 10)

        self.frontLeft.setSelectedSensorPosition(0, 0, 10)
        self.frontRight.setSelectedSensorPosition(0, 0, 10)

        self.gyro = wpilib.ADIS16470_IMU()
        self.gyro.setYawAxis(self.gyro.IMUAxis.kX)

        self.timer = wpilib.Timer()

    def teleopPeriodic(self):

        power = self.driverController.getLeftY()
        rotate = self.driverController.getRightX()

        leftMotors = -power + rotate
        rightMotors = -power - rotate

        wpilib.SmartDashboard.putNumber("Left", leftMotors)
        wpilib.SmartDashboard.putNumber("Right", rightMotors)
        wpilib.SmartDashboard.putNumber("Gyro X", self.gyro.getAngle() % 360)

    def autonomousInit(self):
        
        self.timer.start()

    def autonomousPeriodic(self):

        feetToTravel = 4
        setPoint = (feetToTravel/1.57) * 2048

        if self.timer.get() <= 3:

            self.frontLeft.set(ctre.ControlMode.MotionMagic, setPoint)
            self.frontRight.set(ctre.ControlMode.MotionMagic, setPoint)

if __name__ == "__main__":

    wpilib.run(Palpatine)