# paciente_ui.py
import flet as ft

def crear_paciente_ui(page, confirm_delete, save_edit, on_search, change_page, on_edit_file_picked, guardar_historia_clinica):
    """Crea la interfaz de usuario para la gestión de pacientes."""
    # Texto dinámico para mostrar el número de página
    page_number_text = ft.Text(f"Página 1")

    # Diálogo de confirmación para eliminar
    confirm_delete_dialog = ft.AlertDialog(
        title=ft.Text("Confirmar eliminación"),
        content=ft.Text("¿Estás seguro de que deseas eliminar este paciente?"),
        actions=[
            ft.TextButton("Sí", on_click=lambda e: confirm_delete(True)),
            ft.TextButton("No", on_click=lambda e: confirm_delete(False)),
        ],
    )

    # Componentes para el diálogo de historia clínica
    historia_paciente_id = ft.TextField(label="ID Paciente", read_only=True)
    historia_motivo = ft.TextField(label="Motivo de consulta", multiline=True)
    historia_enfermedad = ft.TextField(label="Enfermedad actual", multiline=True)
    
    historia_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Agregar Historia Clínica"),
        content=ft.Column(
            [
                historia_paciente_id,
                historia_motivo,
                historia_enfermedad,
            ],
            tight=True,
        ),
        actions=[
            ft.TextButton("Guardar", on_click=guardar_historia_clinica),
            ft.TextButton("Cancelar", on_click=lambda e: setattr(historia_dialog, "open", False) or page.update()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Diálogo de edición
    edit_id = ft.TextField(label="ID Paciente", disabled=True)
    edit_nombre = ft.TextField(label="Nombre")
    edit_apellido = ft.TextField(label="Apellido")
    edit_sexo = ft.Dropdown(
        label="Sexo",
        options=[
            ft.dropdown.DropdownOption("M"),
            ft.dropdown.DropdownOption("F"),
            ft.dropdown.DropdownOption("O"),
        ],
    )
    edit_fecha = ft.TextField(label="Fecha Nacimiento (dd-mm-yyyy)", hint_text="Ej: 15-05-1990")
    edit_historia = ft.TextField(label="Historia Clínica")
    edit_default_photo_icon = ft.Icon(ft.icons.PERSON, size=100, visible=True)
    edit_photo_preview = ft.Image(width=100, height=100, visible=False)
    edit_file_picker = ft.FilePicker(on_result=on_edit_file_picked)
    edit_dialog = ft.AlertDialog(
        title=ft.Text("Editar Paciente"),
        content=ft.Column(
            [
                edit_nombre,
                edit_apellido,
                edit_sexo,
                edit_fecha,
                edit_historia,
                ft.Row(
                    [
                        edit_file_picker,
                        ft.ElevatedButton(
                            "Seleccionar Foto",
                            on_click=lambda e: edit_file_picker.pick_files(allow_multiple=False),
                        ),
                        ft.Column(
                            [edit_default_photo_icon, edit_photo_preview],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ]
                ),
            ],
            spacing=10,
        ),
        actions=[
            ft.TextButton("Guardar", on_click=save_edit),
            ft.TextButton("Cancelar", on_click=lambda e: setattr(edit_dialog, "open", False) or page.update()),
        ],
    )

    # Diálogo de alerta para mostrar errores
    alert_dialog = ft.AlertDialog(
        title=ft.Text("Error"),
        content=ft.Text(""),
        actions=[
            ft.TextButton(
                "OK",
                on_click=lambda e: setattr(alert_dialog, "open", False) or page.update(),
            )
        ],
    )

    # Diálogo de éxito para mostrar mensajes positivos
    success_dialog = ft.AlertDialog(
        title=ft.Text("Éxito"),
        content=ft.Text(""),
        actions=[
            ft.TextButton(
                "OK",
                on_click=lambda e: setattr(success_dialog, "open", False) or page.update(),
            )
        ],
    )

    # Campo de búsqueda
    search_field = ft.TextField(
        label="Buscar por nombre o apellido",
        on_change=on_search,
        expand=True,
        suffix=ft.IconButton(ft.icons.SEARCH, on_click=on_search),
    )

    # Lista de pacientes
    pacientes_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    # Controles de paginación
    pagination_controls = ft.Row(
        [
            ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: change_page(-1)),
            page_number_text,
            ft.IconButton(ft.icons.ARROW_FORWARD, on_click=lambda e: change_page(1)),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    return {
        "page_number_text": page_number_text,
        "confirm_delete_dialog": confirm_delete_dialog,
        "alert_dialog": alert_dialog,
        "success_dialog": success_dialog,
        "search_field": search_field,
        "pacientes_list": pacientes_list,
        "edit_id": edit_id,
        "edit_nombre": edit_nombre,
        "edit_apellido": edit_apellido,
        "edit_sexo": edit_sexo,
        "edit_fecha": edit_fecha,
        "edit_historia": edit_historia,
        "edit_default_photo_icon": edit_default_photo_icon,
        "edit_photo_preview": edit_photo_preview,
        "edit_file_picker": edit_file_picker,
        "edit_dialog": edit_dialog,
        "historia_dialog": historia_dialog,
        "historia_paciente_id": historia_paciente_id,
        "historia_motivo": historia_motivo,
        "historia_enfermedad": historia_enfermedad,
        "pagination_controls": pagination_controls,
    }