from kivy.event import EventDispatcher
from kivy.properties import StringProperty, ObjectProperty

class AppState(EventDispatcher):
    """
    Manages the global state of the application.
    It holds data that needs to be shared across different screens.
    """
    # Wi-Fi credentials
    wifi_ssid = StringProperty(None)
    wifi_password = StringProperty(None)

    # Last scanned meat identification code
    last_meat_code = StringProperty(None)

    # Holds the result type ('wifi' or 'meat') for the ResultScreen
    result_type = StringProperty(None)

    # Generic property to hold error messages
    error_message = StringProperty("Ocorreu um erro inesperado.")

    def is_wifi_configured(self):
        """Check if Wi-Fi credentials are set."""
        return self.wifi_ssid is not None and self.wifi_password is not None

    def clear_wifi_config(self):
        """Clears the current Wi-Fi configuration."""
        self.wifi_ssid = None
        self.wifi_password = None

    def clear_last_meat_code(self):
        """Clears the last scanned meat code."""
        self.last_meat_code = None
