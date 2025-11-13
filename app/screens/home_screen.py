# app/screens/home_screen.py
# Este é um arquivo placeholder para a tela principal da sua aplicação.

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class HomeScreen(Screen):
    """
    Tela Principal (HomeScreen).
    
    Esta tela será exibida após a tela de splash.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout para organizar o conteúdo da tela
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Adiciona um rótulo simples para identificar a tela
        main_label = Label(
            text='Bem-vindo à Aplicação Principal',
            font_size='24sp',
            halign='center',
            valign='middle'
        )
        
        layout.add_widget(main_label)
        self.add_widget(layout)
