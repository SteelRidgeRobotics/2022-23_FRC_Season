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

def test():
    pass

cA = float(input("currentAngle? = "))
d = float(input("direction? = "))
print(str(conversions.giveRevCompensation(cA, d)))
print(str(conversions.getclosest(cA, d, 1)))