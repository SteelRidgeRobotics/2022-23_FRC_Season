import commands2
import wpilib
import ctre
from subsystems.drivetrain import Drivetrain
from subsystems.arm import Arm

class StationCorrection(commands2.CommandBase):

    def __init__(self, train: Drivetrain, arm: Arm):

        super().__init__()

        self.train = train
        self.arm = arm
        self.timer = wpilib.Timer()
        
        self.addRequirements([self.train, self.arm])

        wpilib.SmartDashboard.putNumber("Time", self.timer.get())

        # self.startTime = wpilib.Timer.getFPGATimestamp()
        
        # self.commandFinished = False

    def initialize(self):

        self.train.onChargeStation = False
        self.timer.stop()
        self.timer.reset()
        
        wpilib.SmartDashboard.putNumber("Time", self.timer.get())

    def execute(self):

        # if self.commandFinished:

        #     self.startTime = wpilib.Timer.getFPGATimestamp()
        #     self.commandFinished = False

        wpilib.SmartDashboard.putNumber("Angle", self.train.gyro.getAngle())
        wpilib.SmartDashboard.putNumber("Time", self.timer.get())

        if self.train.gyro.getAngle() <= 7.5 and not self.train.onChargeStation:
            
            self.train.arcadeDrive(-0.3, 0.0, True)

            wpilib.SmartDashboard.putString("Auto Status", "Driving to Station")

        elif self.timer.get() <= 1:

            self.train.onChargeStation = True
            self.timer.start()

        else:
            
            power = (self.train.pidController.calculate(self.train.gyro.getAngle(), 0.0))

            wpilib.SmartDashboard.putNumber("Requested Power", power)
            wpilib.SmartDashboard.putString("Auto Status", "PID Control")

            if abs(power) <= 0.5:

                self.train.arcadeDrive(power, 0.0, True)

                wpilib.SmartDashboard.putBoolean("Power Accepted", True)

            else:

                wpilib.SmartDashboard.putBoolean("Power Accepted", False)
        
        self.arm.keepArmsAtZero()

        # wpilib.SmartDashboard.putNumberArray("Time", [wpilib.Timer.getFPGATimestamp(), wpilib.Timer.getFPGATimestamp() - self.startTime])
        wpilib.SmartDashboard.putBoolean("Running", True)

        # wpilib.SmartDashboard.putNumberArray("Time", [self.startTime, wpilib.Timer.getFPGATimestamp(), wpilib.Timer.getFPGATimestamp - self.startTime])

    def end(self, interrupted: bool):
        
        self.train.arcadeDrive(0.0, 0.0)
        wpilib.SmartDashboard.putBoolean("Running", False)
    
    def isFinished(self):
        return False