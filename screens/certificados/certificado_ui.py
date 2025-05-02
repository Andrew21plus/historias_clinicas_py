import flet as ft
from datetime import datetime

def crear_buscador_pacientes(on_search, on_select):
    search_field = ft.TextField(
        label="Buscar paciente",
        hint_text="Ingrese nombre o apellido",
        on_change=on_search,
        suffix=ft.IconButton(icon=ft.icons.SEARCH, on_click=on_search),
        width=700
    )
    
    pacientes_list = ft.ListView(expand=True, spacing=10)
    
    pacientes_container = ft.Container(
        content=pacientes_list,
        height=200,
        border=ft.border.all(1),
        padding=10,
        border_radius=10,
        visible=False,
        width=700
    )
    
    return {
        "search_field": search_field,
        "pacientes_list": pacientes_list,
        "pacientes_container": pacientes_container,
        "container": ft.Column(
            [
                ft.Container(
                    content=search_field,
                    alignment=ft.alignment.center,
                    padding=10
                ),
                ft.Container(
                    content=pacientes_container,
                    alignment=ft.alignment.center
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
    }

def crear_formulario_certificado():
    # Controles del formulario
    diagnostico_container = ft.Column([])
    
    cie_input = ft.TextField(
        label="CIE-10",
        read_only=True,
        width=700,
        multiline=True
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
    
    texto_certificacion = ft.TextField(
        label="Texto de certificación",
        multiline=True,
        min_lines=3,
        max_lines=5,
        value="CERTIFICO que el/la paciente fue atendido(a) en esta unidad médica "
              "por presentar los diagnósticos mencionados a continuación, requiriendo "
              "las indicaciones médicas correspondientes.",
        width=700,
        border=ft.InputBorder.UNDERLINE,
        filled=True
    )
    
    contingencia_radio = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="enfermedad", label="Enfermedad"),
                ft.Radio(value="maternidad", label="Maternidad"),
                ft.Radio(value="accidente", label="Accidente"),
                ft.Radio(value="emergencia", label="Emergencia"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        ),
        value="enfermedad"
    )
    
    indicaciones_input = ft.TextField(
        label="Indicaciones médicas",
        multiline=True,
        min_lines=3,
        max_lines=5,
        width=700,
        border=ft.InputBorder.UNDERLINE,
        filled=True
    )
    
    dias_reposo = ft.TextField(
        label="Días de reposo",
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]"),
        width=150
    )
    
    # Función para crear filas centradas
    def crear_fila_centrada(*controls, spacing=20):
        return ft.Row(
            controls,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=spacing
        )
    
    # Función para crear secciones con título centrado
    def crear_seccion(titulo, contenido):
        return ft.Column(
            [
                ft.Container(
                    content=ft.Text(titulo, weight=ft.FontWeight.BOLD),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(bottom=5, top=10)
                ),
                contenido
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    
    form_content = ft.Column(
        [
            crear_seccion(
                "Datos del Certificado",
                crear_fila_centrada(
                    fecha_consulta,
                    fecha_consulta_button
                )
            ),
            
            crear_seccion(
                "Texto de Certificación",
                ft.Container(
                    texto_certificacion,
                    width=700,
                    padding=10
                )
            ),
            
            crear_seccion(
                "Diagnósticos",
                ft.Container(
                    diagnostico_container,
                    width=700,
                    padding=10
                )
            ),
            
            crear_seccion(
                "CIE-10",
                ft.Container(
                    cie_input,
                    width=700,
                    padding=10
                )
            ),
            
            crear_seccion(
                "Tipo de contingencia",
                contingencia_radio
            ),
            
            crear_seccion(
                "Indicaciones médicas",
                ft.Container(
                    indicaciones_input,
                    width=700,
                    padding=10
                )
            ),
            
            crear_seccion(
                "Días de reposo",
                ft.Container(
                    dias_reposo,
                    padding=10
                )
            )
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    return {
        "diagnostico_container": diagnostico_container,
        "cie": cie_input,
        "fecha_consulta": fecha_consulta,
        "fecha_consulta_button": fecha_consulta_button,
        "texto_certificacion": texto_certificacion,
        "contingencia": contingencia_radio,
        "indicaciones": indicaciones_input,
        "dias_reposo": dias_reposo,
        "form": ft.Container(
            content=form_content,
            alignment=ft.alignment.center,
            padding=20,
            expand=True
        )
    }