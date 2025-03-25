import flet as ft
import time
import uuid
from screens.login_screen import LoginScreen
from screens.menu_screen import MenuScreen
from services.usuarios_service import validar_usuario


def main(page: ft.Page):
    page.title = "Historias Clínicas"
    page.window_width = 1200  # type: ignore
    page.window_height = 800  # type: ignore
    page.window_maximized = True  # type: ignore
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Prefijo único para las claves de almacenamiento
    STORAGE_PREFIX = "clinica.user."

    # Duración de la sesión en segundos (3 días en segundos)
    SESSION_DURATION = 259200

    def check_saved_session():
        """Verifica si hay una sesión válida guardada"""
        session_token = page.client_storage.get(f"{STORAGE_PREFIX}session_token")
        session_data = page.client_storage.get(f"{STORAGE_PREFIX}session_data")
        saved_timestamp = page.client_storage.get(f"{STORAGE_PREFIX}timestamp")

        if all([session_token, session_data, saved_timestamp]):
            if (
                saved_timestamp is not None
                and time.time() - saved_timestamp < SESSION_DURATION
            ):
                # Aquí podrías validar el token con tu backend si fuera necesario
                return session_data
        return None

    def go_to_menu(correo, password, mostrar_mensaje_temporal):
        """Maneja el inicio de sesión"""
        resultado = validar_usuario(correo, password)

        if resultado["status"]:
            # Generamos un token de sesión único
            session_token = str(uuid.uuid4())

            # Datos que queremos persistir
            session_data = {
                "id_usuario": resultado["id_usuario"],
                "nombre": resultado["nombre"],
                "apellido": resultado["apellido"],
                "correo": correo,
            }

            # Guardamos en el almacenamiento del cliente
            page.client_storage.set(f"{STORAGE_PREFIX}session_token", session_token)
            page.client_storage.set(f"{STORAGE_PREFIX}session_data", session_data)
            page.client_storage.set(f"{STORAGE_PREFIX}timestamp", time.time())

            # Mostramos el menú principal
            show_main_menu(session_data)
        else:
            mostrar_mensaje_temporal(resultado["message"], color="red")

    def show_main_menu(user_data):
        """Muestra el menú principal"""
        page.clean()
        page.add(
            MenuScreen(
                page,
                user_data["id_usuario"],
                user_data["nombre"],
                user_data["apellido"],
                logout,
            )
        )

    def logout():
        """Cierra la sesión limpiando el almacenamiento"""
        keys_to_remove = [
            f"{STORAGE_PREFIX}session_token",
            f"{STORAGE_PREFIX}session_data",
            f"{STORAGE_PREFIX}timestamp",
        ]

        for key in keys_to_remove:
            if page.client_storage.contains_key(key):
                page.client_storage.remove(key)

        go_to_login()

    def go_to_login():
        """Muestra la pantalla de login"""
        page.clean()
        page.drawer = None
        page.add(LoginScreen(page, go_to_menu))

    # Al iniciar la aplicación, verificamos si hay sesión guardada
    saved_session = check_saved_session()
    if saved_session:
        show_main_menu(saved_session)
    else:
        go_to_login()


ft.app(target=main, view=ft.AppView.FLET_APP)
