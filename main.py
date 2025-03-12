import flet as ft
from screens.login_screen import LoginScreen
from screens.menu_screen import MenuScreen
from services.usuarios_service import validar_usuario  # Importamos la validación


def main(page: ft.Page):
    page.title = "Historias Clínicas"
    page.window_width = 1200  # type: ignore
    page.window_height = 800  # type: ignore
    page.window_maximized = True  # type: ignore
    page.window_resizable = True  # type: ignore
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def go_to_menu(correo, password):
        if validar_usuario(correo, password)["status"]:
            page.clean()
            page.add(MenuScreen(page))
        else:
            page.add(ft.Text("Usuario o contraseña incorrectos", color="red"))

    page.add(LoginScreen(go_to_menu))


ft.app(target=main, view=ft.AppView.FLET_APP)
