import commands2
import wpilib
from subsystems.drivetrain import Drivetrain


class JoystickDrive(commands2.CommandBase):

    def __init__(self, train: Drivetrain, left, right, leftBumper, rightBumper, buttonA):

        super().__init__()

        self.train = train

        self.leftFunc = left
        self.rightFunc = right
        self.leftBumperFunc = leftBumper
        self.rightBumperFunc = rightBumper
        self.buttonAFunc = buttonA

        self.placeMode = False

        self.addRequirements([self.train])

    def execute(self):

        self.left = self.leftFunc()
        self.right = self.rightFunc()
        self.leftBumper = self.leftBumperFunc()
        self.rightBumper = self.rightBumperFunc()

        wpilib.SmartDashboard.putNumberArray(
            "LRJoy", [self.left, self.leftBumper, self.right, self.rightBumper])

        if self.buttonAFunc():
            self.placeMode = not self.placeMode

        if self.placeMode:
            self.left *= 0.17
            self.right *= 0.17

        if self.leftBumper or self.rightBumper:
            self.left *= 0.5
            self.right *= 0.5

        self.train.arcadeDrive(self.left, self.right, False)

        wpilib.SmartDashboard.putNumber(
            "Gyro", self.train.gyro.getAngle())

        wpilib.SmartDashboard.putBoolean("Place Mode", self.placeMode)

    def end(self, interrupted):

        self.train.arcadeDrive(0.0, 0.0, False)

    def isFinished(self):

        return False
