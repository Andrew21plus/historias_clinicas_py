import flet as ft
import base64
from services.paciente_service import get_pacientes, add_paciente, update_paciente, delete_paciente

def PacientesScreen(page):
    selected_photo = None  # Variable para almacenar la imagen seleccionada

    def refresh_pacientes():
        pacientes_list.controls.clear()
        pacientes = get_pacientes()
        for paciente in pacientes:
            photo_widget = None
            if paciente.foto:
                photo_widget = ft.Image(src_base64=base64.b64encode(paciente.foto).decode(), width=100, height=100)

            paciente_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(f"{paciente.nombre} {paciente.apellido}", weight=ft.FontWeight.BOLD),
                                    ft.Row([
                                        ft.IconButton(ft.icons.EDIT, on_click=lambda e, p=paciente: open_edit_dialog(p)),
                                        ft.IconButton(ft.icons.DELETE, on_click=lambda e, id_paciente=paciente.id_paciente: remove_paciente(id_paciente))
                                    ])
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Text(f"ID: {paciente.id_paciente} - Sexo: {paciente.sexo} - Fecha Nac: {paciente.fecha_nacimiento}"),
                            ft.Text(f"Historia Clínica: {paciente.num_historia_clinica}", italic=True),
                            photo_widget if photo_widget else ft.Text("No hay foto")
                        ]
                    ),
                    padding=10
                ),
                width=page.window_width * 0.95
            )
            pacientes_list.controls.append(paciente_card)
        page.update()

    def add_paciente_clicked(e):
        if all([paciente_id.value, paciente_nombre.value, paciente_apellido.value, paciente_sexo.value, paciente_fecha.value, paciente_historia.value]):
            with open(selected_photo, "rb") as image_file:
                encoded_photo = image_file.read() if selected_photo else None

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
        edit_id.value = paciente.id_paciente
        edit_nombre.value = paciente.nombre
        edit_apellido.value = paciente.apellido
        edit_sexo.value = paciente.sexo
        edit_fecha.value = paciente.fecha_nacimiento
        edit_historia.value = paciente.num_historia_clinica
        edit_dialog.open = True
        page.update()

    def save_edit(e):
        update_paciente(edit_id.value, edit_nombre.value, edit_apellido.value, edit_sexo.value, edit_fecha.value, edit_historia.value)
        edit_dialog.open = False
        refresh_pacientes()

    def clear_fields():
        paciente_id.value = ""
        paciente_nombre.value = ""
        paciente_apellido.value = ""
        paciente_sexo.value = ""
        paciente_fecha.value = ""
        paciente_historia.value = ""
        page.update()

    def on_file_picked(e: ft.FilePickerResultEvent):
        nonlocal selected_photo
        if e.files:
            selected_photo = e.files[0].path
            photo_preview.src = selected_photo
            page.update()

    paciente_id = ft.TextField(label="ID Paciente", width=150)
    paciente_nombre = ft.TextField(label="Nombre", expand=True)
    paciente_apellido = ft.TextField(label="Apellido", expand=True)
    paciente_sexo = ft.Dropdown(
        label="Sexo",
        options=[ft.dropdown.DropdownOption("M"), ft.dropdown.DropdownOption("F"), ft.dropdown.DropdownOption("O")],
        width=100
    )
    paciente_fecha = ft.TextField(label="Fecha Nacimiento", width=200)
    paciente_historia = ft.TextField(label="Historia Clínica", expand=True)
    pacientes_list = ft.Column(scroll=ft.ScrollMode.AUTO)
    
    photo_preview = ft.Image(width=100, height=100)  # Muestra una vista previa de la imagen
    file_picker = ft.FilePicker(on_result=on_file_picked)

    edit_id = ft.TextField(label="ID Paciente", disabled=True)
    edit_nombre = ft.TextField(label="Nombre")
    edit_apellido = ft.TextField(label="Apellido")
    edit_sexo = ft.Dropdown(
        label="Sexo",
        options=[ft.dropdown.DropdownOption("M"), ft.dropdown.DropdownOption("F"), ft.dropdown.DropdownOption("O")]
    )
    edit_fecha = ft.TextField(label="Fecha Nacimiento")
    edit_historia = ft.TextField(label="Historia Clínica")
    edit_dialog = ft.AlertDialog(
        title=ft.Text("Editar Paciente"),
        content=ft.Column([edit_nombre, edit_apellido, edit_sexo, edit_fecha, edit_historia]),
        actions=[
            ft.TextButton("Guardar", on_click=save_edit),
            ft.TextButton("Cancelar", on_click=lambda e: setattr(edit_dialog, "open", False) or page.update())
        ],
    )

    refresh_pacientes()

    return ft.Column(
        [
            ft.Text("Gestión de Pacientes", size=24, weight=ft.FontWeight.BOLD),
            ft.Column([
                ft.Row([paciente_id, paciente_nombre, paciente_apellido], spacing=10),
                ft.Row([paciente_sexo, paciente_fecha, paciente_historia], spacing=10),
                ft.Row([
                    file_picker,  # Botón para seleccionar archivos
                    ft.ElevatedButton("Seleccionar Foto", on_click=lambda e: file_picker.pick_files(allow_multiple=False)),
                    photo_preview  # Vista previa de la foto
                ]),
                ft.Row([ft.ElevatedButton("Agregar", on_click=add_paciente_clicked)], alignment=ft.MainAxisAlignment.CENTER)
            ], spacing=10),
            pacientes_list,
            edit_dialog
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
