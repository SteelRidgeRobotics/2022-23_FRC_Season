import wpilib
import ctre

class LimitSwitchTest(wpilib.TimedRobot):

    def robotInit(self):
        
        # init limit switches (this aren't limit switch thingies)
        self.baseArmBack = ctre.LimitSwitchSource.RemoteTalon
        self.baseArmFront = ctre.LimitSwitchSource.RemoteTalon
        
        self.middleArmBack = ctre.LimitSwitchSource.RemoteTalon
        self.middleArmFront = ctre.LimitSwitchSource.RemoteTalon

        self.topArmBack = ctre.LimitSwitchSource.RemoteTalon
        self.topArmFront = ctre.LimitSwitchSource.RemoteTalon

    def teleopPeriodic(self):

        # Shows if the switch is pressed
        wpilib.SmartDashboard.putNumberArray('Base Arm (b/f)', [self.baseArmBack.get(), self.baseArmFront.get()])
        wpilib.SmartDashboard.putNumberArray('Middle Arm (b/f)', [self.middleArmBack.get(), self.middleArmFront.get()])
        wpilib.SmartDashboard.putNumberArray('Top Arm (b/f)', [self.topArmBack.get(), self.topArmFront.get()])

if __name__ == "__main__":

    wpilib.run(LimitSwitchTest)