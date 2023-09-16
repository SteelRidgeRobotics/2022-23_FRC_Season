import math

# motors
kleftFrontSpeedID = 0
kleftRearSpeedID = 1
krightFrontSpeedID = 2
krightRearSpeedID = 3

kleftFrontDirectionID = 4
kleftRearDirectionID = 5
krightFrontDirectionID = 6
krightRearDirectionID = 7

kdriverControllerPort = 0
kdeadband = 0.15

# Encoders
ktimeoutMs = 10
kF = 0.05282272  # Feed forward
kP = 0.2  # Proportional
kI = 0.004  # Integral
kD = 2  # Derivative
kIzone = 150
kcruiseVel = 10567.0  # Cruise Velocity at 50% of max
kcruiseAccel = 10567.0  # Cruise Acceleration same as velocity
kticksPerRev = 2048
kSlotIdx = 0
kPIDLoopIdx = 0

# CANCoders
# CAN coders
kflCANcoderID = 10
krlCANcoderID = 11
kfrCANcoderID = 12
krrCANcoderID = 13

# offsets
kflCANoffset = 168.662
krlCANoffset = 105.380859375
kfrCANoffset = 302.431640625
krrCANoffset = 210.234

ksteeringGearRatio = 150 / 7

klength = 29
kwidth = 29
kr = math.sqrt((klength ** 2) + (kwidth ** 2))  # ** is the exponent operator
