import flet as ft
from screens.login_screen import LoginScreen
from screens.tasks_screen import TasksScreen

def main(page: ft.Page):
    page.title = "To-Do App"
    page.window_width = 600  # Tamaño mediano
    page.window_height = 500
    page.window_resizable = True  # Permitir que se ajuste si es necesario
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def go_to_tasks(e):
        page.clean()
        page.add(TasksScreen(page))

    page.add(LoginScreen(go_to_tasks))

ft.app(target=main)
