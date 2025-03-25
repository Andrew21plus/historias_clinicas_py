import flet as ft
import base64
from .paciente_crud import (
    obtener_pacientes,
    agregar_paciente,
    actualizar_paciente,
    eliminar_paciente,
    calcular_edad,
)
from .paciente_ui import crear_paciente_ui
from utils.formulario_paciente import crear_formulario_paciente
from ..historia_clinica.historia_clinica_crud import agregar_historia_clinica


def PacientesScreen(page: ft.Page, id_usuario: int):
    selected_photo = None  # Variable para almacenar la imagen seleccionada
    existing_photo = None  # Variable para almacenar la foto existente al editar
    current_page = 0  # Página actual de la paginación
    pacientes_per_page = 5  # Número de pacientes por página
    search_query = ""  # Variable para almacenar la consulta de búsqueda
    all_pacientes = []  # Lista para almacenar todos los pacientes
    selected_paciente_id = (
        None  # Variable para almacar el ID del paciente seleccionado para eliminar
    )

    def show_alert(message):
        """Muestra un diálogo de alerta con el mensaje proporcionado."""
        alert_dialog.content = ft.Text(message)
        alert_dialog.open = True
        page.update()

    def validar_campos_requeridos(campos):
        campos_faltantes = [campo for campo in campos if not campo.value]
        if campos_faltantes:
            show_alert(
                f"Por favor, complete los siguientes campos: {', '.join([campo.label for campo in campos_faltantes])}"
            )
            return False
        return True

    def confirm_delete(confirmed):
        """Maneja la confirmación de eliminación."""
        nonlocal selected_paciente_id
        confirm_delete_dialog.open = False
        page.update()
        if confirmed:
            eliminar_paciente(selected_paciente_id)  # Eliminar el paciente
            refresh_pacientes()
        selected_paciente_id = None  # Reiniciar el ID del paciente seleccionado

    def refresh_pacientes():
        """Actualiza la lista de pacientes con estilos consistentes."""
        nonlocal all_pacientes
        pacientes_list.controls.clear()
        all_pacientes = obtener_pacientes(id_usuario, search_query)

        # Paginación
        start_index = current_page * pacientes_per_page
        end_index = start_index + pacientes_per_page
        
        for paciente in all_pacientes[start_index:end_index]:
            # Widget de foto
            photo_widget = ft.Icon(ft.icons.PERSON, size=100)  # Icono por defecto con color
            if paciente.foto:
                photo_widget = ft.Image(
                    src_base64=base64.b64encode(paciente.foto).decode(),
                    width=100,
                    height=100,
                    fit=ft.ImageFit.COVER,
                    border_radius=ft.border_radius.all(5),
                )

            # Calcular edad
            edad = calcular_edad(paciente.fecha_nacimiento)

            # Crear card del paciente con estilos consistentes
            paciente_card = ft.Card(
                content=ft.Container(
                    content=ft.Row(
                        [
                            # Columna izquierda (foto)
                            ft.Container(
                                content=photo_widget,
                                padding=10,
                                alignment=ft.alignment.center,
                                width=120,
                            ),
                            
                            # Columna derecha (datos)
                            ft.Column(
                                [
                                    # Fila superior (nombre y botones)
                                    ft.Row(
                                        [
                                            ft.Text(
                                                f"👤 {paciente.nombre} {paciente.apellido}",
                                                weight=ft.FontWeight.BOLD,
                                                size=16,
                                                expand=True,
                                            ),
                                            ft.Row(
                                                [
                                                    ft.IconButton(
                                                        ft.icons.EDIT,
                                                        icon_color=ft.colors.BLUE,
                                                        tooltip="Editar paciente",
                                                        on_click=lambda e, p=paciente: open_edit_dialog(p),
                                                    ),
                                                    ft.IconButton(
                                                        ft.icons.DELETE,
                                                        icon_color=ft.colors.RED,
                                                        tooltip="Eliminar paciente",
                                                        on_click=lambda e, id_paciente=paciente.id_paciente: confirm_delete_dialog_handler(id_paciente),
                                                    ),
                                                ],
                                                spacing=5,
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),
                                    
                                    # Datos del paciente con nuevo estilo
                                    ft.Column(
                                        [
                                            ft.Row(
                                                [
                                                    ft.Text("📋 ID:", weight=ft.FontWeight.BOLD),
                                                    ft.Text(paciente.id_paciente),
                                                ],
                                                spacing=5,
                                            ),
                                            ft.Row(
                                                [
                                                    ft.Text(" ⚥  Sexo:", weight=ft.FontWeight.BOLD),
                                                    ft.Text(paciente.sexo),
                                                ],
                                                spacing=5,
                                            ),
                                            ft.Row(
                                                [
                                                    ft.Text("🎂 Fecha Nac:", weight=ft.FontWeight.BOLD),
                                                    ft.Text(paciente.fecha_nacimiento),
                                                ],
                                                spacing=5,
                                            ),
                                            ft.Row(
                                                [
                                                    ft.Text("🔢 Edad:", weight=ft.FontWeight.BOLD),
                                                    ft.Text(edad),
                                                ],
                                                spacing=5,
                                            ),
                                            ft.Row(
                                                [
                                                    ft.Text("🏥 HC:", weight=ft.FontWeight.BOLD),
                                                    ft.Text(paciente.num_historia_clinica, italic=True),
                                                ],
                                                spacing=5,
                                            ),
                                        ],
                                        spacing=3,
                                    ),
                                ],
                                spacing=8,
                                expand=True,
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=ft.padding.symmetric(vertical=10, horizontal=15),
                ),
                elevation=3,
                margin=ft.margin.symmetric(vertical=5),
                width=page.window_width * 0.95,
            )
            pacientes_list.controls.append(paciente_card)
        
        page.update()

    def confirm_delete_dialog_handler(id_paciente):
        """Abre el diálogo de confirmación para eliminar."""
        nonlocal selected_paciente_id
        selected_paciente_id = id_paciente  # Guardar el ID del paciente seleccionado
        confirm_delete_dialog.open = True
        page.update()

    def mostrar_dialogo_historia_clinica(id_paciente, nombre_completo):
        """Muestra el diálogo para agregar historia clínica"""
        historia_dialog.title = ft.Text(
            f"Agregar Historia Clínica para {nombre_completo}"
        )
        historia_paciente_id.value = id_paciente
        historia_motivo.value = ""
        historia_enfermedad.value = ""
        historia_dialog.open = True
        page.update()

    def guardar_historia_clinica(e):
        """Guarda la historia clínica del paciente"""
        if not all([historia_motivo.value, historia_enfermedad.value]):
            # Configura el diálogo de alerta existente
            alert_dialog.title = ft.Row(
                controls=[
                    ft.Icon(ft.icons.WARNING_AMBER, color=ft.colors.AMBER),
                    ft.Text(" Campos incompletos", weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
            
            alert_dialog.content = ft.Text(
                "No se pudo crear la historia clínica porque faltan datos.\n\n"
                "Por favor complete:\n"
                f"- {'Motivo de consulta' if not historia_motivo.value else ''}\n"
                f"- {'Enfermedad actual' if not historia_enfermedad.value else ''}\n\n"
                "Puede completarlos desde el menú 'Historia clínica'."
            )
            
            alert_dialog.open = True
            page.update()
            return

        try:
            agregar_historia_clinica(
                historia_paciente_id.value,
                historia_motivo.value,
                historia_enfermedad.value,
                id_usuario,
            )
            historia_dialog.open = False
            success_dialog.title = ft.Text("Éxito")
            success_dialog.content = ft.Text("Historia clínica agregada exitosamente")
            success_dialog.open = True
            page.update()
        except Exception as ex:
            alert_dialog.title = ft.Text("Error")
            alert_dialog.content = ft.Text(
                f"Error al agregar historia clínica: {str(ex)}"
            )
            alert_dialog.open = True
            page.update()

    def add_paciente_clicked(e):
        """Agrega un nuevo paciente."""
        # Validar campos requeridos
        campos_requeridos = [
            paciente_id,
            paciente_nombre,
            paciente_apellido,
            paciente_sexo,
            paciente_fecha,
            paciente_historia,
        ]
        if not validar_campos_requeridos(campos_requeridos):
            return

        if all(
            [
                paciente_id.value,
                paciente_nombre.value,
                paciente_apellido.value,
                paciente_sexo.value,
                paciente_fecha.value,
                paciente_historia.value,
            ]
        ):
            encoded_photo = None
            if selected_photo:
                with open(selected_photo, "rb") as image_file:
                    encoded_photo = image_file.read()

            try:
                # Convertir nombre y apellido a mayúsculas
                nombre_mayusculas = paciente_nombre.value.upper()
                apellido_mayusculas = paciente_apellido.value.upper()

                # Llamar a agregar_paciente con el id_usuario
                agregar_paciente(
                    paciente_id.value,
                    nombre_mayusculas,
                    apellido_mayusculas,
                    paciente_sexo.value,
                    paciente_fecha.value,
                    paciente_historia.value,
                    encoded_photo,
                    id_usuario,
                )

                # Mostrar diálogo para agregar historia clínica
                nombre_completo = f"{nombre_mayusculas} {apellido_mayusculas}"
                mostrar_dialogo_historia_clinica(paciente_id.value, nombre_completo)

                clear_fields()  # Limpiar los campos después de agregar
                form_panel.expanded = False  # Colapsar el panel del formulario
                refresh_pacientes()

            except Exception as ex:
                show_alert(f"Error al agregar paciente: {str(ex)}")

    def open_edit_dialog(paciente):
        """Abre el diálogo de edición para un paciente."""
        nonlocal selected_photo, existing_photo
        selected_photo = None  # Reiniciar la foto seleccionada al abrir el diálogo
        existing_photo = paciente.foto  # Guardar la foto existente
        edit_id.value = paciente.id_paciente
        edit_nombre.value = paciente.nombre
        edit_apellido.value = paciente.apellido
        edit_sexo.value = paciente.sexo
        edit_fecha.value = paciente.fecha_nacimiento
        edit_historia.value = paciente.num_historia_clinica
        edit_photo_preview.src_base64 = (
            base64.b64encode(paciente.foto).decode() if paciente.foto else None
        )
        edit_photo_preview.visible = paciente.foto is not None
        edit_default_photo_icon.visible = paciente.foto is None
        edit_dialog.open = True
        page.update()

    def save_edit(e):
        """Guarda los cambios realizados en el paciente."""
        campos_requeridos = [
            edit_id,
            edit_nombre,
            edit_apellido,
            edit_sexo,
            edit_fecha,
            edit_historia,
        ]
        if not validar_campos_requeridos(campos_requeridos):
            return

        encoded_photo = existing_photo  # Usar la foto existente por defecto
        if selected_photo:  # Si se selecciona una nueva foto, actualizar
            with open(selected_photo, "rb") as image_file:
                encoded_photo = image_file.read()

        try:
            # Convertir nombre y apellido a mayúsculas
            nombre_mayusculas = edit_nombre.value.upper()  # type: ignore
            apellido_mayusculas = edit_apellido.value.upper()  # type: ignore

            actualizar_paciente(
                edit_id.value,
                nombre_mayusculas,
                apellido_mayusculas,
                edit_sexo.value,
                edit_fecha.value,
                edit_historia.value,
                id_usuario,
                encoded_photo,
            )
            edit_dialog.open = False
            refresh_pacientes()
        except Exception as ex:
            show_alert(f"Error al actualizar paciente: {str(ex)}")

    def clear_fields():
        """Limpia los campos del formulario."""
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

    def on_file_picked(e: ft.FilePickerResultEvent):
        """Maneja la selección de una foto al agregar un paciente."""
        nonlocal selected_photo
        if e.files:
            selected_photo = e.files[0].path
            photo_preview.src = selected_photo
            photo_preview.visible = True  # Muestra la vista previa de la imagen
            default_photo_icon.visible = False  # Oculta el icono por defecto
            page.update()

    def on_edit_file_picked(e: ft.FilePickerResultEvent):
        """Maneja la selección de una foto al editar un paciente."""
        nonlocal selected_photo
        if e.files:
            selected_photo = e.files[0].path
            edit_photo_preview.src = selected_photo
            edit_photo_preview.visible = True  # Muestra la vista previa de la imagen
            edit_default_photo_icon.visible = False  # Oculta el icono por defecto
            page.update()

    def change_page(delta):
        """Cambia la página actual."""
        nonlocal current_page
        current_page += delta
        if current_page < 0:
            current_page = 0
        max_pages = (len(all_pacientes) + pacientes_per_page - 1) // pacientes_per_page
        if current_page >= max_pages:
            current_page = max_pages - 1
        page_number_text.value = f"Página {current_page + 1}"
        refresh_pacientes()

    def on_search(e):
        """Filtra los pacientes según la consulta de búsqueda."""
        nonlocal search_query, current_page
        search_query = search_field.value
        current_page = 0  # Reiniciar la página a 0 al realizar una nueva búsqueda
        page_number_text.value = (
            f"Página {current_page + 1}"  # Actualizar el texto del número de página
        )
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

    # Crear la interfaz de usuario
    ui = crear_paciente_ui(
        page,
        confirm_delete,
        save_edit,
        on_search,
        change_page,
        on_edit_file_picked,
        guardar_historia_clinica,
    )

    # Acceder a los componentes de la UI
    page_number_text = ui["page_number_text"]
    confirm_delete_dialog = ui["confirm_delete_dialog"]
    alert_dialog = ui["alert_dialog"]
    success_dialog = ui["success_dialog"]
    search_field = ui["search_field"]
    pacientes_list = ui["pacientes_list"]
    edit_id = ui["edit_id"]
    edit_nombre = ui["edit_nombre"]
    edit_apellido = ui["edit_apellido"]
    edit_sexo = ui["edit_sexo"]
    edit_fecha = ui["edit_fecha"]
    edit_historia = ui["edit_historia"]
    edit_default_photo_icon = ui["edit_default_photo_icon"]
    edit_photo_preview = ui["edit_photo_preview"]
    edit_file_picker = ui["edit_file_picker"]
    edit_dialog = ui["edit_dialog"]
    historia_dialog = ui["historia_dialog"]
    historia_paciente_id = ui["historia_paciente_id"]
    historia_motivo = ui["historia_motivo"]
    historia_enfermedad = ui["historia_enfermedad"]
    pagination_controls = ui["pagination_controls"]

    # Crear el ExpansionPanel para el formulario
    form_panel = ft.ExpansionPanel(
        header=ft.ListTile(
            title=ft.Text("Agregar Nuevo Paciente"),
            on_click=lambda e: setattr(form_panel, "expanded", not form_panel.expanded)
            or page.update(),
        ),
        content=ft.Column([form_expansion]),  # Contenido del formulario
        expanded=False,  # Inicialmente colapsado
    )

    # Crear el ExpansionPanelList solo con el panel del formulario
    expansion_panel_list = ft.ExpansionPanelList(
        controls=[form_panel],
        on_change=lambda e: page.update(),  # Actualizar la página cuando cambie el estado del panel
    )

    refresh_pacientes()

    return ft.Column(
        [
            ft.Text("Gestión de Pacientes", size=24, weight=ft.FontWeight.BOLD),
            expansion_panel_list,  # Mostrar el panel del formulario
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
            ft.Row([search_field], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
            ft.Container(
                content=pacientes_list,
                expand=True,
                padding=10,
                alignment=ft.alignment.top_center,
            ),
            pagination_controls,
            edit_dialog,
            confirm_delete_dialog,
            alert_dialog,
            success_dialog,
            historia_dialog,  # Diálogo para agregar historia clínica
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )
