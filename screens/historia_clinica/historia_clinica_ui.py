import flet as ft

def crear_historia_clinica_ui(page, confirm_delete, save_edit, on_search, change_page):
    """Crea la interfaz de usuario para la gestión de historias clínicas."""
    # Texto dinámico para mostrar el número de página
    page_number_text = ft.Text(f"Página 1")

    # Diálogo de confirmación para eliminar
    confirm_delete_dialog = ft.AlertDialog(
        title=ft.Text("Confirmar eliminación"),
        content=ft.Text("¿Estás seguro de que deseas eliminar esta historia clínica?"),
        actions=[
            ft.TextButton("Sí", on_click=lambda e: confirm_delete(True)),
            ft.TextButton("No", on_click=lambda e: confirm_delete(False)),
        ],
    )

    # Diálogo de alerta para mostrar errores
    alert_dialog = ft.AlertDialog(
        title=ft.Text("Advertencia"),
        content=ft.Text(""),
        actions=[
            ft.TextButton(
                "OK",
                on_click=lambda e: setattr(alert_dialog, "open", False) or page.update(),
            )
        ],
    )

    # Campo de búsqueda de historias clínicas
    search_field = ft.TextField(
        label="Buscar por nombre o apellido del paciente",
        on_change=on_search,
        expand=True,
        suffix=ft.IconButton(ft.icons.SEARCH, on_click=on_search)
    )

    # Lista de historias clínicas
    historias_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    # Diálogo de edición
    edit_id = ft.TextField(label="ID Historia Clínica", disabled=True)
    edit_paciente = ft.TextField(label="ID Paciente", disabled=True)
    edit_motivo = ft.TextField(label="Motivo de consulta")
    edit_enfermedad = ft.TextField(label="Enfermedad actual")
    edit_dialog = ft.AlertDialog(
        title=ft.Text("Editar Historia Clínica"),
        content=ft.Column(
            [
                edit_motivo,
                edit_enfermedad,
            ],
            spacing=10
        ),
        actions=[
            ft.TextButton("Guardar", on_click=save_edit),
            ft.TextButton("Cancelar", on_click=lambda e: setattr(edit_dialog, "open", False) or page.update())
        ],
    )

    # Controles de paginación
    pagination_controls = ft.Row(
        [
            ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: change_page(-1)),
            page_number_text,  # Texto dinámico para mostrar el número de página
            ft.IconButton(ft.icons.ARROW_FORWARD, on_click=lambda e: change_page(1)),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    return {
        "page_number_text": page_number_text,
        "confirm_delete_dialog": confirm_delete_dialog,
        "alert_dialog": alert_dialog,
        "search_field": search_field,
        "historias_list": historias_list,
        "edit_id": edit_id,
        "edit_paciente": edit_paciente,
        "edit_motivo": edit_motivo,
        "edit_enfermedad": edit_enfermedad,
        "edit_dialog": edit_dialog,
        "pagination_controls": pagination_controls,
    }