import commands2
import ctre
from subsystems.arm import Arm


class JoystickControlArm(commands2.CommandBase):
    def __init__(self, arm: Arm, leftBumper, rightBumper, base, mid, top, grabber, X, Y):
        super().__init__()

        self.arm = arm

        self.base = base
        self.mid = mid
        self.top = top
        self.grabber = grabber
        self.X = X
        self.Y = Y

        self.leftBumper = leftBumper
        self.rightBumper = rightBumper

        self.addRequirements([self.arm])

    def execute(self) -> None:
        self.arm.baseMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.midMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.topMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)
        self.arm.grabberMotor.motor.setNeutralMode(ctre.NeutralMode.Brake)

        lvalue = 1
        if self.leftBumper():
            lvalue = -1

        rvalue = 1
        if self.rightBumper():
            rvalue = -1

        self.arm.manualbaseMotor(0.5 * self.base())
        self.arm.manualmidMotor(0.5 * self.mid())
        self.arm.manualtopMotor(lvalue * 0.5 * self.top())
        self.arm.manualgrabberMotor(rvalue * 0.2 * self.grabber())

    def end(self, interrupted: bool):
        self.arm.holdAtPercentage(0, 0, 0, 0)

    def isFinished(self) -> bool:
        return False
