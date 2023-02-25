import ctre
import wpilib

class Steeltastic(wpilib.TimedRobot):

    def robotInit(self):

        self.grabberMotor = ctre.TalonFX(7)
        self.grabberMotor.setNeutralMode(ctre.NeutralMode.Brake)
        self.driverController = wpilib.XboxController(0)

    def teleopPeriodic(self):

        self.grabberMotor.set(self.driverController.getLeftY() * 0.1)


if __name__ == "__main__":

    wpilib.run(Steeltastic)