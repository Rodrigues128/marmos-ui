import os
# Set Kivy to fullscreen mode for the Raspberry Pi display
os.environ['KIVY_WINDOW'] = 'fullscreen'
# Use the fake KMS/DRM backend on Raspberry Pi
os.environ['KIVY_BCM_DISPMANX_ID'] = '4' # HDMI
os.environ['KIVY_EGL_DEVICE_ID'] = '/dev/dri/card0'

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock
from kivy.core.window import Window

from app.models.app_state import AppState
from app.services.trigger_service import TriggerService

class MarmosApp(App):
    """
    The main application class for the MARMOS-UI.
    It orchestrates the screens, state, and hardware services.
    """

    def build(self):
        """
        Initializes the application, loads the KV file, and sets up services.
        """
        self.title = 'MARMOS-UI'
        
        # Set fullscreen if the environment variable didn't catch it
        Window.fullscreen = 'auto'

        # Instantiate global state and services
        self.state = AppState()
        self.trigger_service = TriggerService()
        self.trigger_service.bind(on_press=self.on_physical_trigger)

        # Load the main KV file which defines the UI
        # The ScreenManager is the root widget
        sm = Builder.load_file('app/marmos.kv')
        
        # Add a reference to the app in the screen manager for easy access
        sm.app = self
        
        return sm

    def on_start(self):
        """
        Called after the build() method is finished.
        Handles the initial screen transition from the splash screen.
        """
        Clock.schedule_once(self.go_to_initial_screen, 3.0) # Show splash for 3 seconds

    def go_to_initial_screen(self, dt):
        """
        Decides which screen to show after the splash screen.
        """
        if self.state.is_wifi_configured():
            self.root.current = 'home_screen'
        else:
            self.root.current = 'wifi_status_screen'

    def on_physical_trigger(self, *args):
        """
        Handles the 'on_press' event from the TriggerService.
        The behavior depends on the currently active screen.
        """
        current_screen_name = self.root.current
        current_screen = self.root.current_screen

        if current_screen_name == 'wifi_status_screen':
            # Behave as "Configurar Wi-Fi"
            self.root.current = 'wifi_qr_screen'
            
        elif current_screen_name == 'wifi_qr_screen':
            # Force a decode attempt (or confirm after read)
            # For simplicity, we can just log this. A more complex implementation
            # could trigger the decode logic manually.
            print("Trigger pressed on Wi-Fi QR screen.")

        elif current_screen_name == 'home_screen':
            # Behave as "Iniciar Leitura da Carne"
            self.root.current = 'meat_qr_screen'

        elif current_screen_name == 'meat_qr_screen':
            # Force decode or confirm
            print("Trigger pressed on Meat QR screen.")

        elif current_screen_name == 'result_screen':
            # Behave as "Voltar ao Início"
            current_screen.go_to_home()
            
        elif current_screen_name == 'error_screen':
            # Apply a simple retry rule
            current_screen.retry_action()

        # The trigger is ignored on the splash screen.

    def on_stop(self):
        """
        Called when the application is closed.
        Cleans up resources like the trigger service.
        """
        self.trigger_service.stop()

if __name__ == '__main__':
    MarmosApp().run()
