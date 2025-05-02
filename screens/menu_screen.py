import flet as ft
from screens.pacientes.pacientes_screen import PacientesScreen
from screens.historia_clinica.historia_clinica_screen import HistoriaClinicaScreen
from screens.tamizaje.tamizaje_screen import TamizajeScreen
from screens.evoluciones.evoluciones_screen import EvolucionesScreen
from screens.certificados.certificados_screen import (
    CertificadoScreen,
)  # Nueva importación
from screens.reportes.reportes_screen import ReportesScreen  # Nueva importación


def MenuScreen(page: ft.Page, id_usuario: int, nombre: str, apellido: str, go_to_login):
    """Pantalla del menú principal con opciones de navegación y cierre de sesión"""

    # Función para cambiar el contenido principal
    def change_content(index):
        if index == 0:
            content_area.content = PacientesScreen(page, id_usuario)
        elif index == 1:
            content_area.content = HistoriaClinicaScreen(page, id_usuario)
        elif index == 2:
            content_area.content = TamizajeScreen(page, id_usuario)
        elif index == 3:
            content_area.content = EvolucionesScreen(page, id_usuario, nombre, apellido)
        elif index == 4:  # Nueva opción: Certificados
            content_area.content = CertificadoScreen(page, id_usuario, f"{nombre} {apellido}")
        elif index == 5:  # Nueva opción: Reportes
            content_area.content = ReportesScreen(page, id_usuario)
        elif index == 6:  # Cerrar sesión (ahora en índice 6)
            page.drawer = None  # Eliminar el NavigationDrawer
            page.update()
            go_to_login()  # Volver al login
        page.update()

    # Información del usuario en el menú lateral
    user_info = ft.Container(
        content=ft.Column(
            [
                ft.Text(f"{nombre} {apellido}", weight=ft.FontWeight.BOLD, size=16),
                ft.Text(
                    f"ID Usuario: {id_usuario}",
                    italic=True,
                    size=14,
                    color=ft.colors.BLUE,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
        ),
        padding=10,
    )

    # Menú lateral (NavigationDrawer)
    drawer = ft.NavigationDrawer(
        controls=[
            user_info,
            ft.Divider(),
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
            ft.NavigationDrawerDestination(
                label="Tamizaje",
                icon=ft.icons.MONITOR_HEART,
                selected_icon=ft.icons.MONITOR_HEART_OUTLINED,
            ),
            ft.NavigationDrawerDestination(
                label="Evoluciones",
                icon=ft.icons.TRENDING_UP,
                selected_icon=ft.icons.TRENDING_UP_OUTLINED,
            ),
            ft.NavigationDrawerDestination(  # Nueva opción: Certificados
                label="Certificados",
                icon=ft.icons.ASSIGNMENT,
                selected_icon=ft.icons.ASSIGNMENT_OUTLINED,
            ),
            ft.NavigationDrawerDestination(  # Nueva opción: Reportes
                label="Reportes",
                icon=ft.icons.ANALYTICS,
                selected_icon=ft.icons.ANALYTICS_OUTLINED,
            ),
            ft.Divider(),
            ft.NavigationDrawerDestination(
                label="Cerrar sesión",
                icon=ft.icons.LOGOUT,
                selected_icon=ft.icons.LOGOUT_OUTLINED,
            ),
        ],
        on_change=lambda e: change_content(e.control.selected_index),
    )

    # Área de contenido principal (inicia en Pacientes)
    content_area = ft.Container(
        content=PacientesScreen(page, id_usuario),
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
