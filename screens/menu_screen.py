import flet as ft
from screens.pacientes_screen import PacientesScreen
from screens.historia_clinica_screen import HistoriaClinicaScreen

def MenuScreen(page: ft.Page, id_usuario: int, nombre: str, apellido: str, rol: str):
    
    
    # Función para cambiar el contenido principal
    def change_content(index):
        if index == 0:
            content_area.content = PacientesScreen(page, id_usuario)  # Pasar id_usuario
        elif index == 1:
            content_area.content = HistoriaClinicaScreen(page, id_usuario)
        page.update()

    # Información del usuario en el menú lateral
    user_info = ft.Container(
        content=ft.Column(
            [
                ft.Text(f"{nombre} {apellido}", weight=ft.FontWeight.BOLD, size=16),
                ft.Text(f"Rol: {rol}", italic=True, size=14, color=ft.colors.GREY),
                ft.Text(f"ID Usuario: {id_usuario}", italic=True, size=14, color=ft.colors.BLUE),  # Mostrar el ID del usuario
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
        ),
        padding=10,
    )

    # Menú lateral (NavigationDrawer)
    drawer = ft.NavigationDrawer(
        controls=[
            user_info,  # Mostrar la información del usuario arriba
            ft.Divider(),  # Separador visual
            ft.NavigationDrawerDestination(
                label="Pacientes",
                icon=ft.icons.PEOPLE,
                selected_icon=ft.icons.PEOPLE_OUTLINE,
            ),
            ft.NavigationDrawerDestination(
                label="Historia Clínica",
                icon=ft.icons.HEALTH_AND_SAFETY,
                selected_icon=ft.icons.HEALTH_AND_SAFETY_OUTLINED,
            ),
        ],
        on_change=lambda e: change_content(e.control.selected_index),
    )

    # Área de contenido principal
    content_area = ft.Container(
        content=PacientesScreen(page, id_usuario),  # Contenido inicial (Pacientes)
        expand=True,
        padding=20,
    )

    # Botón para abrir/cerrar el menú
    def toggle_drawer(e):
        drawer.open = not drawer.open
        page.update()

    menu_button = ft.IconButton(ft.icons.MENU, on_click=toggle_drawer)

    # Añadir el drawer a la página
    page.drawer = drawer

    # Layout principal
    return ft.Column(
        [
            ft.Row([menu_button], alignment=ft.MainAxisAlignment.START),
            content_area,
        ],
        expand=True,
    )