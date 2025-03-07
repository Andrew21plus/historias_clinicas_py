import flet as ft
from services.historia_clinica_service import (
    get_historias_clinicas, 
    add_historia_clinica, 
    update_historia_clinica, 
    delete_historia_clinica,
    paciente_tiene_historia  # Importa la nueva función
)
from services.paciente_service import get_paciente, get_pacientes  # Importa la función para obtener todos los pacientes

def HistoriaClinicaScreen(page: ft.Page):
    selected_historia = None  # Variable para almacenar la historia clínica seleccionada
    current_page = 0  # Página actual de la paginación
    historias_per_page = 5  # Número de historias clínicas por página
    search_query = ""  # Variable para almacenar la consulta de búsqueda
    pacientes = get_pacientes()  # Obtener todos los pacientes

    def refresh_historias():
        historias_list.controls.clear()
        historias = get_historias_clinicas()
        
        # Filtrar historias clínicas por motivo de consulta o enfermedad actual
        if search_query:
            historias = [
                h for h in historias
                if search_query.lower() in h.motivo_consulta.lower() or search_query.lower() in h.enfermedad_actual.lower()
            ]
        
        start_index = current_page * historias_per_page
        end_index = start_index + historias_per_page
        for historia in historias[start_index:end_index]:
            # Obtener los datos del paciente asociado a la historia clínica
            paciente = get_paciente(historia.id_paciente)
            if paciente:
                paciente_nombre = paciente.nombre  # Nombre del paciente
                paciente_apellido = paciente.apellido  # Apellido del paciente
                paciente_sexo = paciente.sexo  # Sexo del paciente
                paciente_fecha_nacimiento = paciente.fecha_nacimiento  # Fecha de nacimiento del paciente
                paciente_historia_clinica = paciente.num_historia_clinica  # Número de historia clínica del paciente
            else:
                paciente_nombre = "Desconocido"
                paciente_apellido = ""
                paciente_sexo = ""
                paciente_fecha_nacimiento = ""
                paciente_historia_clinica = ""

            historia_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(f"Paciente: {paciente_nombre} {paciente_apellido}", weight=ft.FontWeight.BOLD, expand=True),
                                    ft.Row([
                                        ft.IconButton(ft.icons.EDIT, on_click=lambda e, h=historia: open_edit_dialog(h)),
                                        ft.IconButton(ft.icons.DELETE, on_click=lambda e, id_historia=historia.id_historia: remove_historia(id_historia))
                                    ])
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Text(f"Sexo: {paciente_sexo}"),
                            ft.Text(f"Fecha de nacimiento: {paciente_fecha_nacimiento}"),
                            ft.Text(f"Historia clínica: {paciente_historia_clinica}"),
                            ft.Text(f"Motivo de consulta: {historia.motivo_consulta}"),
                            ft.Text(f"Enfermedad actual: {historia.enfermedad_actual}"),
                        ],
                        spacing=5,
                        expand=True
                    ),
                    padding=10
                ),
                width=page.window_width * 0.95
            )
            historias_list.controls.append(historia_card)
        page.update()

    def add_historia_clicked(e):
        if all([historia_paciente.value, historia_motivo.value, historia_enfermedad.value]):
            try:
                add_historia_clinica(
                    historia_paciente.value, historia_motivo.value, historia_enfermedad.value
                )
                clear_fields()
                refresh_historias()
                # Limpiar el campo de búsqueda y restablecer el estado del formulario
                paciente_search_field.value = ""  # Limpiar el campo de búsqueda
                paciente_results.controls = []  # Limpiar la lista de resultados
                page.update()
            except ValueError as e:
                page.snack_bar = ft.SnackBar(content=ft.Text(str(e)))
                page.snack_bar.open = True
                page.update()

    def remove_historia(id_historia):
        delete_historia_clinica(id_historia)
        refresh_historias()

    def open_edit_dialog(historia):
        nonlocal selected_historia
        selected_historia = historia  # Guardar la historia clínica seleccionada
        edit_id.value = historia.id_historia
        edit_paciente.value = historia.id_paciente
        edit_motivo.value = historia.motivo_consulta
        edit_enfermedad.value = historia.enfermedad_actual
        edit_dialog.open = True
        page.update()

    def save_edit(e):
        update_historia_clinica(
            edit_id.value, edit_motivo.value, edit_enfermedad.value
        )
        edit_dialog.open = False
        refresh_historias()

    def clear_fields():
        historia_paciente.value = ""
        historia_motivo.value = ""
        historia_enfermedad.value = ""
        page.update()

    def change_page(delta):
        nonlocal current_page
        current_page += delta
        if current_page < 0:
            current_page = 0
        refresh_historias()

    def on_search(e):
        nonlocal search_query
        search_query = search_field.value
        refresh_historias()

    def on_paciente_search(e):
        """ Busca pacientes por nombre o apellido y muestra los resultados """
        search_text = paciente_search_field.value.lower()
        if search_text:
            resultados = [
                p for p in pacientes
                if search_text in p.nombre.lower() or search_text in p.apellido.lower()
            ]
            paciente_results.controls = [
                ft.ListTile(
                    title=ft.Text(f"{p.nombre} {p.apellido}"),
                    subtitle=ft.Text(f"ID: {p.id_paciente}"),
                    on_click=lambda e, p=p: select_paciente(p)
                ) for p in resultados
            ]
        else:
            paciente_results.controls = []
        page.update()

    def select_paciente(paciente):
        """ Selecciona un paciente y completa el campo de ID """
        historia_paciente.value = paciente.id_paciente
        paciente_search_field.value = f"{paciente.nombre} {paciente.apellido}"
        paciente_results.controls = []  # Limpiar la lista de resultados

        # Verificar si el paciente ya tiene una historia clínica
        if paciente_tiene_historia(paciente.id_paciente):
            agregar_button.disabled = True
            page.snack_bar = ft.SnackBar(content=ft.Text("Este paciente ya tiene una historia clínica."))
            page.snack_bar.open = True
        else:
            agregar_button.disabled = False
        page.update()

    # Campos del formulario
    historia_paciente = ft.TextField(label="ID Paciente", width=200, read_only=True)  # Campo de solo lectura
    historia_motivo = ft.TextField(label="Motivo de consulta", expand=True)
    historia_enfermedad = ft.TextField(label="Enfermedad actual", expand=True)
    historias_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)  # Habilitar scroll en la lista de historias clínicas

    # Campo de búsqueda de pacientes
    paciente_search_field = ft.TextField(
        label="Buscar paciente por nombre o apellido",
        on_change=on_paciente_search,
        expand=True
    )
    paciente_results = ft.Column()  # Lista de resultados de búsqueda de pacientes

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

    # Campo de búsqueda de historias clínicas
    search_field = ft.TextField(
        label="Buscar por motivo de consulta o enfermedad",
        on_change=on_search,
        expand=True,
        suffix=ft.IconButton(ft.icons.SEARCH, on_click=on_search)
    )

    # Botón de agregar
    agregar_button = ft.ElevatedButton("Agregar", on_click=add_historia_clicked)

    # ExpansionTile para el formulario
    form_expansion = ft.ExpansionTile(
        title=ft.Text("Agregar nueva historia clínica"),
        controls=[
            ft.Column(
                [
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),  # Espacio de 10 unidades
                    paciente_search_field,  # Campo de búsqueda de pacientes
                    paciente_results,  # Lista de resultados de búsqueda de pacientes
                    ft.Row([historia_paciente, historia_motivo, historia_enfermedad], spacing=15),
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),  # Espacio antes del botón Agregar
                    ft.Row([agregar_button], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT)  # Espacio después del botón Agregar
                ],
                spacing=10
            )
        ]
    )

    refresh_historias()

    return ft.Column(
        [
            ft.Text("Gestión de Historias Clínicas", size=24, weight=ft.FontWeight.BOLD),
            form_expansion,  # Formulario colapsable
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),  # Espacio después del formulario
            ft.Row([search_field], alignment=ft.MainAxisAlignment.CENTER),  # Barra de búsqueda
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),  # Espacio después del buscador
            ft.Container(
                content=historias_list,
                expand=True,
                padding=10,
                alignment=ft.alignment.top_center
            ),
            ft.Row([
                ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: change_page(-1)),
                ft.Text(f"Página {current_page + 1}"),
                ft.IconButton(ft.icons.ARROW_FORWARD, on_click=lambda e: change_page(1)),
            ], alignment=ft.MainAxisAlignment.CENTER),
            edit_dialog
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO  # Habilitar scroll en la columna principal
    )