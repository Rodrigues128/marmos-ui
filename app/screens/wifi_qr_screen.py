from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from app.services.qr_decoder import QRDecoder

class WiFiQRScreen(Screen):
    """
    This screen uses the camera to scan a Wi-Fi QR code.
    It handles the decoding logic and transitions to the result screen on success.
    """

    def on_enter(self, *args):
        """
        Called when the screen is entered. Starts the camera.
        """
        self.ids.camera_service.is_active = True
        # Bind the on_qr_decoded event from the camera service
        self.ids.camera_service.bind(on_qr_decoded=self.on_qr_code_scanned)

    def on_leave(self, *args):
        """
        Called when the screen is left. Stops the camera to save resources.
        """
        self.ids.camera_service.is_active = False
        self.ids.camera_service.unbind(on_qr_decoded=self.on_qr_code_scanned)

    def on_qr_code_scanned(self, instance, qr_data):
        """
        Callback for when the camera service detects a QR code.
        """
        if not qr_data:
            return

        # Stop the camera immediately to prevent multiple decodes
        self.ids.camera_service.is_active = False

        # Attempt to parse the QR data as a Wi-Fi code
        decoder = QRDecoder()
        wifi_credentials = decoder.parse_wifi_qr(qr_data)

        if wifi_credentials:
            # If successful, update the app state
            app = self.manager.app
            app.state.wifi_ssid = wifi_credentials['ssid']
            app.state.wifi_password = wifi_credentials['password']
            app.state.result_type = 'wifi'
            
            # Go to the result screen
            self.manager.current = 'result_screen'
        else:
            # If it's not a valid Wi-Fi QR code, show an error or ignore.
            # For a better UX, we can provide feedback. For now, just restart the camera.
            # A small delay can prevent instant re-scans of the wrong code.
            Clock.schedule_once(self.reactivate_camera, 1.5)
            # You could also switch to an error screen or show a popup.
            print(f"Scanned a non-WIFI QR code: {qr_data}")

    def reactivate_camera(self, dt):
        """Reactivates the camera after a short delay."""
        if self.manager.current == 'wifi_qr_screen':
            self.ids.camera_service.is_active = True

    def go_back(self):
        """
        Allows the user to cancel the operation and go back.
        The target screen depends on whether Wi-Fi was already configured.
        """
        app = self.manager.app
        if app.state.is_wifi_configured():
            self.manager.current = 'home_screen'
        else:
            self.manager.current = 'wifi_status_screen'
