import commands2
import wpilib
from subsystems.arm import Arm
from subsystems.drivetrain import Drivetrain

class StationCorrection(commands2.CommandBase):

    def __init__(self, train: Drivetrain, arm: Arm):

        super().__init__()

        self.train = train
        self.arm = arm
        self.timer = wpilib.Timer()

        self.addRequirements([self.train, self.arm])

        wpilib.SmartDashboard.putNumber("Time", self.timer.get())

    def initialize(self):

        self.train.onChargeStation = False
        self.timer.stop()
        self.timer.reset()

        wpilib.SmartDashboard.putNumber("Time", self.timer.get())

    def execute(self):

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

        wpilib.SmartDashboard.putBoolean("Running", True)

    def end(self, interrupted: bool):

        self.train.arcadeDrive(0.0, 0.0, False)
        wpilib.SmartDashboard.putBoolean("Running", False)

    def isFinished(self):
        return False



class StationCorrectionMobility(commands2.CommandBase):

    def __init__(self, train: Drivetrain, arm: Arm):

        super().__init__()

        self.train = train
        self.arm = arm
        self.timer = wpilib.Timer()

        self.drift = 0

        self.addRequirements([self.train, self.arm])

        wpilib.SmartDashboard.putNumber("Time", self.timer.get())

        # self.commandFinished = False

    def initialize(self):

        self.train.onChargeStation = False
        self.train.offChargeStation = False
        self.train.onChargeStation2 = False

        self.timer.stop()
        self.timer.reset()

        self.startTime = wpilib.Timer.getFPGATimestamp()

        self.timer.start()

        wpilib.SmartDashboard.putNumber("Time", self.timer.get())

    def execute(self):

        wpilib.SmartDashboard.putNumber("Angle", self.train.gyro.getAngle())
        wpilib.SmartDashboard.putNumber("Time", self.timer.get())

        if self.train.gyro.getAngle() <= 12.5 and not self.train.onChargeStation and not self.train.offChargeStation:

            self.train.arcadeDrive(-0.35, 0.0, True)

            wpilib.SmartDashboard.putString("Auto Status", "Driving to Station")

        elif self.timer.get() <= 3.5:

            self.train.onChargeStation = True
            self.train.arcadeDrive(-0.3, 0.0, True)

            wpilib.SmartDashboard.putString("Auto Status", "1st On CS")

        elif not self.train.offChargeStation:

            self.drift = self.train.gyro.getAngle()
            self.train.offChargeStation = True

            wpilib.SmartDashboard.putString("Auto Status", "Off CS")

        elif self.train.gyro.getAngle() - self.drift >= -7.5 and not self.train.onChargeStation2:

            self.train.arcadeDrive(0.35, 0.0, True)

            wpilib.SmartDashboard.putString("Auto Status", "2nd Driving to Station")

            self.train.gyro.getAngle() - self.drift >= -7.5

        else:

            self.train.onChargeStation2 = True

            power = (self.train.pidController.calculate(self.train.gyro.getAngle(), 0.0))

            wpilib.SmartDashboard.putNumber("Requested Power", power)
            wpilib.SmartDashboard.putString("Auto Status", "PID Control")

            if abs(power) <= 0.5:

                self.train.arcadeDrive(power, 0.0, True)

                wpilib.SmartDashboard.putBoolean("Power Accepted?", True)

            else:

                wpilib.SmartDashboard.putBoolean("Power Accepted?", False)

        self.arm.keepArmsAtZero()

        wpilib.SmartDashboard.putBoolean("Running?", True)
        wpilib.SmartDashboard.putBoolean("Off CS?", self.train.offChargeStation)
        wpilib.SmartDashboard.putBoolean("On CS?", self.train.onChargeStation or self.train.onChargeStation2)

        wpilib.SmartDashboard.putNumber("Gyro Drift", self.drift)

    def end(self, interrupted: bool):

        self.train.arcadeDrive(0.0, 0.0, False)
        wpilib.SmartDashboard.putBoolean("Running", False)

    def isFinished(self):
        return False
