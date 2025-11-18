# app/screens/home_screen.py
# -*- coding: utf-8 -*-

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex

# --- Tema de Cores ---
# Cores inspiradas em uma paleta de design moderno
COLOR_BACKGROUND = get_color_from_hex('#1A1A1A') # Quase preto
COLOR_PRIMARY = get_color_from_hex('#FFD700')    # Dourado/Amarelo para destaque
COLOR_SECONDARY = get_color_from_hex('#4CAF50')  # Verde para ações positivas
COLOR_TEXT = get_color_from_hex('#FFFFFF')       # Branco para texto

class HomeScreen(Screen):
    """
    Tela Principal (HomeScreen).

    Esta tela é o hub central da aplicação, exibindo informações
    e fornecendo acesso a outras funcionalidades.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Define a cor de fundo da tela
        with self.canvas.before:
            Color(*COLOR_BACKGROUND)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # --- Layout Principal ---
        main_layout = BoxLayout(orientation='vertical')

        # --- 1. Cabeçalho (Header) ---
        header_layout = BoxLayout(
            size_hint_y=None,
            height=80,
            padding=20,
            spacing=20
        )
        with header_layout.canvas.before:
            Color(*COLOR_PRIMARY)
            self.header_rect = Rectangle(size=header_layout.size, pos=header_layout.pos)
            header_layout.bind(size=self._update_header_rect, pos=self._update_header_rect)

        header_label = Label(
            text='Marmos UI',
            font_name='assets/fonts/Roboto-Bold.ttf', # Fonte personalizada
            font_size='32sp',
            color=COLOR_BACKGROUND
        )
        header_layout.add_widget(header_label)

        # --- 2. Área de Conteúdo Principal ---
        content_layout = BoxLayout(
            padding=20
        )
        content_label = Label(
            text='Câmera e Informações do Produto',
            font_name='assets/fonts/Roboto-Regular.ttf',
            font_size='24sp',
            color=COLOR_TEXT
        )
        content_layout.add_widget(content_label)

        # --- 3. Rodapé (Footer) com Botões de Navegação ---
        footer_layout = BoxLayout(
            size_hint_y=None,
            height=100,
            padding=10,
            spacing=20
        )
        
        # Botões de exemplo
        add_button = Button(
            text='Adicionar Produto',
            font_name='assets/fonts/Roboto-Bold.ttf',
            font_size='20sp',
            background_color=COLOR_SECONDARY,
            color=COLOR_TEXT
        )
        inventory_button = Button(
            text='Ver Inventário',
            font_name='assets/fonts/Roboto-Bold.ttf',
            font_size='20sp',
            background_color=COLOR_PRIMARY,
            color=COLOR_BACKGROUND
        )
        
        footer_layout.add_widget(add_button)
        footer_layout.add_widget(inventory_button)

        # --- Montagem do Layout ---
        main_layout.add_widget(header_layout)
        main_layout.add_widget(content_layout)
        main_layout.add_widget(footer_layout)
        
        self.add_widget(main_layout)

    def _update_rect(self, instance, value):
        """ Atualiza o tamanho e a posição do retângulo de fundo. """
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_header_rect(self, instance, value):
        """ Atualiza o tamanho e a posição do retângulo do cabeçalho. """
        self.header_rect.pos = instance.pos
        self.header_rect.size = instance.size
