import flet as ft
from .historia_clinica_crud import (
    obtener_historias_clinicas,
    agregar_historia_clinica,
    actualizar_historia_clinica,
    eliminar_historia_clinica,
    paciente_tiene_historia,
)
from .historia_clinica_ui import crear_historia_clinica_ui
from utils.formulario_historia_clinica import crear_formulario_historia_clinica
from services.paciente_service import get_paciente, get_pacientes_by_id_usuario

def HistoriaClinicaScreen(page: ft.Page, id_usuario: int):
    selected_historia = None  # Variable para almacenar la historia clínica seleccionada
    current_page = 0  # Página actual de la paginación
    historias_per_page = 5  # Número de historias clínicas por página
    search_query = ""  # Variable para almacenar la consulta de búsqueda
    all_historias = []  # Lista para almacenar todas las historias clínicas

    def show_alert(message):
        """Muestra un diálogo de alerta con el mensaje proporcionado."""
        alert_dialog.content = ft.Text(message)
        alert_dialog.open = True
        page.update()

    def confirm_delete(confirmed):
        """Maneja la confirmación de eliminación."""
        nonlocal selected_historia
        confirm_delete_dialog.open = False
        page.update()
        if confirmed:
            remove_historia(selected_historia.id_historia)  # Eliminar la historia clínica
        selected_historia = None  # Reiniciar la historia seleccionada

    def remove_historia(id_historia):
        """Elimina la historia clínica."""
        eliminar_historia_clinica(id_historia)
        refresh_historias()

    def refresh_historias():
        """Actualiza la lista de historias clínicas."""
        nonlocal all_historias
        historias_list.controls.clear()
        all_historias = obtener_historias_clinicas(id_usuario, search_query)

        start_index = current_page * historias_per_page
        end_index = start_index + historias_per_page
        for historia in all_historias[start_index:end_index]:
            paciente = get_paciente(historia.id_paciente)
            if paciente:
                paciente_nombre = paciente.nombre
                paciente_apellido = paciente.apellido
                paciente_sexo = paciente.sexo
                paciente_fecha_nacimiento = paciente.fecha_nacimiento
                paciente_historia_clinica = paciente.num_historia_clinica
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
                                    ft.Text(f"Paciente: {paciente_nombre} {paciente_apellido}", weight=ft.FontWeight.BOLD,
                                            expand=True),
                                    ft.Row([
                                        ft.IconButton(ft.icons.EDIT, on_click=lambda e, h=historia: open_edit_dialog(h)),
                                        ft.IconButton(ft.icons.DELETE,
                                                      on_click=lambda e, h=historia: confirm_delete_dialog_handler(h))
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

    def confirm_delete_dialog_handler(historia):
        """Abre el diálogo de confirmación para eliminar."""
        nonlocal selected_historia
        selected_historia = historia  # Guardar la historia clínica seleccionada
        confirm_delete_dialog.open = True
        page.update()

    def add_historia_clicked(e):
        """Agrega una nueva historia clínica."""
        if all([historia_paciente.value, historia_motivo.value, historia_enfermedad.value]):
            try:
                agregar_historia_clinica(
                    historia_paciente.value, historia_motivo.value, historia_enfermedad.value, id_usuario
                )
                clear_fields()
                refresh_historias()
                paciente_search_field.value = ""
                paciente_results.controls = []
                form_panel.expanded = False
                page.update()
            except ValueError as e:
                show_alert(f"Error al agregar historia clínica: {str(e)}")

    def open_edit_dialog(historia):
        """Abre el diálogo de edición para una historia clínica."""
        nonlocal selected_historia
        selected_historia = historia
        edit_id.value = historia.id_historia
        edit_paciente.value = historia.id_paciente
        edit_motivo.value = historia.motivo_consulta
        edit_enfermedad.value = historia.enfermedad_actual
        edit_dialog.open = True
        page.update()

    def save_edit(e):
        """Guarda los cambios realizados en la historia clínica."""
        actualizar_historia_clinica(
            edit_id.value, edit_motivo.value, edit_enfermedad.value, id_usuario
        )
        edit_dialog.open = False
        refresh_historias()

    def clear_fields():
        """Limpia los campos del formulario."""
        historia_paciente.value = ""
        historia_motivo.value = ""
        historia_enfermedad.value = ""
        page.update()

    def change_page(delta):
        """Cambia la página actual."""
        nonlocal current_page
        current_page += delta
        if current_page < 0:
            current_page = 0
        max_pages = (len(all_historias) + historias_per_page - 1) // historias_per_page
        if current_page >= max_pages:
            current_page = max_pages - 1
        page_number_text.value = f"Página {current_page + 1}"
        refresh_historias()

    def on_search(e):
        """Filtra las historias clínicas según la consulta de búsqueda."""
        nonlocal search_query, current_page
        search_query = search_field.value
        current_page = 0
        page_number_text.value = f"Página {current_page + 1}"
        refresh_historias()

    def on_paciente_search(e):
        """Busca pacientes por nombre o apellido."""
        search_text = paciente_search_field.value.lower()
        if search_text:
            resultados = [
                p for p in get_pacientes_by_id_usuario(id_usuario)
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
        """Selecciona un paciente y completa el campo de ID."""
        historia_paciente.value = paciente.id_paciente
        paciente_search_field.value = f"{paciente.nombre} {paciente.apellido}"
        paciente_results.controls = []

        if paciente_tiene_historia(paciente.id_paciente, all_historias):
            agregar_button.disabled = True
            show_alert("Este paciente ya tiene una historia clínica.")
        else:
            agregar_button.disabled = False
        page.update()

    # Crear el formulario de historia clínica
    formulario = crear_formulario_historia_clinica(
        page,
        add_historia_clicked,
        on_paciente_search,
        select_paciente,
        all_historias
    )

    # Acceder a los componentes del formulario
    form_content = formulario["form_content"]
    historia_paciente = formulario["historia_paciente"]
    historia_motivo = formulario["historia_motivo"]
    historia_enfermedad = formulario["historia_enfermedad"]
    paciente_search_field = formulario["paciente_search_field"]
    paciente_results = formulario["paciente_results"]
    agregar_button = formulario["agregar_button"]

    # Crear el ExpansionPanel para el formulario
    form_panel = ft.ExpansionPanel(
        header=ft.ListTile(
            title=ft.Text("Agregar Nueva Historia Clínica"),
            on_click=lambda e: setattr(form_panel, "expanded", not form_panel.expanded) or page.update(),
        ),
        content=ft.Container(content=form_content),
        expanded=False,
    )

    # Crear el ExpansionPanelList para contener el panel del formulario
    expansion_panel_list = ft.ExpansionPanelList(
        controls=[form_panel],
        on_change=lambda e: page.update(),
    )

    # Crear la interfaz de usuario
    ui = crear_historia_clinica_ui(
        page,
        confirm_delete,
        save_edit,
        on_search,
        change_page
    )

    # Acceder a los componentes de la UI
    page_number_text = ui["page_number_text"]
    confirm_delete_dialog = ui["confirm_delete_dialog"]
    alert_dialog = ui["alert_dialog"]
    search_field = ui["search_field"]
    historias_list = ui["historias_list"]
    edit_id = ui["edit_id"]
    edit_paciente = ui["edit_paciente"]
    edit_motivo = ui["edit_motivo"]
    edit_enfermedad = ui["edit_enfermedad"]
    edit_dialog = ui["edit_dialog"]
    pagination_controls = ui["pagination_controls"]

    refresh_historias()

    return ft.Column(
        [
            ft.Text("Gestión de Historias Clínicas", size=24, weight=ft.FontWeight.BOLD),
            expansion_panel_list,
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
            ft.Row([search_field], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
            ft.Container(
                content=historias_list,
                expand=True,
                padding=10,
                alignment=ft.alignment.top_center
            ),
            pagination_controls,
            edit_dialog,
            confirm_delete_dialog,
            alert_dialog
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )