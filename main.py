import flet as ft
from screens.login_screen import LoginScreen
from screens.menu_screen import MenuScreen

def main(page: ft.Page):
    page.title = "Historias Clínicas"
    page.window_width = 1200  # Ancho inicial (por si no se maximiza)
    page.window_height = 800  # Alto inicial (por si no se maximiza)
    page.window_maximized = True  # Maximizar la ventana al iniciar
    page.window_resizable = True  # Permitir redimensionar la ventana
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def go_to_menu(e):
        page.clean()
        page.add(MenuScreen(page))

    # Mostrar la pantalla de login al inicio
    page.add(LoginScreen(go_to_menu))

# Asegúrate de que la ventana se abra maximizada
ft.app(target=main, view=ft.AppView.FLET_APP)