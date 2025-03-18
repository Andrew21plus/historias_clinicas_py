import flet as ft

def paciente_tiene_historia(paciente_id, all_historias):
    """Verifica si un paciente ya tiene una historia clínica."""
    for historia in all_historias:
        if historia.id_paciente == paciente_id:  # Acceder directamente a id_paciente
            return True
    return False

def crear_formulario_historia_clinica(page, add_historia_clicked, on_paciente_search, select_paciente, all_historias):
    # Campos del formulario
    historia_paciente = ft.TextField(label="ID Paciente", width=200, read_only=True)
    historia_motivo = ft.TextField(label="Motivo de consulta", expand=True)
    historia_enfermedad = ft.TextField(label="Enfermedad actual", expand=True)

    # Campo de búsqueda de pacientes
    paciente_search_field = ft.TextField(
        label="Buscar paciente por nombre o apellido",
        on_change=on_paciente_search,
        expand=True
    )
    paciente_results = ft.Column()

    # Botón de agregar
    agregar_button = ft.ElevatedButton("Agregar", on_click=add_historia_clicked)

    # Crear el contenido del formulario (sin ExpansionTile)
    form_content = ft.Column(
        [
            ft.Divider(height=10, color=ft.colors.TRANSPARENT),
            paciente_search_field,
            paciente_results,
            ft.Row([historia_paciente, historia_motivo, historia_enfermedad], spacing=15),
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
            ft.Row([agregar_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=20, color=ft.colors.TRANSPARENT)
        ],
        spacing=10
    )

    return {
        "form_content": form_content,
        "historia_paciente": historia_paciente,
        "historia_motivo": historia_motivo,
        "historia_enfermedad": historia_enfermedad,
        "paciente_search_field": paciente_search_field,
        "paciente_results": paciente_results,
        "agregar_button": agregar_button,
        "paciente_tiene_historia": paciente_tiene_historia  # Devolver la función de validación
    }