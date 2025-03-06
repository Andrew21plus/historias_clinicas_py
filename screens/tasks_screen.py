import flet as ft
from services.task_service import get_tasks, create_task, toggle_task_status, remove_task, edit_task

def TasksScreen(page):
    def refresh_tasks():
        tasks_list.controls.clear()
        tasks = get_tasks()
        for task in tasks:
            task_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Checkbox(
                                        label=task.title,
                                        value=task.completed,
                                        on_change=lambda e, task_id=task.id: toggle_task_status(task_id, e.control.value)
                                    ),
                                    ft.IconButton(ft.icons.EDIT, on_click=lambda e, t=task: open_edit_dialog(t)),
                                    ft.IconButton(ft.icons.DELETE, on_click=lambda e, task_id=task.id: delete_task(task_id))
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Text(task.description, size=12, italic=True),
                        ]
                    ),
                    padding=10
                ),
                width=page.window_width * 0.9  # Responsivo, 90% del ancho de la ventana
            )
            tasks_list.controls.append(task_card)
        page.update()

    def add_task_clicked(e):
        if task_title.value and task_description.value:
            create_task(task_title.value, task_description.value)
            task_title.value = ""
            task_description.value = ""
            refresh_tasks()

    def delete_task(task_id):
        remove_task(task_id)
        refresh_tasks()

    def open_edit_dialog(task):
        edit_title.value = task.title
        edit_description.value = task.description
        edit_dialog.open = True
        edit_dialog.task_id = task.id
        page.update()

    def save_edit(e):
        edit_task(edit_dialog.task_id, edit_title.value, edit_description.value)
        edit_dialog.open = False
        refresh_tasks()

    task_title = ft.TextField(hint_text="Título de la tarea", expand=True)
    task_description = ft.TextField(hint_text="Descripción de la tarea", expand=True)
    tasks_list = ft.Column(scroll=ft.ScrollMode.AUTO)  # Permitir scroll si hay muchas tareas

    edit_title = ft.TextField(label="Editar título")
    edit_description = ft.TextField(label="Editar descripción")
    edit_dialog = ft.AlertDialog(
        title=ft.Text("Editar tarea"),
        content=ft.Column([edit_title, edit_description]),
        actions=[ft.TextButton("Guardar", on_click=save_edit), ft.TextButton("Cancelar", on_click=lambda e: setattr(edit_dialog, "open", False) or page.update())],
    )

    refresh_tasks()

    return ft.Column(
        [
            ft.Text("Mis Tareas", size=24, weight=ft.FontWeight.BOLD),
            ft.Row([task_title, task_description, ft.ElevatedButton("Agregar", on_click=add_task_clicked)], spacing=10),
            tasks_list,
            edit_dialog
        ],
        expand=True,  # Que la pantalla ocupe todo el espacio disponible
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
