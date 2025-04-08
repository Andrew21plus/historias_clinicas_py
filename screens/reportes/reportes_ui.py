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

    # Componentes para reporte de diagnósticos frecuentes
    diagnosticos_frecuentes_chart = ft.BarChart(
        bar_groups=[],
        border=ft.border.all(1, ft.colors.GREY_400),
        left_axis=ft.ChartAxis(labels_size=40),
        bottom_axis=ft.ChartAxis(labels_size=40),
        interactive=True,
        expand=True,
        **tooltip_config
    )
    
    # Selector de rango de fechas para diagnósticos frecuentes
    fecha_inicio_picker = ft.DatePicker(
        first_date=datetime.now() - timedelta(days=365*2),
        last_date=datetime.now(),
    )
    
    fecha_fin_picker = ft.DatePicker(
        first_date=datetime.now() - timedelta(days=365*2),
        last_date=datetime.now(),
    )
    
    # Añadir los datepickers al overlay de la página
    page.overlay.extend([fecha_inicio_picker, fecha_fin_picker])
    
    def abrir_selector_inicio(e):
        fecha_inicio_picker.open = True
        page.update()
    
    def abrir_selector_fin(e):
        fecha_fin_picker.open = True
        page.update()
    
    # Controles de selección de fechas (simplificado sin texto de rango)
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
    
    # Componentes para reporte de distribución por sexo
    distribucion_sexo_chart = ft.PieChart(
        sections=[],
        sections_space=0,
        center_space_radius=60,
        expand=True,
    )
    
    # Componentes para reporte de tendencias temporales
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
    
    # Dropdown de CIE
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
    
    # Componentes para reporte de pacientes diagnosticados
    actividad_periodo_dropdown = ft.Dropdown(
        label="Agrupación temporal",
        options=[
            ft.dropdown.Option("day", "Día"),
            ft.dropdown.Option("week", "Semana"),
            ft.dropdown.Option("month", "Mes"),
        ],
        value="month",
        width=150,
    )
    
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
    
    # Componentes para reporte de prescripciones
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
        "diagnosticos_frecuentes_chart": diagnosticos_frecuentes_chart,
        "selector_fechas": selector_fechas,
        "fecha_inicio_picker": fecha_inicio_picker,
        "fecha_fin_picker": fecha_fin_picker,
        "distribucion_sexo_chart": distribucion_sexo_chart,
        "tendencias_temporales_chart": tendencias_temporales_chart,
        "tendencias_cie_dropdown": tendencias_cie_dropdown,
        "actividad_periodo_dropdown": actividad_periodo_dropdown,
        "actividad_chart": actividad_chart,
        "prescripciones_chart": prescripciones_chart,
        "cie_dict": cie_dict,
    }