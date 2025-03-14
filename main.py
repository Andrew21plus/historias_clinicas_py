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
        """Valida el usuario y navega al menú si es correcto"""
        resultado = validar_usuario(correo, password)

        if resultado["status"]:
            nombre = resultado["nombre"]
            apellido = resultado["apellido"]
            id_usuario = resultado["id_usuario"]
            page.clean()
            page.add(MenuScreen(page, id_usuario, nombre, apellido))  # Pasar datos al menú
        else:
            page.add(ft.Text(resultado["message"], color="red"))

    # Agregar pantalla de login
    LoginScreen(page, go_to_menu)  # <- PASAMOS `page` AQUÍ

ft.app(target=main, view=ft.AppView.FLET_APP)
