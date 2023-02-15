import wpilib
import ctre
import magicbot

class ArmLength:

    def __init__(self, motorID, CCWLimitSwitch, CWLimitSwitch):

        self.motor = ctre.WPI_TalonFX(motorID)
        self.CCWLimitSwitch = wpilib.DigitalInput(CCWLimitSwitch)
        self.CWLimitSwitch = wpilib.DigitalInput(CWLimitSwitch)

    def set(self, angle):

        # self.motor.set(ctre.TalonFXControlMode.INSERTHERE, angle * 2048)
        pass

    def getCCWLimitSwitch(self):

        return self.CCWLimitSwitch.get()
    
    def getCWLimitSwitch(self):

        return self.CWLimitSwitch.get()

class Arm:

    baseArm: ArmLength
    middleArm: ArmLength
    topArm: ArmLength
    
    wristMotor: ctre.WPI_TalonFX
    grabberMotor: ctre.WPI_TalonSRX

    def setup(self):

        pass

    def execute(self):

        pass