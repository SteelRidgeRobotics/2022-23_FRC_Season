import math

#Controller ports
kdriverControllerPort = 0
kfunctionsControllerPort = 1

#Motors
kfrontLeft = 0
kbackLeft = 1
kfrontRight = 2
kbackRight = 3

#Encoders
ktimeoutMs = 10

#Autonomous
kAutoBackupDistanceFeet = 8                                                                                                                                                                                                                                          
kAutoDriveSpeed = 1

#Motion Magic
kdistanceToTravel = 8.0
kSlotIdx = 0
kPIDLoopIdx = 0
kmotorCruiseVelocity = 15000 #please change this
kmotorAcceleration = 6000 #this too

kF = 0.0509563647
kP = 0.375
kD = 11.25
kI = 0.0


#Physical constants
kunitsPerRotation = 2048.0
kwheelCircumference = 1.57 #this is in feet