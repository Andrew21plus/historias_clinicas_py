import flet as ft
from .reportes_crud import (
    obtener_diagnosticos_frecuentes,
    obtener_distribucion_sexo,
    obtener_tendencias_temporales,
    obtener_pacientes_diagnosticados_por_periodo,
    obtener_prescripciones_frecuentes,
    obtener_periodos_disponibles,
    obtener_cie_disponibles
)
from .reportes_ui import crear_reportes_ui

def ReportesScreen(page: ft.Page, id_usuario: int):
    """Pantalla de Reportes Clínicos con todas las mejoras"""
    
    # Crear componentes de UI
    ui = crear_reportes_ui(page, id_usuario)
    cie_dict = ui["cie_dict"]
    
    # Obtener referencias a los componentes
    diagnosticos_frecuentes_chart = ui["diagnosticos_frecuentes_chart"]
    diagnosticos_frecuentes_dropdown = ui["diagnosticos_frecuentes_dropdown"]
    distribucion_sexo_chart = ui["distribucion_sexo_chart"]
    tendencias_temporales_chart = ui["tendencias_temporales_chart"]
    tendencias_cie_dropdown = ui["tendencias_cie_dropdown"]
    actividad_periodo_dropdown = ui["actividad_periodo_dropdown"]
    actividad_chart = ui["actividad_chart"]
    prescripciones_chart = ui["prescripciones_chart"]

    def cargar_diagnosticos_frecuentes(e=None):
        """Carga diagnósticos frecuentes"""
        periodo = diagnosticos_frecuentes_dropdown.value if diagnosticos_frecuentes_dropdown.value != "all" else None
        datos = obtener_diagnosticos_frecuentes(id_usuario, periodo=periodo)
        
        colors = [
            ft.colors.BLUE_400,
            ft.colors.INDIGO_400,
            ft.colors.TEAL_400,
            ft.colors.CYAN_400,
            ft.colors.LIGHT_BLUE_400
        ]
        
        diagnosticos_frecuentes_chart.bar_groups = [
            ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=item[2],
                        width=25,
                        color=colors[i % len(colors)],
                        tooltip=f"Código: {item[0]}\n"
                               f"Descripción: {cie_dict.get(item[0], 'No disponible')}\n"
                               f"Frecuencia: {item[2]}\n"
                               f"Período: {periodo if periodo else 'Todos'}",
                        border_radius=4,
                    )
                ],
            )
            for i, item in enumerate(datos[:10])
        ]
        
        diagnosticos_frecuentes_chart.bottom_axis.labels = [
            ft.ChartAxisLabel(
                value=i,
                label=ft.Container(
                    content=ft.Text(
                        f"{item[0]}\n({item[2]})", 
                        size=10, 
                        color=ft.colors.BLACK,
                        text_align=ft.TextAlign.CENTER
                    ),
                    width=80,
                ),
            )
            for i, item in enumerate(datos[:10])
        ]
        
        page.update()

    def cargar_distribucion_sexo(e=None):
        """Distribución por sexo con etiquetas externas"""
        datos = obtener_distribucion_sexo(id_usuario)
        total = sum(count for sexo, count in datos) or 1  # Evitar división por cero
        
        # Configurar gráfico sin etiquetas internas
        distribucion_sexo_chart.sections = [
            ft.PieChartSection(
                value=count,
                title="",
                color=(
                    ft.colors.BLUE_600 if sexo == 'M' else 
                    ft.colors.PINK_600 if sexo == 'F' else 
                    ft.colors.GREEN_600
                ),
                radius=60,
            )
            for sexo, count in datos if count > 0
        ]
        
        # Crear leyenda externa mejorada
        leyenda = ft.Row(
            [
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            width=20,
                            height=20,
                            bgcolor=(
                                ft.colors.BLUE_600 if sexo == 'M' else 
                                ft.colors.PINK_600 if sexo == 'F' else 
                                ft.colors.GREEN_600
                            ),
                            border_radius=4,
                            margin=ft.margin.only(right=5)
                        ),
                        ft.Text(
                            f"{sexo}: {count} ({count/total:.1%})", 
                            size=12,
                            weight=ft.FontWeight.BOLD
                        )
                    ]),
                    padding=5,
                    border_radius=5,
                    bgcolor=ft.colors.GREY_100,
                    margin=5
                )
                for sexo, count in datos if count > 0
            ],
            wrap=True,
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        # Actualizar o crear leyenda
        if not hasattr(page, 'leyenda_sexo'):
            page.leyenda_sexo = leyenda
        else:
            page.leyenda_sexo.controls = leyenda.controls
        
        page.update()

    def cargar_tendencias_temporales(e=None):
        """Tendencias con variación porcentual"""
        codigo_cie = tendencias_cie_dropdown.value if tendencias_cie_dropdown.value else None
        datos, variaciones = obtener_tendencias_temporales(id_usuario, codigo_cie)
        descripcion = cie_dict.get(codigo_cie, "Todos los diagnósticos") if codigo_cie else "Todos los diagnósticos"
        
        tendencias_temporales_chart.bar_groups = [
            ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=item[1],
                        width=20,
                        color=ft.colors.GREEN_400 if variaciones[i] >= 0 else ft.colors.RED_400,
                        tooltip=f"Período: {item[0]}\n"
                               f"Diagnóstico: {descripcion}\n"
                               f"Casos: {item[1]}\n"
                               f"Variación: {'+' if variaciones[i] >=0 else ''}{variaciones[i]:.1f}%",
                        border_radius=4,
                    )
                ],
            )
            for i, item in enumerate(datos[-12:])
        ]
        
        tendencias_temporales_chart.bottom_axis.labels = [
            ft.ChartAxisLabel(
                value=i,
                label=ft.Text(
                    item[0].split('-')[1],
                    size=10,
                    color=ft.colors.BLACK
                ),
            )
            for i, item in enumerate(datos[-12:])
        ]
        
        page.update()

    def cargar_pacientes_diagnosticados(e=None):
        """Pacientes diagnosticados por período corregido"""
        periodo = actividad_periodo_dropdown.value
        datos = obtener_pacientes_diagnosticados_por_periodo(id_usuario, periodo)
        
        if not datos:
            actividad_chart.content = ft.Text("No hay datos disponibles", size=16)
            page.update()
            return
            
        # Configurar colores
        color = ft.colors.BLUE_400
        
        actividad_chart.bar_groups = [
            ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=item[1],
                        width=25,
                        color=color,
                        tooltip=f"Período: {item[0]}\n"
                               f"Pacientes únicos: {item[1]}",
                        border_radius=4,
                    )
                ],
            )
            for i, item in enumerate(datos[-12:])
        ]
        
        # Configurar etiquetas del eje X
        actividad_chart.bottom_axis.labels = [
            ft.ChartAxisLabel(
                value=i,
                label=ft.Container(
                    content=ft.Text(
                        item[0].split('-')[1] if periodo == 'month' else item[0][-2:],
                        size=10,
                        color=ft.colors.BLACK
                    ),
                    width=60,
                    alignment=ft.alignment.center,
                ),
            )
            for i, item in enumerate(datos[-12:])
        ]
        
        page.update()

    def cargar_prescripciones(e=None):
        """Prescripciones frecuentes"""
        datos = obtener_prescripciones_frecuentes(id_usuario)
        
        prescripciones_chart.bar_groups = [
            ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=item[1],
                        width=20,
                        color=ft.colors.ORANGE_400,
                        tooltip=f"Medicamento: {item[0]}\nRecetas: {item[1]}",
                        border_radius=4,
                    ),
                ],
            )
            for i, item in enumerate(datos[:12])
        ]
        
        prescripciones_chart.bottom_axis.labels = [
            ft.ChartAxisLabel(
                value=i,
                label=ft.Container(
                    content=ft.Text(
                        item[0].split()[0][:10],
                        size=9,
                        color=ft.colors.BLACK,
                        weight=ft.FontWeight.BOLD
                    ),
                    width=80,
                    alignment=ft.alignment.center,
                ),
            )
            for i, item in enumerate(datos[:12])
        ]
        
        page.update()

    # Configurar eventos
    diagnosticos_frecuentes_dropdown.on_change = cargar_diagnosticos_frecuentes
    tendencias_cie_dropdown.on_change = cargar_tendencias_temporales
    actividad_periodo_dropdown.on_change = cargar_pacientes_diagnosticados
    
    # Cargar datos iniciales
    cargar_diagnosticos_frecuentes()
    cargar_distribucion_sexo()
    cargar_tendencias_temporales()
    cargar_pacientes_diagnosticados()
    cargar_prescripciones()
    
    # Diseño de pestañas
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Epidemiológicos",
                content=ft.Column(
                    [
                        ft.Text("Diagnósticos más frecuentes", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row([diagnosticos_frecuentes_dropdown], alignment=ft.MainAxisAlignment.END),
                        ft.Container(diagnosticos_frecuentes_chart, height=300),
                        
                        ft.Divider(),
                        
                        ft.Text("Distribución por sexo", size=18, weight=ft.FontWeight.BOLD),
                        ft.Column([
                            ft.Container(distribucion_sexo_chart, height=250),
                            page.leyenda_sexo if hasattr(page, 'leyenda_sexo') else ft.Container()
                        ], spacing=10),
                        
                        ft.Divider(),
                        
                        ft.Text("Tendencias temporales", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row([tendencias_cie_dropdown], alignment=ft.MainAxisAlignment.END),
                        ft.Container(tendencias_temporales_chart, height=300),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
            ft.Tab(
                text="Actividad Clínica",
                content=ft.Column(
                    [
                        ft.Text("Pacientes diagnosticados por período", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row([actividad_periodo_dropdown], alignment=ft.MainAxisAlignment.END),
                        ft.Container(actividad_chart, height=300),
                        
                        ft.Divider(),
                        
                        ft.Text("Prescripciones frecuentes", size=18, weight=ft.FontWeight.BOLD),
                        ft.Container(prescripciones_chart, height=300),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
        ],
        expand=True,
    )
    
    return ft.Column(
        [
            ft.Text("Reportes Clínicos", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(height=10),
            tabs,
        ],
        expand=True,
    )