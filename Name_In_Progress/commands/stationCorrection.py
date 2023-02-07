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
        
        self.onChargeStation = False

    def execute(self):

        wpilib.SmartDashboard.putNumber("Angle", self.train.gyro.getAngle())

        if self.train.gyro.getAngle() <= 7.5 and not self.onChargeStation:

            self.train.FLMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.2)
            self.train.FRMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.2)

            wpilib.SmartDashboard.putString("Auto Status", "Driving to Station")
        
        else:

            self.onChargeStation = True
            
            power = self.train.pidController.calculate(self.train.gyro.getAngle(), 0.0)

            wpilib.SmartDashboard.putNumber("Requested Power", power)

            wpilib.SmartDashboard.putString("Auto Status", "PID Control")

            if abs(power) <= 0.5:

                self.train.FLMotor.set(ctre.TalonFXControlMode.PercentOutput, power)
                self.train.FRMotor.set(ctre.TalonFXControlMode.PercentOutput, power)

                wpilib.SmartDashboard.putBoolean("Power Accepted", True)

            else:

                wpilib.SmartDashboard.putBoolean("Power Accepted", False)

    def end(self, interrupted: bool):
        
        self.train.FLMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.0)
        self.train.FRMotor.set(ctre.TalonFXControlMode.PercentOutput, 0.0)
    
    def isFinished(self):

        return False