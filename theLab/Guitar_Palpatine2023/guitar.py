from wpilib import SmartDashboard
from wpilib.interfaces import GenericHID
from wpilib import XboxController


class Guitar(GenericHID):
    """
    Handle input from guitar controllers connected to the Driver Station.

    This class handles guitar input that comes from the Driver Station. Each time a value is requested the most recent value is returned. There is a single class instance for each controller and the mapping of ports to hardware buttons depends on the code in the Driver Station.
    """

    def __init__(self, port: int) -> None:
        super().__init__(port)

    class Axis():
        kJoyX = 0
        kJoyY = 1
        kWhamBar = 2
        kSlider = 4
        
    class Button():
        kGreen = 1
        kRed = 2
        kYellow = 3
        kBlue = 4
        kOrange = 5
        kStrumDown = 6
        kVol = 7
        kStar = 8
        kStrumUp = 9

    def sendValuesToSmartDashboard(s) -> None: # Renamed 'self' to 's' to keep this function readable
        """
        Adds all button and axis values to Smart Dashboard.
        """
        SmartDashboard.putNumberArray("Joystick XY", [s.getJoystickX(), s.getJoystickY()])
        SmartDashboard.putBooleanArray("Fret Buttons", [s.getGreenButton(), s.getRedButton(), s.getYellowButton(), s.getBlueButton(), s.getOrangeButton()])
        SmartDashboard.putBooleanArray("Strum Bar (Up, Down)", [s.getStrumBarUp(), s.getStrumBarDown()])
        SmartDashboard.putNumber("Slider", s.getSlider())
        SmartDashboard.putNumber("Whammy Bar", s.getWhammyBar())

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
        return self.getButton(self.Button.kGreen)
    
    def getRedButton(self) -> bool:
        """
        Returns true if the Red Fret button is being pressed.
        """
        return self.getButton(self.Button.kRed)

    def getYellowButton(self) -> bool:
        """
        Returns true if the Yellow Fret button is being pressed.
        """
        return self.getButton(self.Button.kYellow)

    def getBlueButton(self) -> bool:
        """
        Returns true if the Blue Fret button is being pressed.
        """
        return self.getButton(self.Button.kBlue)

    def getOrangeButton(self) -> bool:
        """
        Returns true if the Orange Fret button is being pressed.
        """
        return self.getButton(self.Button.kOrange)
    
    def getStrumBar(self) -> bool:
        """
        Returns true if the strum bar is being strummed/pressed up OR down.

        The strum bar is technically 2 buttons, but in case you want to treat it as 1 button (pushed either up or down) use this.
        """
        return self.getButton(self.Button.kStrumDown) or self.getButton(self.Button.kStrumUp)
    
    def getStrumBarUp(self) -> bool:
        """
        Returns true if the strum bar is being "strummed" upwards.

        Up is considered when you're facing the guitar and holding the guitar pointing right.
        """
        return self.getButton(self.Button.kStrumUp)
    
    def getStrumBarDown(self) -> bool:
        """
        Returns true if the strum bar is being "strummed" downwards.

        Down is considered when you're facing the guitar and holding the guitar pointing right.
        """
        return self.getButton(self.Button.kStrumDown)
    
    def getVolumeButtons(self) -> bool:
        """
        Returns true if either volume button is being pressed.

        Both volume buttons are recognized as 1 button in Driver Station.
        """
        return self.getButton(self.Button.kVol)
    
    def getStarPowerButton(self) -> bool:
        """
        Returns true if the Star Power button is being pressed.

        The Star Power button is located in between the volume buttons. It also says "Star Power" on it.
        """
        return self.getButton(self.Button.kStar)
    
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
        return self.getAxis(self.Axis.kJoyX)
    
    def getJoystickY(self) -> float:
        """
        Returns the current Y value of the joystick.

        Minimum value (may differ from guitar to guitar) is -0.94, maximum value is 0.78. (Values may differ between guitars)
        """
        return self.getAxis(self.Axis.kJoyY)
    
    def getWhammyBar(self) -> float:
        """
        Returns the current Whammy Bar rotation.

        The Whammy Bar only moves in 1 axis (recognized in Driver Station as Axis 2)
        """
        return self.getAxis(self.Axis.kWhamBar)
    
    def getSlider(self) -> float:
        """
        Returns current value of the slider (located beneath the Orange Fret button).

        Values range from -0.94 - 0.73.
        """
        return self.getAxis(self.Axis.kSlider)
    