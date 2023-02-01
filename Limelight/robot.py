
import ntcore
import wpilib

class MyRobot(wpilib.TimedRobot):
    """
    def robotInit(self) -> None:
    
    def teleopInit(self) -> None:
    """
    
    def teleopPeriodic(self) -> None:

        inst = ntcore.NetworkTableInstance.getDefault()
        table = inst.getTable("limelight")
        tx = table.getNumber('tx',None)
        ty = table.getNumber('ty',None)
        ta = table.getNumber('ta',None)
        ts = table.getNumber('ts',None)
        wpilib.SmartDashboard.putNumber("tx", tx)
        wpilib.SmartDashboard.putNumber("ty", ty)
        wpilib.SmartDashboard.putNumber("ta", ta)
        wpilib.SmartDashboard.putNumber("ts", ts)

if __name__ == "__main__":
    wpilib.run(MyRobot)