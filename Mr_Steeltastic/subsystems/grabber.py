from ctre import TalonFX, TalonFXControlMode
from commands2 import SubsystemBase
from constants import *
from enum import Enum
from wpilib import SmartDashboard

class States(Enum):
        STOPPED = 0
        CLOCKWISE = 1
        COUNTERCLOCKWISE = 2

class Grabber(SubsystemBase):
    flywheel = TalonFX(FLYWHEELPORT)
    state = States.STOPPED

    def __init__(self) -> None:
        super().__init__()
        self.state = States.STOPPED

    def setToState(self, state: States) -> None:
        match state:
            case States.STOPPED:
                self.stop()
            case States.CLOCKWISE:
                self.pushAway()
            case States.COUNTERCLOCKWISE:
                self.pullTowards()

    def stop(self) -> None:
        self.flywheel.set(TalonFXControlMode.PercentOutput, 0)
        self.state = States.STOPPED
        SmartDashboard.putString("Grabber State", self.state.name)

    def pullTowards(self) -> None:
        self.flywheel.set(TalonFXControlMode.PercentOutput, -0.1)
        self.state = States.CLOCKWISE
        SmartDashboard.putString("Grabber State", self.state.name)

    def pushAway(self) -> None:
        self.flywheel.set(TalonFXControlMode.PercentOutput, 0.1)
        self.state = States.COUNTERCLOCKWISE
        SmartDashboard.putString("Grabber State", self.state.name)
