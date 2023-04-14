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
        # Inputs currently reversed, slider goes forward/backward, while joystick Y controls turning. WIll probably fix later.
        self.drive.userDrive(forwardSum(self.guitar.getJoystickY(), self.guitar.getSliderValue()), reverseSum(self.guitar.getJoystickY(), self.guitar.getSliderValue()), 0.5)

        wpilib.SmartDashboard.putNumberArray('Joystick - ', [self.guitar.getJoystickX(), self.guitar.getJoystickY()])
        wpilib.SmartDashboard.putBooleanArray("Fret Buttons: ", [self.guitar.getGreenButton(), self.guitar.getRedButton(), self.guitar.getYellowButton(), self.guitar.getBlueButton(), self.guitar.getOrangeButton()])
        wpilib.SmartDashboard.putBooleanArray("Strum Bar (U, D):", [self.guitar.getStrumBarUp(), self.guitar.getStrumBarDown()])
        wpilib.SmartDashboard.putNumber('Slider - ', self.guitar.getSliderValue())
        wpilib.SmartDashboard.putNumber("Whammy Bar - ", self.guitar.getWhammyBarRot())
        wpilib.SmartDashboard.putNumber("Left Velocity - ", self.drive.frontLeft.getSelectedSensorVelocity())
        wpilib.SmartDashboard.putNumber("Right Velocity - ", self.drive.frontRight.getSelectedSensorVelocity())

    def end(self, interrupted: bool) -> None:
        self.drive.stopMotors()

    def isFinished(self) -> bool:
        return False
    
def forwardSum(x, y) -> float:
        finalValue = -y + x
        if (finalValue > 1):
            finalValue = 1
        elif (finalValue < -1):
            finalValue = -1
        return finalValue

def reverseSum(x, y) -> float:
    finalValue = -y - x
    if (finalValue > 1):
        finalValue = 1
    elif (finalValue < -1):
        finalValue = -1
    return finalValue
