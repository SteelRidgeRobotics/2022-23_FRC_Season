import math


def convertDegreesToTalonFXUnits(num: float) -> float:
    conversionFactor = 2048 / 360  # 1 revolution of the falcon 500 is 2048 units
    num *= conversionFactor
    return num


def convertTalonFXUnitsToDegrees(num: float) -> float:
    num *= (360 / 2048)
    return num


def sign(num) -> int:
    if num > 0:
        # positive
        return 1
    elif num < 0:
        # negative
        return -1
    else:
        # zero
        return 0

"""
def convertJoystickInputToDegrees(x: float,
                                  y: float):  # this allows us to use the x and y values on the joystick and convert it into degrees
    if sign(x) == -1:
        return float(
            math.degrees(math.atan2(x, -y)) + 360.0)  # this will make sure that it gives us a number between 0 and 360
    else:
        if float(math.degrees(
                 math.atan2(x, -y))) == 360.0:  # This makes sure that if we get 360.0 degrees, it will be zero
            return 0.0
        else:
            return float(math.degrees(
                         math.atan2(x, -y)))  # the degrees, the joystick up is zero and the values increase clock-wise
"""
def convertJoystickInputToDegrees(x: float, y: float):
    return float(math.degrees(math.atan2(x, -y)))


def deadband(value: float, band: float):
    # this makes sure that joystick drifting is not an issue.
    # It takes the small values and forces it to be zero if smaller than the band value
    if math.fabs(value) <= band:
        return 0
    else:
        return value
