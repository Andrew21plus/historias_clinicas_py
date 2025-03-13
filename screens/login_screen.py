import flet as ft
from services.usuarios_service import nuevo_usuario


def LoginScreen(on_login):
    # nombre_field = ft.TextField(label="Nombre")
    # apellido_field = ft.TextField(label="Apellido")
    correo_field = ft.TextField(label="Correo")
    password_field = ft.TextField(label="Contraseña", password=True)

    # rol_field = ft.Dropdown(
    #     label="Rol",
    #     hint_text="¿Qué rol tendrá?",
    #     options=[
    #         ft.dropdown.Option("Administrador"),
    #         ft.dropdown.Option("Doctor"),
    #         ft.dropdown.Option("Enfermero"),
    #     ],
    # )

    def handle_login(e):
        usuario = correo_field.value
        password = password_field.value
        on_login(usuario, password)

    # def handle_register(e):
    #     nuevo_usuario(
    #         nombre_field.value,
    #         apellido_field.value,
    #         correo_field.value,
    #         password_field.value,
    #         rol_field.value,
    #     )

    return ft.Column(
        [
            ft.Text("Bienvenido", size=24, weight=ft.FontWeight.BOLD),
            # nombre_field,
            # apellido_field,
            correo_field,
            password_field,
            # rol_field,
            # ft.ElevatedButton("Crear Usuario", on_click=handle_register),
            ft.ElevatedButton("Iniciar sesión", on_click=handle_login),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
