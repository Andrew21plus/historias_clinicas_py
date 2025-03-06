import flet as ft
from screens.login_screen import LoginScreen
from screens.pacientes_screen import PacientesScreen

def main(page: ft.Page):
    page.title = "Gestión de Pacientes"
    page.window_width = 800  # Ajustado para mejor visualización
    page.window_height = 600
    page.window_resizable = True
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def go_to_pacientes(e):
        page.clean()
        page.add(PacientesScreen(page))

    page.add(LoginScreen(go_to_pacientes))

ft.app(target=main)

