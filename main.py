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
            page.add(MenuScreen(page, id_usuario, nombre, apellido, go_to_login))  # Pasar datos al menú
        else:
            page.add(ft.Text(resultado["message"], color="red"))

    def go_to_login():
        """Vuelve a la pantalla de login"""
        page.clean()  # Limpiar la página
        page.drawer = None  # Asegurarse de que no haya un drawer activo
        LoginScreen(page, go_to_menu)  # Mostrar la pantalla de login

    # Iniciar con la pantalla de login
    go_to_login()

ft.app(target=main, view=ft.AppView.FLET_APP)