# app/main.py
# -*- coding: utf-8 -*-

import os
from kivy.config import Config

# --- Configuração do Kivy ---
# Estas configurações devem ser definidas ANTES de importar outros módulos do Kivy.
# Define o modo de tela cheia. 'auto' usa o modo nativo do sistema operacional.
# Essencial para o Raspberry Pi bootar diretamente no app.
Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'window_state', 'maximized')
Config.write()

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window

# Importa a tela principal da aplicação
from screens.home_screen import HomeScreen

class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Define o layout que permitirá o posicionamento flexível da imagem
        layout = FloatLayout()
        
        # Define a cor de fundo da janela como preto
        Window.clearcolor = (0, 0, 0, 1) # RGBA para preto

        # Carrega a imagem do logo
        # O caminho é relativo ao diretório onde o script é executado
        logo_path = os.path.join('assets', 'images', 'logo_marmos.png')
        
        self.logo = Image(
            source=logo_path,
            size_hint=(None, None),
            size=(400, 400), # Tamanho da imagem (ajuste conforme necessário)
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            opacity=0  # Começa totalmente transparente para o fade-in
        )
        
        layout.add_widget(self.logo)
        self.add_widget(layout)

    def on_enter(self, *args):
        # Animação de fade-in: opacidade de 0 para 1 em 1.5 segundos
        fade_in_animation = Animation(opacity=1, duration=3)
        fade_in_animation.start(self.logo)
        
        # Agenda a transição para a próxima tela após 3 segundos
        Clock.schedule_once(self.start_fade_out, 10)

    def start_fade_out(self, *args):
        # Animação de fade-out: opacidade de 1 para 0 em 1.5 segundos
        fade_out_animation = Animation(opacity=0, duration=3)
        
        # Ao completar a animação de fade-out, chama o método para trocar de tela
        fade_out_animation.bind(on_complete=self.change_to_home_screen)
        
        fade_out_animation.start(self.logo)

    def change_to_home_screen(self, *args):
        if self.manager:
            self.manager.current = 'home'


class MarmosUIApp(App):
    """
    Classe principal da aplicação Kivy.
    """
    def build(self):
        """
        Constrói a interface da aplicação.
        """
        # Cria o gerenciador de telas com uma transição de fade
        sm = ScreenManager(transition=FadeTransition(duration=1))
        
        # Adiciona as telas ao gerenciador
        # A primeira tela adicionada ('splash') será a tela inicial
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(HomeScreen(name='home'))
        
        return sm

# --- Ponto de Entrada da Aplicação ---
if __name__ == '__main__':
    MarmosUIApp().run()