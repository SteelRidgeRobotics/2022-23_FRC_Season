import typing
import commands2
from subsystems.swerve_wheel import SwerveWheel
import wpilib
import constants
import conversions
import math
import ctre

class TurnToSpecificPoint(commands2.CommandBase):
    def __init__(self,  wheel: SwerveWheel, x: typing.Callable[[], float], y: typing.Callable[[], float]) -> None:
        super().__init__()
        self.wheel = wheel
        #self.units = conversions.convertDegreesToTalonFXUnits(conversions.convertJoystickInputToDegrees(x(), y()))
        self.x = x
        self.y = y
        self.addRequirements([self.wheel])

    def execute(self) -> None:
        self.angle = conversions.convertJoystickInputToDegrees(conversions.deadband(self.x(), constants.kdeadband), conversions.deadband(self.y(), constants.kdeadband))
        self.units = conversions.convertDegreesToTalonFXUnits(self.angle)
        self.magnitude = math.hypot(conversions.deadband(self.x(), constants.kdeadband), conversions.deadband(self.y(), constants.kdeadband))
        if self.magnitude >= 1.0:
            self.magnitude = 1.0
        # we calculate what we need to rotate the wheel to, keeping in mind the gear ratios

        #insert translate code here
        currentAngle = conversions.convertTalonFXUnitsToDegrees(self.wheel.directionMotor.getSelectedSensorPosition())
        if math.fabs(self.angle) >= 180.0:
            opposAngle = math.fabs(self.angle) - 180.0
        else:
            opposAngle = math.fabs(self.angle) + 180.0
        wpilib.SmartDashboard.putNumber(" Original Angle -", self.angle)
        wpilib.SmartDashboard.putNumber(" Abs Opposit Angle -", opposAngle)
        if self.magnitude != 0.0:
            if math.fabs(currentAngle - self.angle) <= math.fabs(currentAngle - opposAngle):
                #turn to the original angle
                if self.angle == 0.0:
                    if (2048*constants.ksteeringGearRatio) - self.units < self.wheel.directionMotor.getSelectedSensorPosition():
                        self.wheel.turn(2048*constants.ksteeringGearRatio)
                    else:
                        self.wheel.turn(0.0)
                else:
                    self.wheel.turn(self.units*constants.ksteeringGearRatio)
                #move command
                self.wheel.move(self.magnitude)
            else:
                #turn to the other angle
                if self.angle == 0.0:
                    if (2048*constants.ksteeringGearRatio) - conversions.convertDegreesToTalonFXUnits(opposAngle) < self.wheel.directionMotor.getSelectedSensorPosition():
                        self.wheel.turn(2048*constants.ksteeringGearRatio)
                    else:
                        self.wheel.turn(0.0)
                else:
                #change direction of the speed motor
                    self.wheel.turn(conversions.convertDegreesToTalonFXUnits(opposAngle)*constants.ksteeringGearRatio)
                #move command
                self.wheel.move(-self.magnitude)

        self.wheel.showStats()
        wpilib.SmartDashboard.putNumber("Setpoint -", self.units)
        wpilib.SmartDashboard.putNumber("Angle -", self.angle)
        wpilib.SmartDashboard.putNumber("Input to wheel -", self.units*constants.ksteeringGearRatio)
        wpilib.SmartDashboard.putNumber("Magnitude -", self.magnitude)
        wpilib.SmartDashboard.putNumber("Difference fro 2048 -", float((2048*constants.ksteeringGearRatio) - self.wheel.directionMotor.getSelectedSensorPosition()))
        

    def end(self, interrupted: bool) -> None:
        self.wheel.stopAllMotors()

    def isFinished(self) -> bool:
        return False
    
