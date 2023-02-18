import wpilib

class LimitSwitchTest(wpilib.TimedRobot):

    def robotInit(self):
        
        # init limit switches
        self.baseArmBack = wpilib.DigitalInput() # put stuff here
        self.baseArmFront = wpilib.DigitalInput()
        
        self.middleArmBack = wpilib.DigitalInput()
        self.middleArmFront = wpilib.DigitalInput()

        self.topArmBack = wpilib.DigitalInput()
        self.topArmFront = wpilib.DigitalInput()

    def teleopPeriodic(self):

        # Shows if the switch is pressed
        wpilib.SmartDashboard.putNumberArray('Base Arm (b/f)', [self.baseArmBack.get(), self.baseArmFront.get()]) 
        wpilib.SmartDashboard.putNumberArray('Middle Arm (b/f)', [self.middleArmBack.get(), self.middleArmFront.get()]) 
        wpilib.SmartDashboard.putNumberArray('Top Arm (b/f)', [self.topArmBack.get(), self.topArmFront.get()]) 
        
        
        
      