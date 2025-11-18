from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty

class WiFiStatusScreen(Screen):
    """
    Displays the current Wi-Fi connection status.
    Provides options to configure Wi-Fi or proceed offline.
    The UI is defined in marmos.kv.
    """
    is_connected = BooleanProperty(False)

    def on_enter(self, *args):
        """
        Event handler for when the screen is entered.
        Here you could add logic to check the actual Wi-Fi status of the device.
        For now, it relies on the AppState.
        """
        # This is a placeholder. A real implementation would check the system's
        # network status. For this project, we just reflect the AppState.
        app = self.manager.app
        self.is_connected = app.state.is_wifi_configured()
