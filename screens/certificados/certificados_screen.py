import flet as ft

def CertificadosScreen(page: ft.Page, id_usuario: int):
    """Pantalla de Certificados Médicos (versión inicial)"""
    return ft.Column(
        [
            ft.Text("Certificados Médicos", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(height=20),
            ft.Text(
                "Aquí se gestionarán los certificados médicos de los pacientes.",
                size=16,
                color=ft.colors.GREY_600,
            ),
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )