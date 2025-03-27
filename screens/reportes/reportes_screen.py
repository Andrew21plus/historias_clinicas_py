import flet as ft

def ReportesScreen(page: ft.Page, id_usuario: int):
    """Pantalla de Reportes Clínicos (versión inicial)"""
    return ft.Column(
        [
            ft.Text("Reportes Clínicos", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(height=20),
            ft.Text(
                "Esta sección generará reportes estadísticos y clínicos.",
                size=16,
                color=ft.colors.GREY_600,
            ),
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )