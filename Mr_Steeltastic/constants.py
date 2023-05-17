import wpilib

DRIVERCONTROLLERPORT = 0
FUNCTIONSCONTROLLERPORT = 1

USINGGUITARCONTROLLER = True # Turn this to True if using the guitar controller. Everything will explode if you don't

FRONTLEFT = 0
BACKLEFT = 1
FRONTRIGHT = 2
BACKRIGHT = 3

ARMBASEPORT = 5
ARMMIDPORT = 4
ARMTOPPORT = 6
ARMGRABBERPORT = 7

# BASEENCODERPORT = -1
# MIDENCODERPORT = -1
# TOPENCODERPORT = -1
# GRABBERENCODERPORT = -1

# Arm Gear Ratios

BASERATIO = 48 * (74 / 18)
MIDDLERATIO = 48 * (50 / 18)
TOPRATIO = 12
GRABBERRATIO = 12

TIMEOUTMS = 10

CRUISEVELOCITY = 15000
CRUISEACCEL = 6000

# Motion Magic PIDF
MMP = 0.375
MMI = 0.0
MMD = 0.0
MMF = 0.0

DEADBAND = 0.02

# Normal P Control for Charge Station
# P og 0.0118
P = 0.0115
I = 0.0
D = 0.0013

ARMBASEP = 0.15 # Originally 0.1
ARMBASED = 0
#ARMBASEF = 0.225
ARMBASEF = 0.23

# ARMMIDP = 0.9
ARMMIDP = 0.8 #CUrrently guess
ARMMIDD = 0
#ARMMIDF = 0.05244
ARMMIDF = 0.05

# ARMTOPP = 1.5
ARMTOPP = 0.85
ARMTOPD = 0
#ARMTOPF = 0.27962
ARMTOPF = 0.75

# ARMGRABBERP = 0.29
ARMGRABBERP = 0.29
ARMGRABBERD = 0
#ARMGRABBERF = 0.2798
ARMGRABBERF = 0.3

ARMWRISTP = 0
ARMWRISTD = 0
ARMWRISTF = 0

# Cruising Velocities
ARMBASECRUISEVEL = 9000
ARMMIDCRUISEVEL = 4000
ARMTOPCRUISEVEL = 2000
ARMGRABBERCRUISEVEL = 200
#ARMWRISTCRUISEVEL = 10

# Motion Acceleration
ARMBASEACCEL = 9000
ARMMIDACCEL = 4000
ARMTOPACCEL = 2000
ARMGRABBERACCEL = 180
#ARMWRISTACCEL = 100

# Hold Percentages
ARMBASEHOLDPERCENT = -0.135 # Originally -0.135, changed because <insert reason here>
ARMMIDHOLDPERCENT = -0.105
ARMTOPHOLDPERCENT = 0.125
ARMGRABBERHOLDPERCENT = 0

# Solenoid on Grabber

SOLENOIDMODULE = 0
SOLENOIDMODULETYPE = wpilib.PneumaticsModuleType.CTREPCM
GRABBERSOLENOIDIN = 0
GRABBERSOLENOIDOUT = 1
