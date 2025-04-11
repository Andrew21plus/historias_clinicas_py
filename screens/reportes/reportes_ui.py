import flet as ft
from datetime import datetime, timedelta
from services.cie_service import get_cie
from .reportes_crud import obtener_periodos_disponibles, obtener_cie_disponibles

def crear_reportes_ui(page, id_usuario):
    """Crea los componentes de UI para los reportes con tooltips mejorados"""
    
    # Obtener datos dinámicos para los dropdowns
    periodos_disponibles = obtener_periodos_disponibles(id_usuario)
    cie_disponibles = obtener_cie_disponibles(id_usuario)
    
    # Obtener todos los CIE con sus descripciones
    todos_cie = get_cie()
    cie_dict = {cie.codigo: cie.descripcion for cie in todos_cie if hasattr(cie, 'codigo') and hasattr(cie, 'descripcion')}
    
    # Configuración común para tooltips
    tooltip_config = {
        'tooltip_bgcolor': ft.colors.BLUE_GREY_800,
        'tooltip_padding': 10,
        'tooltip_margin': 10
    }

    # ========== Componentes para Diagnósticos Frecuentes ==========
    diagnosticos_frecuentes_chart = ft.BarChart(
        bar_groups=[],
        border=ft.border.all(1, ft.colors.GREY_400),
        left_axis=ft.ChartAxis(labels_size=40),
        bottom_axis=ft.ChartAxis(labels_size=40),
        interactive=True,
        expand=True,
        **tooltip_config
    )
    
    fecha_inicio_picker = ft.DatePicker(
        first_date=datetime.now() - timedelta(days=365*2),
        last_date=datetime.now(),
    )
    
    fecha_fin_picker = ft.DatePicker(
        first_date=datetime.now() - timedelta(days=365*2),
        last_date=datetime.now(),
    )
    
    page.overlay.extend([fecha_inicio_picker, fecha_fin_picker])
    
    def abrir_selector_inicio(e):
        fecha_inicio_picker.open = True
        page.update()
    
    def abrir_selector_fin(e):
        fecha_fin_picker.open = True
        page.update()
    
    selector_fechas = ft.Row(
        [
            ft.ElevatedButton(
                "Fecha Inicio",
                icon=ft.icons.CALENDAR_MONTH,
                on_click=abrir_selector_inicio,
            ),
            ft.ElevatedButton(
                "Fecha Fin",
                icon=ft.icons.CALENDAR_MONTH,
                on_click=abrir_selector_fin,
            )
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START
    )
    
    # ========== Componentes para Distribución por Sexo ==========
    distribucion_sexo_chart = ft.PieChart(
        sections=[],
        sections_space=0,
        center_space_radius=60,
        expand=True,
    )
    
    # ========== Componentes para Tendencias Temporales ==========
    tendencias_temporales_chart = ft.BarChart(
        bar_groups=[],
        border=ft.border.all(1, ft.colors.GREY_400),
        left_axis=ft.ChartAxis(labels_size=40),
        bottom_axis=ft.ChartAxis(
            labels_size=40,
            labels=[
                ft.ChartAxisLabel(
                    value=i,
                    label=ft.Text(periodo, size=10),
                )
                for i, periodo in enumerate([])
            ]
        ),
        interactive=True,
        expand=True,
        **tooltip_config
    )
    
    tendencias_cie_dropdown = ft.Dropdown(
        label="Diagnóstico (CIE)",
        options=[ft.dropdown.Option("", "Todos los diagnósticos")] + [
            ft.dropdown.Option(
                cie, 
                f"{cie} - {cie_dict.get(cie, 'Descripción no disponible')[:30]}..."
            ) for cie in cie_disponibles
        ],
        value="",
        width=350,
    )
    
    # ========== Componentes para Pacientes Diagnosticados ==========
    actividad_chart = ft.BarChart(
        bar_groups=[],
        border=ft.border.all(1, ft.colors.GREY_400),
        left_axis=ft.ChartAxis(labels_size=40),
        bottom_axis=ft.ChartAxis(
            labels_size=40,
            labels=[
                ft.ChartAxisLabel(
                    value=i,
                    label=ft.Text("", size=10),
                )
                for i in range(0)
            ]
        ),
        interactive=True,
        expand=True,
        **tooltip_config
    )
    
    # Selectores de fecha para Pacientes Diagnosticados
    actividad_fecha_inicio_picker = ft.DatePicker(
        first_date=datetime.now() - timedelta(days=365*2),
        last_date=datetime.now(),
    )
    
    actividad_fecha_fin_picker = ft.DatePicker(
        first_date=datetime.now() - timedelta(days=365*2),
        last_date=datetime.now(),
    )
    
    page.overlay.extend([actividad_fecha_inicio_picker, actividad_fecha_fin_picker])
    
    def abrir_selector_actividad_inicio(e):
        actividad_fecha_inicio_picker.open = True
        page.update()
    
    def abrir_selector_actividad_fin(e):
        actividad_fecha_fin_picker.open = True
        page.update()
    
    actividad_selector_fechas = ft.Row(
        [
            ft.ElevatedButton(
                "Fecha Inicio",
                icon=ft.icons.CALENDAR_MONTH,
                on_click=abrir_selector_actividad_inicio,
            ),
            ft.ElevatedButton(
                "Fecha Fin",
                icon=ft.icons.CALENDAR_MONTH,
                on_click=abrir_selector_actividad_fin,
            )
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START
    )
    
    # ========== Componentes para Prescripciones Frecuentes ==========
    prescripciones_chart = ft.BarChart(
        bar_groups=[],
        border=ft.border.all(1, ft.colors.GREY_400),
        left_axis=ft.ChartAxis(labels_size=40),
        bottom_axis=ft.ChartAxis(labels_size=40),
        interactive=True,
        expand=True,
        **tooltip_config
    )
    
    return {
        # Diagnósticos frecuentes
        "diagnosticos_frecuentes_chart": diagnosticos_frecuentes_chart,
        "selector_fechas": selector_fechas,
        "fecha_inicio_picker": fecha_inicio_picker,
        "fecha_fin_picker": fecha_fin_picker,
        
        # Distribución por sexo
        "distribucion_sexo_chart": distribucion_sexo_chart,
        
        # Tendencias temporales
        "tendencias_temporales_chart": tendencias_temporales_chart,
        "tendencias_cie_dropdown": tendencias_cie_dropdown,
        
        # Pacientes diagnosticados (actividad clínica)
        "actividad_chart": actividad_chart,
        "actividad_selector_fechas": actividad_selector_fechas,
        "actividad_fecha_inicio_picker": actividad_fecha_inicio_picker,
        "actividad_fecha_fin_picker": actividad_fecha_fin_picker,
        
        # Prescripciones frecuentes
        "prescripciones_chart": prescripciones_chart,
        
        # Diccionario CIE
        "cie_dict": cie_dict,
    }