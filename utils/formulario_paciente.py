# utils/formulario_paciente.py
import flet as ft
import re
from datetime import datetime

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

def validar_fecha(formato_fecha):
    # Expresión regular para validar el formato dd-mm-yyyy
    if not re.match(r"^\d{2}-\d{2}-\d{4}$", formato_fecha):
        return False

    # Verificar si la fecha es válida
    try:
        dia, mes, anio = map(int, formato_fecha.split('-'))
        datetime(year=anio, month=mes, day=dia)
        return True
    except ValueError:
        return False

def crear_formulario_paciente(page, add_paciente_clicked, on_file_picked):
    # Campos del formulario
    ancho_campo = 300  # Ancho fijo para todos los campos

    paciente_id = ft.TextField(label="ID Paciente", width=ancho_campo)
    paciente_nombre = ft.TextField(label="Nombre", width=ancho_campo)
    paciente_apellido = ft.TextField(label="Apellido", width=ancho_campo)
    paciente_sexo = ft.Dropdown(
        label="Sexo",
        options=[ft.dropdown.DropdownOption("M"), ft.dropdown.DropdownOption("F"), ft.dropdown.DropdownOption("O")],
        width=ancho_campo
    )
    paciente_fecha = ft.TextField(
        label="Fecha Nacimiento (dd-mm-yyyy)",
        width=ancho_campo,
        hint_text="Ej: 15-05-1990",
        on_change=lambda e: validar_fecha_campo(paciente_fecha)
    )
    paciente_historia = ft.TextField(label="Historia Clínica", width=ancho_campo)

    # Función para validar el campo de fecha
    def validar_fecha_campo(campo_fecha):
        if campo_fecha.value:
            if not validar_fecha(campo_fecha.value):
                campo_fecha.error_text = "Formato inválido. Use dd-mm-yyyy."
            else:
                campo_fecha.error_text = None
            page.update()

    # Vista previa de la foto y icono por defecto
    default_photo_icon = ft.Icon(ft.icons.PERSON, size=100, visible=True)
    photo_preview = ft.Image(width=100, height=100, visible=False)  # Inicialmente oculta
    file_picker = ft.FilePicker(on_result=on_file_picked)  # Usar on_file_picked aquí

    # Formulario reorganizado en dos columnas
    form_expansion = ft.Column(
        [
            ft.Divider(height=10, color=ft.colors.TRANSPARENT),  # Espacio de 10 unidades

            # Fila principal con dos columnas
            ft.Row(
                [
                    # Columna 1: Campos del formulario (organizados en filas de dos campos)
                    ft.Column(
                        [
                            # Fila 1: ID e Historia Clínica
                            ft.Row(
                                [
                                    paciente_id,
                                    ft.Container(width=20),  # Espacio entre ID e Historia Clínica
                                    paciente_historia
                                ],
                                spacing=15
                            ),

                            # Fila 2: Nombre y Apellido
                            ft.Row(
                                [
                                    paciente_nombre,
                                    ft.Container(width=20),  # Espacio entre Nombre y Apellido
                                    paciente_apellido
                                ],
                                spacing=15
                            ),

                            # Fila 3: Sexo y Fecha
                            ft.Row(
                                [
                                    paciente_sexo,
                                    ft.Container(width=20),  # Espacio entre Sexo y Fecha
                                    paciente_fecha
                                ],
                                spacing=15
                            )
                        ],
                        spacing=10  # Espacio entre las filas de campos
                    ),

                    # Columna 2: Foto y botón para seleccionar foto
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Column(
                                        [
                                            default_photo_icon,
                                            photo_preview
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER
                                    ),
                                    ft.Column(
                                        [
                                            file_picker,
                                            ft.ElevatedButton(
                                                "Seleccionar Foto",
                                                on_click=lambda e: file_picker.pick_files(allow_multiple=False)
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER
                                    )
                                ],
                                spacing=5
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START
                    )
                ],
                spacing=100  # Espacio entre las dos columnas
            ),

            # Espacio antes del botón Agregar
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),

            # Botón Agregar
            ft.Row(
                [ft.ElevatedButton("Agregar", on_click=add_paciente_clicked)],
                alignment=ft.MainAxisAlignment.CENTER
            ),

            # Espacio después del botón Agregar
            ft.Divider(height=20, color=ft.colors.TRANSPARENT)
        ],
        spacing=10  # Espacio entre las filas
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