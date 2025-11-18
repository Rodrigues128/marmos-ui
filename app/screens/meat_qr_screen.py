from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

class MeatQRScreen(Screen):
    """
    This screen uses the camera to scan a meat identification QR code.
    It will accept any QR code that is not a Wi-Fi configuration code.
    """

    def on_enter(self, *args):
        """
        Called when the screen is entered. Starts the camera.
        """
        self.ids.camera_service.is_active = True
        self.ids.camera_service.bind(on_qr_decoded=self.on_qr_code_scanned)

    def on_leave(self, *args):
        """
        Called when the screen is left. Stops the camera.
        """
        self.ids.camera_service.is_active = False
        self.ids.camera_service.unbind(on_qr_decoded=self.on_qr_code_scanned)

    def on_qr_code_scanned(self, instance, qr_data):
        """
        Callback for when the camera service detects a QR code.
        """
        if not qr_data:
            return

        # It's a meat QR code if it's NOT a Wi-Fi QR code.
        if not qr_data.startswith("WIFI:"):
            # Stop the camera to prevent multiple decodes
            self.ids.camera_service.is_active = False

            # Update the app state
            app = self.manager.app
            app.state.last_meat_code = qr_data
            app.state.result_type = 'meat'
            
            # Go to the result screen
            self.manager.current = 'result_screen'
        else:
            # This is a Wi-Fi QR code, which is not what we want here.
            # Give feedback to the user (optional) and restart the camera.
            print("Scanned a Wi-Fi QR code on the meat screen. Ignoring.")
            # A small delay can prevent instant re-scans of the wrong code.
            Clock.schedule_once(self.reactivate_camera, 1.5)

    def reactivate_camera(self, dt):
        """Reactivates the camera after a short delay."""
        if self.manager.current == 'meat_qr_screen':
            self.ids.camera_service.is_active = True

    def go_to_home(self):
        """Allows the user to cancel and return to the home screen."""
        self.manager.current = 'home_screen'
