# import commands2
import ctre
import wpilib
from conversions import *
from constants import *


class SwerveWheel():


    def __init__(self, directionMotor: ctre.TalonFX, 
                 speedMotor: ctre.TalonFX, 
                 CANcoder: ctre.CANCoder) -> None:
        

        # super().__init__()
        self.directionMotor = directionMotor
        self.speedMotor = speedMotor
        self.CANcoder = CANcoder

        self.directionMotor.configSelectedFeedbackSensor(
            ctre.FeedbackDevice.IntegratedSensor, 0, ktimeoutMs)

        # self.directionMotor.setSelectedSensorPosition(0.0, 0, ktimeoutMs)

        self.directionMotor.config_kF(0, kF, ktimeoutMs)

        self.directionMotor.config_kP(0, kP, ktimeoutMs)

        self.directionMotor.config_kI(0, kI, ktimeoutMs)

        self.directionMotor.config_kD(0, kD, ktimeoutMs)

        self.directionMotor.config_IntegralZone(0, kIzone, ktimeoutMs)

        # MOTOR CONFIG
        self.directionMotor.configNominalOutputForward(0, ktimeoutMs)
        self.directionMotor.configNominalOutputReverse(0, ktimeoutMs)

        self.directionMotor.configPeakOutputForward(1, ktimeoutMs)
        self.directionMotor.configPeakOutputReverse(-1, ktimeoutMs)

        self.directionMotor.selectProfileSlot(kSlotIdx, kPIDLoopIdx)

        self.directionMotor.configMotionCruiseVelocity(kcruiseVel, ktimeoutMs)
        self.directionMotor.configMotionAcceleration(kcruiseAccel, ktimeoutMs)

        self.directionMotor.setNeutralMode(ctre.NeutralMode.Brake)

        self.directionMotor.setSelectedSensorPosition(0.0, kPIDLoopIdx, 
                                                      ktimeoutMs)

        wpilib.SmartDashboard.putNumber(" P -", kP)
        wpilib.SmartDashboard.putNumber(" I -", kI)
        wpilib.SmartDashboard.putNumber(" D -", kD)
        wpilib.SmartDashboard.putNumber(" F -", kF)
        # wpilib.SmartDashboard.putNumber(" Sensor Position -", 
        # self.directionMotor.getSelectedSensorPosition())
        self.notTurning = True

    # this is our testing turn method
    def turn(self, set_point: float):
        self.notTurning = False
        current_pos = self.directionMotor.getSelectedSensorPosition()
        self.directionMotor.set(ctre.TalonFXControlMode.MotionMagic, 
                                int(set_point))

    def isNotinMotion(self) -> bool:

        if self.directionMotor.getActiveTrajectoryVelocity() == 0.0:
            self.notTurning = True
        else:
            self.notTurning = False
        return self.notTurning

    def move(self, joystick_input: float):

        self.speedMotor.set(ctre.TalonFXControlMode.PercentOutput, 
                            joystick_input)

    def stopAllMotors(self):

        self.directionMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.0)
        self.speedMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.0)
        self.directionMotor.setNeutralMode(ctre.NeutralMode.Coast)

    def getCurrentAngle(self):

        return convertTalonFXUnitsToDegrees(
            (self.directionMotor.getSelectedSensorPosition()) 
            + self.getAbsAngle())
        # return self.CANcoder.getAbsolutePosition()

    def getAbsAngle(self):
            
            return self.CANcoder.getAbsolutePosition()

    def getVelocity(self):

        return self.speedMotor.getSelectedSensorVelocity()

    def showStats(self):

        wpilib.SmartDashboard.putNumber(" P -", kP)
        wpilib.SmartDashboard.putNumber(" I -", kI)
        wpilib.SmartDashboard.putNumber(" D -", kD)
        wpilib.SmartDashboard.putNumber(" F -", kF)
        wpilib.SmartDashboard.putNumber(" CAN - ", self.getAbsAngle())

        # wpilib.SmartDashboard.putNumber(" Sensor Position -", 
        # self.directionMotor.getSelectedSensorPosition())
        # wpilib.SmartDashboard.putNumber(" Sensor Velocity -", 
        # self.directionMotor.getSelectedSensorVelocity())
        # wpilib.SmartDashboard.putBoolean(" Is Not Moving? -", 
        # self.isNotinMotion())

        """
        # This allows us to change the values for the PIDF Controller
        
        self.directionMotor.config_kF(0, kF, ktimeoutMs)

        self.directionMotor.config_kP(0, kP, ktimeoutMs)
 
        self.directionMotor.config_kI(0, kI, ktimeoutMs)

        self.directionMotor.config_kD(0, kD, ktimeoutMs)
        """
