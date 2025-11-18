from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

class ErrorScreen(Screen):
    """
    A generic screen to display error messages.
    The message is sourced from the AppState.
    """
    
    def on_enter(self, *args):
        """
        When the screen is shown, update its message label from the app state.
        """
        app = self.manager.app
        self.ids.error_message_label.text = app.state.error_message

    def retry_action(self):
        """
        A generic retry action. The logic for what to "retry" would
        depend on the context in which the error occurred. For now,
        it just goes back to the home screen.
        """
        # This could be made more intelligent by storing the previous screen
        # in the AppState.
        self.manager.current = 'home_screen'

    def go_to_home(self):
        """Navigates back to the home screen."""
        self.manager.current = 'home_screen'
