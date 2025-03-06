import flet as ft

def LoginScreen(on_login):
    return ft.Column(
        [
            ft.Text("Bienvenido", size=24, weight=ft.FontWeight.BOLD),
            ft.TextField(label="Usuario"),
            ft.TextField(label="Contraseña", password=True),
            ft.ElevatedButton("Iniciar sesión", on_click=on_login)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
