# screens/pacientes_screen.py
import flet as ft
import base64
from services.paciente_service import (
    get_pacientes, 
    add_paciente, 
    update_paciente, 
    delete_paciente,
    cedula_existe,
    historia_clinica_existe
)
from utils.formulario_paciente import crear_formulario_paciente, validar_cedula_ecuatoriana, validar_fecha

def PacientesScreen(page):
    selected_photo = None  # Variable para almacenar la imagen seleccionada
    existing_photo = None  # Variable para almacenar la foto existente al editar
    current_page = 0  # Página actual de la paginación
    pacientes_per_page = 5  # Número de pacientes por página
    search_query = ""  # Variable para almacenar la consulta de búsqueda

    def show_alert(message):
        alert_dialog.content = ft.Text(message)
        alert_dialog.open = True
        page.update()

    def validar_campos_requeridos(campos):
        campos_faltantes = [campo for campo in campos if not campo.value]
        if campos_faltantes:
            show_alert(f"Por favor, complete los siguientes campos: {', '.join([campo.label for campo in campos_faltantes])}")
            return False
        return True

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
        campos_requeridos = [paciente_id, paciente_nombre, paciente_apellido, paciente_sexo, paciente_fecha, paciente_historia]
        if not validar_campos_requeridos(campos_requeridos):
            return

        # Validar el formato de la fecha
        if not validar_fecha(paciente_fecha.value):
            show_alert("Formato de fecha inválido. Use dd-mm-yyyy.")
            return

        if not validar_cedula_ecuatoriana(paciente_id.value):
            show_alert("Cédula inválida. Por favor, ingrese una cédula ecuatoriana válida.")
            return

        if cedula_existe(paciente_id.value):
            show_alert("Error: La cédula ya está registrada.")
            return

        if historia_clinica_existe(paciente_historia.value):
            show_alert("Error: El número de historia clínica ya está registrado.")
            return

        if all([paciente_id.value, paciente_nombre.value, paciente_apellido.value, paciente_sexo.value, paciente_fecha.value, paciente_historia.value]):
            encoded_photo = None
            if selected_photo:
                with open(selected_photo, "rb") as image_file:
                    encoded_photo = image_file.read()

            try:
                # Convertir nombre y apellido a mayúsculas
                nombre_mayusculas = paciente_nombre.value.upper()
                apellido_mayusculas = paciente_apellido.value.upper()

                add_paciente(
                    paciente_id.value, nombre_mayusculas, apellido_mayusculas,
                    paciente_sexo.value, paciente_fecha.value, paciente_historia.value, encoded_photo
                )
                clear_fields()  # Limpiar los campos después de agregar
                form_panel.expanded = False  # Colapsar el panel del formulario
                refresh_pacientes()
                page.update()  # Forzar la actualización de la interfaz
            except Exception as ex:
                show_alert(f"Error al agregar paciente: {str(ex)}")

    def remove_paciente(id_paciente):
        try:
            delete_paciente(id_paciente)
            refresh_pacientes()
        except Exception as ex:
            show_alert(f"Error al eliminar paciente: {str(ex)}")

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
        campos_requeridos = [edit_id, edit_nombre, edit_apellido, edit_sexo, edit_fecha, edit_historia]
        if not validar_campos_requeridos(campos_requeridos):
            return

        # Validar el formato de la fecha
        if not validar_fecha(edit_fecha.value):
            show_alert("Formato de fecha inválido. Use dd-mm-yyyy.")
            return

        if not validar_cedula_ecuatoriana(edit_id.value):
            show_alert("Cédula inválida. Por favor, ingrese una cédula ecuatoriana válida.")
            return

        if cedula_existe(edit_id.value, exclude_id=edit_id.value):
            show_alert("Error: La cédula ya está registrada.")
            return

        if historia_clinica_existe(edit_historia.value, exclude_id=edit_id.value):
            show_alert("Error: El número de historia clínica ya está registrado.")
            return

        encoded_photo = existing_photo  # Usar la foto existente por defecto
        if selected_photo:  # Si se selecciona una nueva foto, actualizar
            with open(selected_photo, "rb") as image_file:
                encoded_photo = image_file.read()

        try:
            # Convertir nombre y apellido a mayúsculas
            nombre_mayusculas = edit_nombre.value.upper()
            apellido_mayusculas = edit_apellido.value.upper()

            update_paciente(
                edit_id.value, nombre_mayusculas, apellido_mayusculas,
                edit_sexo.value, edit_fecha.value, edit_historia.value, encoded_photo
            )
            edit_dialog.open = False
            refresh_pacientes()
        except Exception as ex:
            show_alert(f"Error al actualizar paciente: {str(ex)}")

    def clear_fields():
        nonlocal selected_photo
        paciente_id.value = ""
        paciente_nombre.value = ""
        paciente_apellido.value = ""
        paciente_sexo.value = "M"  # Restablecer el valor del Dropdown a None
        paciente_fecha.value = ""
        paciente_historia.value = ""
        selected_photo = None
        photo_preview.src = None
        photo_preview.visible = False  # Oculta la vista previa de la imagen
        default_photo_icon.visible = True  # Muestra el icono por defecto
        page.update()  # Forzar la actualización de la interfaz

    def close_edit_dialog(e):
        edit_dialog.open = False
        edit_sexo.value = None  # Restablecer el valor del Dropdown a None
        page.update()  # Forzar la actualización de la interfaz

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

    # Crear el formulario desde utils
    form_data = crear_formulario_paciente(page, add_paciente_clicked, on_file_picked)
    form_expansion = form_data["form_expansion"]
    paciente_id = form_data["paciente_id"]
    paciente_nombre = form_data["paciente_nombre"]
    paciente_apellido = form_data["paciente_apellido"]
    paciente_sexo = form_data["paciente_sexo"]
    paciente_sexo.value = "M" 
    paciente_fecha = form_data["paciente_fecha"]
    paciente_historia = form_data["paciente_historia"]
    default_photo_icon = form_data["default_photo_icon"]
    photo_preview = form_data["photo_preview"]
    file_picker = form_data["file_picker"]

    pacientes_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)  # Habilitar scroll en la lista de pacientes

    # Diálogo de edición
    edit_id = ft.TextField(label="ID Paciente", disabled=True)
    edit_nombre = ft.TextField(label="Nombre")
    edit_apellido = ft.TextField(label="Apellido")
    edit_sexo = ft.Dropdown(
        label="Sexo",
        options=[ft.dropdown.DropdownOption("M"), ft.dropdown.DropdownOption("F"), ft.dropdown.DropdownOption("O")]
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
            ft.TextButton("Cancelar", on_click=close_edit_dialog)
        ],
    )

    # Campo de búsqueda
    search_field = ft.TextField(
        label="Buscar por nombre o apellido",
        on_change=on_search,
        expand=True,
        suffix=ft.IconButton(ft.icons.SEARCH, on_click=on_search)
    )

    # Diálogo de alerta para mostrar errores
    alert_dialog = ft.AlertDialog(
        title=ft.Text("Error"),
        content=ft.Text(""),
        actions=[
            ft.TextButton("OK", on_click=lambda e: setattr(alert_dialog, "open", False) or page.update())
        ],
    )

    # Crear el ExpansionPanel solo para el formulario de agregar paciente
    form_panel = ft.ExpansionPanel(
        header=ft.ListTile(
            title=ft.Text("Agregar Nuevo Paciente"),
            on_click=lambda e: setattr(form_panel, "expanded", not form_panel.expanded) or page.update()  # Alternar expansión
        ),
        content=ft.Column([form_expansion]),  # Contenido del formulario
        expanded=False  # Inicialmente colapsado
    )

    # Crear el ExpansionPanelList solo con el panel del formulario
    expansion_panel_list = ft.ExpansionPanelList(
        controls=[form_panel],
        on_change=lambda e: page.update()  # Actualizar la página cuando cambie el estado del panel
    )

    refresh_pacientes()

    return ft.Column(
        [
            ft.Text("Gestión de Pacientes", size=24, weight=ft.FontWeight.BOLD),
            expansion_panel_list,  # Mostrar el panel del formulario
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),  # Espacio entre el formulario y la lista
            ft.Row([search_field], alignment=ft.MainAxisAlignment.CENTER),  # Barra de búsqueda
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),  # Espacio entre la barra de búsqueda y la lista
            ft.Container(
                content=pacientes_list,
                expand=True,
                padding=10,
                alignment=ft.alignment.top_center
            ),  # Lista de pacientes
            ft.Row([
                ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: change_page(-1)),
                ft.Text(f"Página {current_page + 1}"),
                ft.IconButton(ft.icons.ARROW_FORWARD, on_click=lambda e: change_page(1)),
            ], alignment=ft.MainAxisAlignment.CENTER),  # Controles de paginación
            edit_dialog,
            alert_dialog
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO  # Habilitar scroll en la columna principal
    )