import commands2
import ctre
import constants

class Arm(commands2.SubsystemBase):

    def __init__(self):

        super().__init__()
        baseMotor = ctre.TalonFX(constants.ARMBASEPORT)
        midMotor = ctre.TalonFX(constants.ARMMIDPORT)
        topMotor = ctre.TalonFX(constants.ARMTOPPORT)
        grabberMotor = ctre.TalonFX(constants.ARMGRABBERPORT)
        wristMotor = ctre.TalonSRX(constants.ARMGRABBERWRISTPORT)

    def 