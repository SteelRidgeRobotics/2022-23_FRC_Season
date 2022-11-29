import commands2
import wpilib
import typing
from subsystems.swerve_wheel import SwerveWheel
import conversions
import constants
class Joysticks(commands2.CommandBase):

    def __init__(self, robotcontainer: SwerveWheel, LeftX: typing.Callable[[], float], LeftY: typing.Callable[[], float], RightX: typing.Callable[[], float], RightY: typing.Callable[[], float]) -> None:
        super().__init__()
        self.robotcontainer = robotcontainer

        self.leftx = LeftX
        self.lefty = LeftY
        self.rightx = RightX
        self.righty = RightY
        #self.degrees = conversions.Conversions.convertJoystickInputToDegrees(LeftX(), LeftY())

        self.addRequirements((self.robotcontainer))

    def execute(self) -> None:
        #self.degrees = conversions.Conversions.convertJoystickInputToDegrees(self.leftx(), self.lefty())
        wpilib.SmartDashboard.putNumber("   LeftX - ", conversions.deadband(self.leftx(), constants.kdeadband))
        wpilib.SmartDashboard.putNumber("   Left Y - ", conversions.deadband(self.lefty(), constants.kdeadband))
        wpilib.SmartDashboard.putNumber("   RightX - ", conversions.deadband(self.rightx(), constants.kdeadband))
        wpilib.SmartDashboard.putNumber("   Right Y - ", conversions.deadband(self.righty(), constants.kdeadband))
        #wpilib.SmartDashboard.putNumber("   Left Degrees - ", self.degrees)
        
    
    def end(self, interrupted: bool) -> None:
        print()
    
    def isFinished(self) -> bool:
        return False
