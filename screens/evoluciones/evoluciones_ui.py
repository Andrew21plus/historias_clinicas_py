import flet as ft

def crear_evoluciones_ui(page, on_search, change_page, save_edit):
    page_number_text = ft.Text(f"Página 1")

    # Diálogos
    alert_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Aviso"),
        actions=[ft.TextButton("OK", on_click=lambda e: setattr(alert_dialog, "open", False) or page.update())],
    )

    edit_id = ft.TextField(visible=False)
    edit_paciente = ft.TextField(visible=False)
    edit_motivo = ft.TextField(label="Motivo de consulta", multiline=True)
    edit_enfermedad = ft.TextField(label="Enfermedad actual", multiline=True)

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

    # Componentes principales
    search_field = ft.TextField(
        label="Buscar paciente...",
        on_change=on_search,
        width=page.window_width * 0.9,
        suffix_icon=ft.icons.SEARCH,
    )

    pacientes_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    pagination_controls = ft.Row(
        [
            ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: change_page(-1)),
            page_number_text,
            ft.IconButton(ft.icons.ARROW_FORWARD, on_click=lambda e: change_page(1)),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    return {
        "page_number_text": page_number_text,
        "alert_dialog": alert_dialog,
        "search_field": search_field,
        "pacientes_list": pacientes_list,
        "pagination_controls": pagination_controls,
        "edit_id": edit_id,
        "edit_paciente": edit_paciente,
        "edit_motivo": edit_motivo,
        "edit_enfermedad": edit_enfermedad,
        "edit_dialog": edit_dialog,
    }