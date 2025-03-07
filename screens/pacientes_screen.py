import flet as ft
import base64
from services.paciente_service import get_pacientes, add_paciente, update_paciente, delete_paciente

def PacientesScreen(page):
    selected_photo = None  # Variable para almacenar la imagen seleccionada
    existing_photo = None  # Variable para almacenar la foto existente al editar
    current_page = 0  # Página actual de la paginación
    pacientes_per_page = 5  # Número de pacientes por página
    search_query = ""  # Variable para almacenar la consulta de búsqueda

    def refresh_pacientes():
        pacientes_list.controls.clear()
        pacientes = get_pacientes()
        
        # Filtrar pacientes por nombre o apellido si hay una consulta de búsqueda
        if search_query:
            pacientes = [
                p for p in pacientes
                if search_query.lower() in p.nombre.lower() or search_query.lower() in p.apellido.lower()
            ]
        
        start_index = current_page * pacientes_per_page
        end_index = start_index + pacientes_per_page
        for paciente in pacientes[start_index:end_index]:
            photo_widget = ft.Icon(ft.icons.PERSON, size=100)  # Icono por defecto
            if paciente.foto:
                photo_widget = ft.Image(src_base64=base64.b64encode(paciente.foto).decode(), width=100, height=100)

            paciente_card = ft.Card(
                content=ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=photo_widget,
                                padding=10,
                                alignment=ft.alignment.center
                            ),
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(f"{paciente.nombre} {paciente.apellido}", weight=ft.FontWeight.BOLD, expand=True),
                                            ft.Row([
                                                ft.IconButton(ft.icons.EDIT, on_click=lambda e, p=paciente: open_edit_dialog(p)),
                                                ft.IconButton(ft.icons.DELETE, on_click=lambda e, id_paciente=paciente.id_paciente: remove_paciente(id_paciente))
                                            ])
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    ),
                                    ft.Text(f"ID: {paciente.id_paciente}"),
                                    ft.Text(f"Sexo: {paciente.sexo}"),
                                    ft.Text(f"Fecha Nac: {paciente.fecha_nacimiento}"),
                                    ft.Text(f"Historia Clínica: {paciente.num_historia_clinica}", italic=True),
                                ],
                                spacing=5,
                                expand=True
                            )
                        ],
                        spacing=10
                    ),
                    padding=10
                ),
                width=page.window_width * 0.95
            )
            pacientes_list.controls.append(paciente_card)
        page.update()

    def add_paciente_clicked(e):
        if all([paciente_id.value, paciente_nombre.value, paciente_apellido.value, paciente_sexo.value, paciente_fecha.value, paciente_historia.value]):
            encoded_photo = None
            if selected_photo:
                with open(selected_photo, "rb") as image_file:
                    encoded_photo = image_file.read()

            add_paciente(
                paciente_id.value, paciente_nombre.value, paciente_apellido.value,
                paciente_sexo.value, paciente_fecha.value, paciente_historia.value, encoded_photo
            )
            clear_fields()
            refresh_pacientes()

    def remove_paciente(id_paciente):
        delete_paciente(id_paciente)
        refresh_pacientes()

    def open_edit_dialog(paciente):
        nonlocal selected_photo, existing_photo
        selected_photo = None  # Reiniciar la foto seleccionada al abrir el diálogo
        existing_photo = paciente.foto  # Guardar la foto existente
        edit_id.value = paciente.id_paciente
        edit_nombre.value = paciente.nombre
        edit_apellido.value = paciente.apellido
        edit_sexo.value = paciente.sexo
        edit_fecha.value = paciente.fecha_nacimiento
        edit_historia.value = paciente.num_historia_clinica
        edit_photo_preview.src_base64 = base64.b64encode(paciente.foto).decode() if paciente.foto else None
        edit_photo_preview.visible = paciente.foto is not None
        edit_default_photo_icon.visible = paciente.foto is None
        edit_dialog.open = True
        page.update()

    def save_edit(e):
        encoded_photo = existing_photo  # Usar la foto existente por defecto
        if selected_photo:  # Si se selecciona una nueva foto, actualizar
            with open(selected_photo, "rb") as image_file:
                encoded_photo = image_file.read()

        update_paciente(
            edit_id.value, edit_nombre.value, edit_apellido.value,
            edit_sexo.value, edit_fecha.value, edit_historia.value, encoded_photo
        )
        edit_dialog.open = False
        refresh_pacientes()

    def clear_fields():
        nonlocal selected_photo
        paciente_id.value = ""
        paciente_nombre.value = ""
        paciente_apellido.value = ""
        paciente_sexo.value = ""
        paciente_fecha.value = ""
        paciente_historia.value = ""
        selected_photo = None
        photo_preview.src = None
        photo_preview.visible = False  # Oculta la vista previa de la imagen
        default_photo_icon.visible = True  # Muestra el icono por defecto
        page.update()

    def on_file_picked(e: ft.FilePickerResultEvent):
        nonlocal selected_photo
        if e.files:
            selected_photo = e.files[0].path
            photo_preview.src = selected_photo
            photo_preview.visible = True  # Muestra la vista previa de la imagen
            default_photo_icon.visible = False  # Oculta el icono por defecto
            page.update()

    def on_edit_file_picked(e: ft.FilePickerResultEvent):
        nonlocal selected_photo
        if e.files:
            selected_photo = e.files[0].path
            edit_photo_preview.src = selected_photo
            edit_photo_preview.visible = True  # Muestra la vista previa de la imagen
            edit_default_photo_icon.visible = False  # Oculta el icono por defecto
            page.update()

    def change_page(delta):
        nonlocal current_page
        current_page += delta
        if current_page < 0:
            current_page = 0
        refresh_pacientes()

    def on_search(e):
        nonlocal search_query
        search_query = search_field.value
        refresh_pacientes()

    # Campos del formulario
    paciente_id = ft.TextField(label="ID Paciente", width=200)
    paciente_nombre = ft.TextField(label="Nombre", expand=True)
    paciente_apellido = ft.TextField(label="Apellido", expand=True)
    paciente_sexo = ft.Dropdown(
        label="Sexo",
        options=[ft.dropdown.DropdownOption("M"), ft.dropdown.DropdownOption("F"), ft.dropdown.DropdownOption("O")],
        width=200
    )
    paciente_fecha = ft.TextField(label="Fecha Nacimiento", width=200)
    paciente_historia = ft.TextField(label="Historia Clínica", width=200)
    pacientes_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)  # Habilitar scroll en la lista de pacientes
    
    # Vista previa de la foto y icono por defecto
    default_photo_icon = ft.Icon(ft.icons.PERSON, size=100, visible=True)
    photo_preview = ft.Image(width=100, height=100, visible=False)  # Inicialmente oculta
    file_picker = ft.FilePicker(on_result=on_file_picked)

    # Diálogo de edición
    edit_id = ft.TextField(label="ID Paciente", disabled=True)
    edit_nombre = ft.TextField(label="Nombre")
    edit_apellido = ft.TextField(label="Apellido")
    edit_sexo = ft.Dropdown(
        label="Sexo",
        options=[ft.dropdown.DropdownOption("M"), ft.dropdown.DropdownOption("F"), ft.dropdown.DropdownOption("O")]
    )
    edit_fecha = ft.TextField(label="Fecha Nacimiento")
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
                ft.Row([
                    edit_file_picker,
                    ft.ElevatedButton("Seleccionar Foto", on_click=lambda e: edit_file_picker.pick_files(allow_multiple=False)),
                    ft.Column([edit_default_photo_icon, edit_photo_preview], alignment=ft.MainAxisAlignment.CENTER)
                ])
            ],
            spacing=10
        ),
        actions=[
            ft.TextButton("Guardar", on_click=save_edit),
            ft.TextButton("Cancelar", on_click=lambda e: setattr(edit_dialog, "open", False) or page.update())
        ],
    )

    # Campo de búsqueda
    search_field = ft.TextField(
        label="Buscar por nombre o apellido",
        on_change=on_search,
        expand=True,
        suffix=ft.IconButton(ft.icons.SEARCH, on_click=on_search)
    )

    # ExpansionTile para el formulario
    form_expansion = ft.ExpansionTile(
        title=ft.Text("Agregar nuevo paciente"),
        controls=[
            ft.Column(
                [
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),  # Espacio de 10 unidades
                    ft.Row([paciente_id, paciente_nombre, paciente_apellido], spacing=15),
                    ft.Row([paciente_sexo, paciente_fecha, paciente_historia], spacing=5),
                    ft.Row(
                        [
                            ft.Column([default_photo_icon, photo_preview], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Column([
                                file_picker,
                                ft.ElevatedButton("Seleccionar Foto", on_click=lambda e: file_picker.pick_files(allow_multiple=False))
                            ], alignment=ft.MainAxisAlignment.CENTER)
                        ],
                        spacing=5
                    ),
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),  # Espacio antes del botón Agregar
                    ft.Row([ft.ElevatedButton("Agregar", on_click=add_paciente_clicked)], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT)  # Espacio después del botón Agregar
                ],
                spacing=10
            )
        ]
    )

    refresh_pacientes()

    return ft.Column(
        [
            ft.Text("Gestión de Pacientes", size=24, weight=ft.FontWeight.BOLD),
            form_expansion,  # Formulario colapsable
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),  # Espacio después del formulario
            ft.Row([search_field], alignment=ft.MainAxisAlignment.CENTER),  # Barra de búsqueda
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),  # Espacio después del buscador
            ft.Container(
                content=pacientes_list,
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