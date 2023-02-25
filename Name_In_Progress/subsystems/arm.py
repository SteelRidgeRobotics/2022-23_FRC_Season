import commands2
import ctre
import constants

class Arm(commands2.SubsystemBase):

    def __init__(self):

        super().__init__()
        self.baseMotor = ctre.TalonFX(constants.ARMBASEPORT)
        self.midMotor = ctre.TalonFX(constants.ARMMIDPORT)
        self.topMotor = ctre.TalonFX(constants.ARMTOPPORT)
        self.grabberMotor = ctre.TalonFX(constants.ARMGRABBERPORT)
        self.wristMotor = ctre.TalonSRX(constants.ARMGRABBERWRISTPORT)

        # neutral modes
        self.baseMotor.setNeutralMode(ctre.NeutralMode.Brake)
        self.midMotor.setNeutralMode(ctre.NeutralMode.Brake)
        self.topMotor.setNeutralMode(ctre.NeutralMode.Brake)
        self.grabberMotor.setNeutralMode(ctre.NeutralMode.Brake)
        self.wristMotor.setNeutralMode(ctre.NeutralMode.Brake)

        # set up limit switches
        self.baseMotor.configForwardLimitSwitchSource(ctre.LimitSwitchSource.RemoteTalon, ctre.LimitSwitchNormal.NormallyOpen, 4, 10)
        self.midMotor.configForwardLimitSwitchSource(ctre.LimitSwitchSource.RemoteTalon, ctre.LimitSwitchNormal.NormallyOpen, 5, 10)
        self.topMotor.configForwardLimitSwitchSource(ctre.LimitSwitchSource.RemoteTalon, ctre.LimitSwitchNormal.NormallyOpen, 6, 10)
        self.grabberMotor.configForwardLimitSwitchSource(ctre.LimitSwitchSource.RemoteTalon, ctre.LimitSwitchNormal.NormallyOpen, 7, 10)
        
        self.baseMotor.configReverseLimitSwitchSource(ctre.LimitSwitchSource.RemoteTalon, ctre.LimitSwitchNormal.NormallyOpen, 4, 10)
        self.midMotor.configReverseLimitSwitchSource(ctre.LimitSwitchSource.RemoteTalon, ctre.LimitSwitchNormal.NormallyOpen, 5, 10)
        self.topMotor.configReverseLimitSwitchSource(ctre.LimitSwitchSource.RemoteTalon, ctre.LimitSwitchNormal.NormallyOpen, 6, 10)
        self.grabberMotor.configReverseLimitSwitchSource(ctre.LimitSwitchSource.RemoteTalon, ctre.LimitSwitchNormal.NormallyOpen, 7, 10)

        # choose sensors
        self.baseMotor.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)
        self.midMotor.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)
        self.topMotor.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)
        self.grabberMotor.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)
        self.wristMotor.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder)
        """
        # set up motion magic

        # config PID values
        self.baseMotor.config_kF() 
        self.baseMotor.config_kP()
        self.baseMotor.config_kD()

        self.midMotor.config_kF()
        self.midMotor.config_kP()
        self.midMotor.config_kD()

        self.topMotor.config_kF()
        self.topMotor.config_kP()
        self.topMotor.config_kD()

        self.grabberMotor.config_kF()
        self.grabberMotor.config_kP()
        self.grabberMotor.config_kD()

        self.wristMotor.config_kF()
        self.wristMotor.config_kP()
        self.wristMotor.config_kD()

        # config cruising velocity
        self.baseMotor.configMotionCruiseVelocity()
        self.midMotor.configMotionCruiseVelocity()
        self.topMotor.configMotionCruiseVelocity()
        self.grabberMotor.configMotionCruiseVelocity()
        self.wristMotor.configMotionCruiseVelocity()

        # config acceleration
        self.baseMotor.configMotionAcceleration()
        self.midMotor.configMotionAcceleration()
        self.topMotor.configMotionAcceleration()
        self.grabberMotor.configMotionAcceleration()
        self.wristMotor.configMotionAcceleration()
        
        # invert sensors
        self.baseMotor.setSensorPhase(False)
        self.midMotor.setSensorPhase(False)
        self.topMotor.setSensorPhase(False)
        self.grabberMotor.setSensorPhase(False)
        self.wristMotor.setSensorPhase(False)
        
        """

        
        
    def moveArmToPose(self, base, mid, top, grabber, wrist):
        """
        Move the arm to a specific pose.
        Requires angles for the base, middle, top, grabber, and wrist motors.
        """
    
    def setGrabber(self, bool):
        """
        Tell the grabber to open or close
        Requires a boolean to say whether to open or close the grabber.
        True closes the grabber, False opens it.
        """
        