import flet as ft

def validar_cedula_ecuatoriana(cedula):
    if len(cedula) != 10 or not cedula.isdigit():
        return False

    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    verificador = int(cedula[-1])
    suma = 0

    for i in range(9):
        valor = int(cedula[i]) * coeficientes[i]
        if valor >= 10:
            valor -= 9
        suma += valor

    total = (suma // 10 + 1) * 10 if suma % 10 != 0 else suma
    return (total - suma) == verificador

def crear_formulario_paciente(page, add_paciente_clicked, on_file_picked):
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
    
    # Vista previa de la foto y icono por defecto
    default_photo_icon = ft.Icon(ft.icons.PERSON, size=100, visible=True)
    photo_preview = ft.Image(width=100, height=100, visible=False)  # Inicialmente oculta
    file_picker = ft.FilePicker(on_result=on_file_picked)  # Usar on_file_picked aquí

    # Formulario sin ExpansionTile
    form_expansion = ft.Column(
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

    return {
        "form_expansion": form_expansion,
        "paciente_id": paciente_id,
        "paciente_nombre": paciente_nombre,
        "paciente_apellido": paciente_apellido,
        "paciente_sexo": paciente_sexo,
        "paciente_fecha": paciente_fecha,
        "paciente_historia": paciente_historia,
        "default_photo_icon": default_photo_icon,
        "photo_preview": photo_preview,
        "file_picker": file_picker
    }