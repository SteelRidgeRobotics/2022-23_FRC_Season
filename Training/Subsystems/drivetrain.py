import commands2
import ctre
import constants

class DriveTrain(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()

        self.frontLeft = ctre.TalonFX(constants.kfrontLeft)
        self.backLeft = ctre.TalonFX(constants.kbackLeft)
        self.frontRight = ctre.TalonFX(constants.kfrontRight)
        self.backRight = ctre.TalonFX(constants.kbackRight)

        #set followers
        self.backLeft.follow(self.frontLeft)
        self.backRight.follow(self.frontRight)

        #reverse sensors
        self.frontLeft.setSensorPhase(False)
        self.frontRight.setSensorPhase(False)

        #invert motors on right side
        self.frontRight.setInverted(True)
        self.backRight.setInverted(True)

    
    def userDrive(self, leftJoy: float, rightJoy: float, percentage: float) -> None:
        self.frontLeft.set(ctre.TalonFXControlMode.PercentOutput, leftJoy*percentage)
        self.frontRight.set(ctre.TalonFXControlMode.PercentOutput, rightJoy*percentage)

    def stopMotors(self) -> None:
        self.frontLeft.set(ctre.TalonFXControlMode.PercentOutput, 0.0)
        self.frontRight.set(ctre.TalonFXControlMode.PercentOutput, 0.0)
    
