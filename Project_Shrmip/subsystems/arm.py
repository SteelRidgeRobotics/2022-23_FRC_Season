import commands2
import ctre
from hal import CAN_OpenStreamSession
import constants
import wpilib

class Arm(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()

        # Initialize Motors
        self.baseMotor = ctre.TalonFX(constants.baseMotor)
        self.middleMotor = ctre.TalonFX(constants.middleMotor)
        self.topMotor = ctre.TalonFX(constants.topMotor)
        self.graberMotor = ctre.TalonSRX(constants.graberMotor)
        self.wristMotor = ctre.TalonFX(constants.wristMotor)

    def rotateClaw(self, degrees:int, speed:int) -> None:
        # James do this pls
        pass

    def returnToStartPos(self) -> None:
        #Maybe do this too, James
        pass

    def rotateClawX(self, degrees:int, speed:int) -> None:
        #This too
        pass

    def stopMotors(self) -> None:
        self.baseMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.0)
        self.middleMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.0)
        self.topMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.0)
        self.graberMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.0)
        self.wristMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.0)

        self.baseMotor.set(0, 0, constants.ktimeoutMs)
        self.middleMotor.set(0, 0, constants.ktimeoutMs)
        self.topMotor.set(0, 0, constants.ktimeoutMs)
        self.graberMotor.set(0, 0, constants.ktimeoutMs)
        self.wristMotor.set(0, 0, constants.ktimeoutMs)

