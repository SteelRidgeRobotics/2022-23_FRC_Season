import conversions
import math

"""
def test(direction):
    if direction < 0:

        opposAngle = direction + 180
        negAngle = 360 + direction

    elif direction > 0:

        opposAngle = direction - 180
        negAngle = direction - 360
        
    else:

        if conversions.sign(direction) == -1:

            opposAngle = -180
            negAngle = 0

        else:

            opposAngle = 180
            negAngle = 0


def giveRevCompensation(currentAngle, direction):

    revCompensation = conversions.getRevolutions(currentAngle)
    curRev = revCompensation * 360
    print("curRevComp: " + str(revCompensation))

    if conversions.sign(currentAngle) == 1:

        print("Sign: 1")

    else:

        print("Sign: -1")

    print("With compensation " + str(curRev - (direction + curRev)))
    print("Without compensation " + str(math.fabs(curRev - direction)))

    if direction == 0:
        print("direction is 0")

        ## current angle is also 0
        if conversions.sign(currentAngle) == 0:

            print("currentAngle is also 0")

            revCompensation = 0

        else: ##  359 => 360; 361 => 360
            print("curREV + 360 = " + str(curRev + 360))
            print("TEST\n"+ str((math.fabs(curRev + 360) + currentAngle)))
            print("FABS CURANGLE " + str(math.fabs(currentAngle)))
            if math.fabs((curRev + 360) - currentAngle) < math.fabs(currentAngle - curRev): ## 360 + 360 - 719 < currentAngle 

                print("go up rev")

                revCompensation = curRev + 360

            elif (math.fabs(curRev + 360) + currentAngle) < math.fabs(currentAngle - curRev):

                print("negative")
                revCompensation = (curRev - 360)

            elif math.fabs(currentAngle - curRev) < math.fabs(currentAngle): ## 361 - 360 < 361 ## -360 + 360 -1

                print("go down rev")

                revCompensation = currentAngle - (currentAngle - curRev)

    elif math.fabs(curRev - (direction + curRev)) < math.fabs(curRev - direction):

        print("revComp is closer")
        revCompensation *= 360
        print("revComp " + str(revCompensation))
    

    return revCompensation

def getclosest(currentAngle, direction):

    rev = giveRevCompensation(currentAngle, direction)

    if direction < 0:

        opposAngle = direction + 180
        negAngle = 360 + direction

    elif direction > 0:

        opposAngle = direction - 180
        negAngle = direction - 360
        
    else:

        if conversions.sign(direction) == -1:

            opposAngle = -180
            negAngle = 0

        else:

            opposAngle = 180
            negAngle = 0

    print("opposAngle = " + str(opposAngle + rev))
    print("negAngle = " + str(negAngle + rev))

    if direction == 0:
        
        return giveRevCompensation(currentAngle, direction)

    elif math.fabs(currentAngle - direction) >= math.fabs(currentAngle - negAngle):

        print("negAngle closer")
        return negAngle + rev

    elif math.fabs(currentAngle - direction) <= math.fabs(currentAngle - opposAngle):

        print("direction closer")
        return direction + rev

    else:

        print("opposAngle closer")
        return opposAngle + rev

cA = float(input("currentAngle? = "))
d = float(input("direction? = "))
closest = getclosest(cA, d)
print("closest = " + str(closest))

rev = giveRevCompensation(cA, d)
print("rev = " + str(rev))
print(str(d+rev))
"""
import math
from conversions import *
def roundToNearestRev(num):
    val = num % 360
    if val >= 180:
        val = num
    else:

    

def giveRevCompensation(currentAngle, direction):
    """
    currentAngle is the true angle, all the revolutions
    direction is the relative angle that we want to go to
    """
    originalAngle = currentAngle
    curRev = getRevolutions(currentAngle) * 360
    revCompensation = getRevolutions(currentAngle)
    currentAngle %= 360 ## now it is the angle relative to the revolution

    if direction == 0:
        print("direction is 0")

        ## current angle is also 0
        if sign(currentAngle) == 0:

            revCompensation = curRev

        else: ##  359 => 360; 361 => 360
            ## up
            print(str(originalAngle - curRev))
            print(str(originalAngle + curRev))
            if (originalAngle - curRev) > (0):
                print("up")
            else:
                print("down")

            if sign(curRev - originalAngle) == -1:

                print("upUP")
                revCompensation = curRev + 360

            elif (math.fabs(curRev + 360) + currentAngle) < math.fabs(originalAngle):
                print("down")
                revCompensation = (curRev - 360)
                
            elif math.fabs(currentAngle - curRev) < math.fabs(originalAngle): ## 361 - 360 < 361 ## -360 + 360 -1

                revCompensation = currentAngle - (currentAngle - curRev)

        if originalAngle % 360 == 0:
            print("gotcha!")
            revCompensation = curRev
    
    ## step down
    elif math.fabs(360 + currentAngle - direction) <= math.fabs(direction): ## (36)1 => 350

        print("step down")
        revCompensation = curRev - 360

    ## if it is closer not to add revCompensation
    elif math.fabs(currentAngle - direction) < math.fabs(curRev - (direction + curRev)):

        print("don't")
        revCompensation = curRev

    elif math.fabs(curRev - (direction + curRev)) <= math.fabs(curRev - direction):

        print(str(math.fabs(curRev - (direction + curRev))) + " <= " + str(math.fabs(curRev - direction)))
        print("stEP UP positive")
        revCompensation = (revCompensation + 1) * 360

    else:
        revCompensation = curRev

    print("(currentAngle) - (360)) ===== " + str(math.fabs((currentAngle) - (360))))
    print("(curRev + 360 + currentAngle) - (curRev + 360) == " + str((curRev + 360 + currentAngle) - (curRev + 360)))
    print("(curRev - direction) == " + str((curRev - direction)))
    return revCompensation

cA = float(input("currentAngle? = "))
d = float(input("direction? = "))
print(str(giveRevCompensation(cA, d)))
