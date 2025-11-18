from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

class ResultScreen(Screen):
    """
    Displays the result of an operation, such as a successful
    Wi-Fi configuration or a meat QR code scan.

    The content is dynamically updated based on the 'result_type'
    from the AppState.
    """
    title = StringProperty("")
    message = StringProperty("")

    def on_enter(self, *args):
        """
        Called when the screen is entered. Updates the labels
        based on the application state.
        """
        app = self.manager.app
        result_type = app.state.result_type

        if result_type == 'wifi':
            self.title = "Wi-Fi Configurado"
            self.message = f"Conectado à rede:\n[b]{app.state.wifi_ssid}[/b]"
        elif result_type == 'meat':
            self.title = "Leitura Concluída"
            self.message = f"Código da carne:\n[b]{app.state.last_meat_code}[/b]"
        else:
            self.title = "Resultado"
            self.message = "Operação concluída."

    def go_to_home(self):
        """Navigates back to the home screen."""
        self.manager.current = 'home_screen'

