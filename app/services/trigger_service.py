from kivy.event import EventDispatcher
from kivy.logger import Logger

# GPIO Zero is specific to Raspberry Pi. We need to handle imports gracefully
# so the app can run on other platforms for development.
try:
    from gpiozero import Button
    GPIO_AVAILABLE = True
except (ImportError, NotImplementedError):
    GPIO_AVAILABLE = False
    Logger.warning("TriggerService: 'gpiozero' library not found. Physical trigger button will be disabled.")

# According to the project requirements
TRIGGER_PIN = 23

class TriggerService(EventDispatcher):
    """
    Manages the physical trigger button connected to a GPIO pin.
    It uses 'gpiozero' and dispatches an 'on_press' event when triggered.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_press')
        self.button = None

        if GPIO_AVAILABLE:
            try:
                # Initialize the button on GPIO 23 with a pull-up resistor.
                # The button is expected to connect the pin to ground when pressed.
                self.button = Button(TRIGGER_PIN, pull_up=True, bounce_time=0.1)
                self.button.when_pressed = self.button_pressed_callback
                Logger.info(f"TriggerService: Successfully initialized button on GPIO {TRIGGER_PIN}.")
            except Exception as e:
                Logger.error(f"TriggerService: Failed to initialize GPIO pin {TRIGGER_PIN}. Error: {e}")
                self.button = None
        else:
            # Create a mock button for development on non-Pi platforms
            self.button = self.MockButton()
            Logger.info("TriggerService: Using mock button for development.")


    def button_pressed_callback(self):
        """
        Internal callback for when the gpiozero button is pressed.
        This method dispatches the Kivy event.
        """
        Logger.info("TriggerService: Physical button pressed.")
        self.dispatch('on_press')

    def on_press(self, *args):
        """
        Default event handler for the 'on_press' event.
        This can be bound to from the main application.
        """
        pass

    def stop(self):
        """Clean up GPIO resources."""
        if GPIO_AVAILABLE and self.button:
            self.button.close()
            Logger.info("TriggerService: GPIO resources released.")

    class MockButton:
        """A mock button class for development on non-Raspberry Pi systems."""
        when_pressed = None
        def close(self):
            pass
