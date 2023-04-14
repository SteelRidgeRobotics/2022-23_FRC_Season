import wpilib
from wpilib.interfaces import GenericHID

class Guitar(GenericHID):
    """
    Handle input from guitar controllers connected to the Driver Station.

    This class handles guitar input that comes from the Driver Station. Each time a value is requested the most recent value is returned. There is a single class instance for each controller and the mapping of ports to hardware buttons depends on the code in the Driver Station.
    """

    def __init__(self, port: int) -> None:
        super().__init__(port)

    def getButton(self, id) -> bool:
        """
        Returns a button with the given id. 
        
        This is mainly used as a helper function for the other button methods, but can be used for any externally added buttons.
        """
        return super().getRawButton(id)
    
    def getGreenButton(self) -> bool:
        """
        Returns true if the Green Fret button is being pressed.
        """
        return self.getButton(1)
    
    def getRedButton(self) -> bool:
        """
        Returns true if the Red Fret button is being pressed.
        """
        return self.getButton(2)

    def getYellowButton(self) -> bool:
        """
        Returns true if the Yellow Fret button is being pressed.
        """
        return self.getButton(3)

    def getBlueButton(self) -> bool:
        """
        Returns true if the Blue Fret button is being pressed.
        """
        return self.getButton(4)

    def getOrangeButton(self) -> bool:
        """
        Returns true if the Orange Fret button is being pressed.
        """
        return self.getButton(5)
    
    def getStrumBar(self) -> bool:
        """
        Returns true if the strum bar is being pressed up OR down.

        The strum bar is technically 2 buttons, but in case you want to treat it as 1 button (pushed either up or down) use this.
        """
        return self.getButton(6) or self.getButton(9)
    
    def getStrumBarUp(self) -> bool:
        """
        Returns true if the strum bar is being "strummed" or pressed up.

        Up is considered when you're facing the guitar and holding the guitar pointing right.
        """
        return self.getButton(9)
    
    def getStrumBarDown(self) -> bool:
        """
        Returns true if the strum bar is being "strummed" or pressed down.

        Down is considered when you're facing the guitar and holding the guitar pointing right.
        """
        return self.getButton(6)
    
    def getVolumeButtonsPressed(self) -> bool:
        """
        Returns true if either volume button is being pressed.

        Both volume buttons are recognized as 1 button in Driver Station.
        """
        return self.getButton(7)
    
    def getStarPowerButtonPressed(self) -> bool:
        """
        Returns true if the Star Power button is being pressed.

        The Star Power button is located in between the volume buttons. It also says "Star Power" on it.
        """
        return self.getButton(8)
    
    def getAxis(self, id) -> float:
        """
        Returns the current value of an axis with the given id.

        This should only be used if an axis was externally added to the guitar, since all axes have their own methods.
        """
        return super().getRawAxis(id)
    
    def getJoystickX(self) -> float:
        """
        Returns the current X value of the joystick.

        Minimum value (may differ from guitar to guitar) is -0.75, maximum value is 0.81. (Values may differ between guitars)
        """
        return self.getAxis(0)
    
    def getJoystickY(self) -> float:
        """
        Returns the current Y value of the joystick.

        Minimum value (may differ from guitar to guitar) is -0.94, maximum value is 0.78. (Values may differ between guitars)
        """
        return self.getAxis(1)
    
    def getWhammyBarRot(self) -> float:
        """
        Returns the current Whammy Bar rotation.

        The Whammy Bar only moves in 1 axis (recognized in Driver Station as Axis 2)
        """
        return self.getAxis(2)
    
    def getSliderValue(self) -> float:
        """
        Returns current value of the slider (located beneath the Orange Fret button).

        Values range from -0.94 - 0.73.
        """
        return self.getAxis(4)
    