import flet as ft
from screens.pacientes_screen import PacientesScreen
from screens.historia_clinica_screen import HistoriaClinicaScreen

def MenuScreen(page: ft.Page):
    # Función para cambiar el contenido principal
    def change_content(index):
        if index == 0:
            content_area.content = PacientesScreen(page)
        elif index == 1:
            content_area.content = HistoriaClinicaScreen(page)
        page.update()

    # Menú lateral (NavigationDrawer)
    drawer = ft.NavigationDrawer(
        controls=[
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
        content=PacientesScreen(page),  # Contenido inicial (Pacientes)
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