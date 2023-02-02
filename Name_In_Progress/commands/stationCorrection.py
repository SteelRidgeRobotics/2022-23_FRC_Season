"""
NOT DONE BY A LONG SHOT
"""

import commands2
import wpilib
import wpimath.controller
import ctre
import constants
from subsystems.drivetrain import Drivetrain

class DriveForward(commands2.CommandBase):

    def __init__(self, train: Drivetrain, distance: float):

        super().__init__()

        self.train = train
        
        self.addRequirements([self.train])
        
        self.onChargeStation = False

    def execute(self):

        wpilib.SmartDashboard.putNumber("Angle", self.train.gyro.getAngle())

        if self.train.gyro.getAngle() <= 7.5 and not self.onChargeStation:

            self.train.frontLeft.set(ctre.TalonFXControlMode.PercentOutput, 0.2)
            self.train.frontRight.set(ctre.TalonFXControlMode.PercentOutput, 0.2)

            wpilib.SmartDashboard.putString("Auto Status", "Driving to Station")

    def end(self, interrupted: bool):
        
        self.train.frontLeft.set(ctre.TalonFXControlMode.PercentOutput, 0.0)
        self.train.frontRight.set(ctre.TalonFXControlMode.PercentOutput, 0.0)
    
    def isFinished(self):

        pass