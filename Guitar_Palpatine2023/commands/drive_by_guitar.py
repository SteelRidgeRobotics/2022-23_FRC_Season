import typing

import commands2
import wpilib
from subsystems.drivetrain import Drivetrain
from guitar import Guitar

class DriveByGuitar(commands2.CommandBase):
    """
    This allows us to drive the robot with a Wii Guitar Controller. Yep. This is what we're doing right now.
    """

    def __init__(self, drive: Drivetrain, guitar: Guitar) -> None:
        super().__init__()

        self.drive = drive
        self.guitar = guitar

        self.addRequirements([self.drive])

    def execute(self) -> None:
        self.drive.userDrive(forwardSum(-self.guitar.getSlider(), -self.guitar.getJoystickY()), reverseSum(-self.guitar.getSlider(), -self.guitar.getJoystickY()), 0.33)

        self.guitar.sendValuesToSmartDashboard()
        wpilib.SmartDashboard.putNumber("Forward Sum - ", forwardSum(self.guitar.getSlider(), self.guitar.getJoystickY()))
        wpilib.SmartDashboard.putNumber("Reverse Sum - ", reverseSum(self.guitar.getSlider(), self.guitar.getJoystickY()))
        wpilib.SmartDashboard.putNumber("Left Velocity - ", self.drive.frontLeft.getSelectedSensorVelocity())
        wpilib.SmartDashboard.putNumber("Right Velocity - ", self.drive.frontRight.getSelectedSensorVelocity())

    def end(self, interrupted: bool) -> None:
        self.drive.stopMotors()

    def isFinished(self) -> bool:
        return False
    
def clamp(n, minn, maxn):
    """
    Simple number cap:
    If n < minn, n = minn OR if n > maxn, n = maxn
    """
    return max(min(maxn, n), minn)
    
def forwardSum(x, y) -> float:
        finalValue = -y + x
        return clamp(finalValue, -1, 1)

def reverseSum(x, y) -> float:
    finalValue = -y - x
    return clamp(finalValue, -1, 1)
