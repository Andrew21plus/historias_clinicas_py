import flet as ft
from datetime import datetime
def crear_buscador_pacientes(on_search, on_select):
    search_field = ft.TextField(
        label="Buscar paciente",
        hint_text="Ingrese nombre o apellido",
        on_change=on_search,
        suffix=ft.IconButton(icon=ft.icons.SEARCH, on_click=on_search),
        width=400
    )
    
    pacientes_list = ft.ListView(expand=True, spacing=10)
    
    return {
        "search_field": search_field,
        "pacientes_list": pacientes_list,
        "container": ft.Column([
            search_field,
            ft.Container(
                content=pacientes_list,
                height=200,
                border=ft.border.all(1),
                padding=10,
                border_radius=10
            )
        ])
    }

def crear_formulario_certificado():
    # Controles del formulario
    diagnostico_container = ft.Column([])  # Reemplazamos el Dropdown por un contenedor para Checkboxes
    
    cie_input = ft.TextField(
        label="CIE-10",
        read_only=True,
        width=200,
        multiline=True  # Permitir múltiples CIE
    )
    
    fecha_consulta = ft.TextField(
        label="Fecha de consulta",
        read_only=True,
        width=200,
        value=datetime.now().strftime("%d/%m/%Y")
    )
    
    fecha_consulta_button = ft.ElevatedButton(
        "Seleccionar fecha",
        icon=ft.icons.CALENDAR_MONTH,
        disabled=True
    )
    
    contingencia_radio = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="enfermedad", label="Enfermedad"),
            ft.Radio(value="maternidad", label="Maternidad"),
            ft.Radio(value="accidente", label="Accidente"),
            ft.Radio(value="emergencia", label="Emergencia"),
        ]),
        value="enfermedad"
    )
    
    indicaciones_input = ft.TextField(
        label="Indicaciones médicas",
        multiline=True,
        min_lines=3,
        max_lines=5,
        width=400,
        border=ft.InputBorder.UNDERLINE,
        filled=True
    )
    
    dias_reposo = ft.TextField(
        label="Días de reposo",
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]"),
        width=150
    )
    
    return {
        "diagnostico_container": diagnostico_container,
        "cie": cie_input,
        "fecha_consulta": fecha_consulta,
        "fecha_consulta_button": fecha_consulta_button,
        "contingencia": contingencia_radio,
        "indicaciones": indicaciones_input,
        "dias_reposo": dias_reposo,
        "form": ft.Column([
            ft.Text("Datos del Certificado", size=18, weight=ft.FontWeight.BOLD),
            ft.Row([
                fecha_consulta,
                fecha_consulta_button
            ], spacing=20),
            ft.Text("Diagnósticos:", weight=ft.FontWeight.BOLD),
            diagnostico_container,
            ft.Text("CIE-10:", weight=ft.FontWeight.BOLD),
            cie_input,
            ft.Text("Tipo de contingencia:", weight=ft.FontWeight.BOLD),
            contingencia_radio,
            ft.Text("Indicaciones médicas:", weight=ft.FontWeight.BOLD),
            indicaciones_input,
            ft.Text("Días de reposo:", weight=ft.FontWeight.BOLD),
            dias_reposo
        ], spacing=15)
    }