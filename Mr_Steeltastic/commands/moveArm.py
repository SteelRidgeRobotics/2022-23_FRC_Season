import commands2
import ctre
from subsystems.arm import Arm
from armSolverBot import ArmSolverBot

class MoveArm(commands2.CommandBase):
    
    def __init__(self, arm: Arm, targetX, targetY):

        super().__init__()

        self.arm = arm

        self.targetX = targetX
        self.targetY = targetY

        self.solver = ArmSolverBot(0, 0, 22, 22)

        self.addRequirements([self.arm])

    def execute(self):
        
        angles = self.solver.targetToAngles((self.targetX(), self.targetY()))
        self.arm.armToPos(angles[0] * (2048 / 360), angles[1] * (2048 / 360), 0, 0)

    def end(self):

        self.arm.armToPos(self.arm.baseMotor.getCurrentAngle() * (2048 / 360), self.arm.midMotor.getCurrentAngle() * (2048 / 360), 0, 0)

    def isFinished(self):

        return False