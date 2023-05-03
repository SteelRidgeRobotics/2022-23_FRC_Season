import conversions
import math

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

    if math.fabs(curRev - (direction + curRev)) < math.fabs(curRev - direction):

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

    if math.fabs(currentAngle - direction) >= math.fabs(currentAngle - negAngle):

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

"""
rev = giveRevCompensation(cA, d)
print(str(d+rev))
"""
