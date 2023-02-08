"""
NOT DONE BY A LONG SHOT
"""

import commands2
import wpilib
import ctre
from subsystems.drivetrain import Drivetrain

class StationCorrection(commands2.CommandBase):

    def __init__(self, train: Drivetrain):

        super().__init__()

        self.train = train
        
        self.addRequirements([self.train])

    def execute(self):

        wpilib.SmartDashboard.putNumber("Angle", self.train.gyro.getAngle())

        if self.train.gyro.getAngle() <= 7.5 and not self.train.onChargeStation:

            self.train.arcadeDrive(0.2, 0.0)

            wpilib.SmartDashboard.putString("Auto Status", "Driving to Station")
        
        else:

            self.train.onChargeStation = True
            
            power = -(self.train.pidController.calculate(self.train.gyro.getAngle(), 0.0))

            wpilib.SmartDashboard.putNumber("Requested Power", power)

            wpilib.SmartDashboard.putString("Auto Status", "PID Control")

            if abs(power) <= 0.5:

                self.train.arcadeDrive(power, 0.0)

                wpilib.SmartDashboard.putBoolean("Power Accepted", True)

            else:

                wpilib.SmartDashboard.putBoolean("Power Accepted", False)

    def end(self, interrupted: bool):
        
        self.train.arcadeDrive(0.0, 0.0)
    
    def isFinished(self):

        return False