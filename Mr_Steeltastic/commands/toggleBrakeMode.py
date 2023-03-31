import commands2
import ctre
from subsystems.arm import Arm
import constants


## create command class that enters numbers into the HoldAtPercentage method of
#  the Arm object.
class ToggleBrakeMode(commands2.CommandBase):

    def __init__(self, arm: Arm) -> None:
        super().__init__()

        self.arm = arm
        self.addRequirements([self.arm])

        # self.grabber = grabber

        self.mode = 'Brake'

    def execute(self):


        if self.mode == 'Coast':
        
            self.arm.baseMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
            self.arm.midMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
            self.arm.topMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
            self.arm.grabberMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)

            self.mode = 'Brake'

        else:

            self.arm.baseMotor.motor.setNeutralMode(ctre.NeutralMode.Coast)
            self.arm.midMotor.motor.setNeutralMode(ctre.NeutralMode.Coast)
            self.arm.topMotor.motor.setNeutralMode(ctre.NeutralMode.Coast)
            self.arm.grabberMotor.motor.setNeutralMode(ctre.NeutralMode.Coast)

            self.mode = 'Coast'


        
        # self.arm.holdAtPercentage(-0.135, -0.105, 0.125)



        

        # For cone for future reference: self.arm.holdAtPercentage(0.0, 0.0, 0.145)

    def end(self, interrupted):
        #self.arm.holdAtPos(self.arm.baseMotor.motor.getSelectedSensorPosition(), self.arm.midMotor.motor.getSelectedSensorPosition(), self.arm.baseMotor.motor.getSelectedSensorPosition())
        pass

    def isFinished(self):
        """
        Return whether or not the command is finished.
        """

        # return wpilib.Timer.getFPGATimestamp() - self.start >= 30
        return False
