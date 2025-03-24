import flet as ft
import re
from datetime import datetime


def paciente_tiene_tamizaje(paciente_id, all_tamizajes):
    """Verifica si un paciente ya tiene un tamizaje."""
    for tamizaje in all_tamizajes:
        if tamizaje["paciente"].id_paciente == paciente_id:
            return True
    return False


def validar_fecha(formato_fecha):
    # Expresión regular para validar el formato dd-mm-yyyy
    if not re.match(r"^\d{2}-\d{2}-\d{4}$", formato_fecha):
        return False

    # Verificar si la fecha es válida
    try:
        dia, mes, anio = map(int, formato_fecha.split("-"))
        datetime(year=anio, month=mes, day=dia)
        return True
    except ValueError:
        return False


def crear_formulario_tamizaje(
    page, add_tamizaje_clicked, on_paciente_search, select_paciente, all_tamizajes
):
    ancho_campo = 300
    # Campos del formulario
    tamizaje_paciente = ft.TextField(label="ID Paciente", width=200, read_only=True)
    tamizaje_tipo = ft.Dropdown(
        label="Tipo de antecedente médico",
        options=[
            ft.dropdown.DropdownOption("Personal"),
            ft.dropdown.DropdownOption("Familiar"),
        ],
        width=ancho_campo,
    )
    tamizaje_descripcion = ft.TextField(
        label="Descripción del antecedente médico", expand=True
    )
    tamizaje_fecha = ft.TextField(
        label="Fecha Nacimiento (dd-mm-yyyy)",
        width=ancho_campo,
        hint_text="Ej: 15-05-1990",
        on_change=lambda e: validar_fecha_campo(tamizaje_fecha),
    )
    tamizaje_presion_arterial = ft.TextField(label="Presión arterial", expand=True)
    tamizaje_frecuencia_cardiaca = ft.TextField(
        label="Frecuencia cardíaca", expand=True
    )
    tamizaje_frecuencia_respiratoria = ft.TextField(
        label="Frecuencia respiratoria", expand=True
    )
    tamizaje_temperatura = ft.TextField(label="Temperatura", expand=True)
    tamizaje_peso = ft.TextField(label="Peso", expand=True)
    tamizaje_talla = ft.TextField(label="Talla", expand=True)

    # Función para validar el campo de fecha
    def validar_fecha_campo(campo_fecha):
        if campo_fecha.value:
            if not validar_fecha(campo_fecha.value):
                campo_fecha.error_text = "Formato inválido. Use dd-mm-yyyy."
            else:
                campo_fecha.error_text = None
            page.update()

    # Campo de búsqueda de pacientes
    paciente_search_field = ft.TextField(
        label="Buscar paciente por nombre o apellido",
        on_change=on_paciente_search,
        expand=True,
    )
    paciente_results = ft.Column()

    # Botón de agregar
    agregar_button = ft.ElevatedButton("Agregar", on_click=add_tamizaje_clicked)

    # Crear el contenido del formulario (sin ExpansionTile)
    form_content = ft.Column(
        [
            ft.Divider(height=10, color=ft.colors.TRANSPARENT),
            paciente_search_field,
            paciente_results,
            ft.Row(
                [tamizaje_paciente, tamizaje_tipo, tamizaje_descripcion], spacing=15
            ),
            ft.Row(
                [
                    tamizaje_fecha,
                    tamizaje_presion_arterial,
                    tamizaje_frecuencia_cardiaca,
                ],
                spacing=15,
            ),
            ft.Row(
                [
                    tamizaje_frecuencia_respiratoria,
                    tamizaje_temperatura,
                    tamizaje_peso,
                    tamizaje_talla,
                ],
                spacing=15,
            ),
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
            ft.Row([agregar_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
        ],
        spacing=10,
    )

    return {
        "form_content": form_content,
        "tamizaje_paciente": tamizaje_paciente,
        "tamizaje_tipo": tamizaje_tipo,
        "tamizaje_descripcion": tamizaje_descripcion,
        "tamizaje_fecha": tamizaje_fecha,
        "tamizaje_presion_arterial": tamizaje_presion_arterial,
        "tamizaje_frecuencia_cardiaca": tamizaje_frecuencia_cardiaca,
        "tamizaje_frecuencia_respiratoria": tamizaje_frecuencia_respiratoria,
        "tamizaje_temperatura": tamizaje_temperatura,
        "tamizaje_peso": tamizaje_peso,
        "tamizaje_talla": tamizaje_talla,
        "paciente_search_field": paciente_search_field,
        "paciente_results": paciente_results,
        "agregar_button": agregar_button,
        "paciente_tiene_tamizaje": paciente_tiene_tamizaje,  # Devolver la función de validación
    }
