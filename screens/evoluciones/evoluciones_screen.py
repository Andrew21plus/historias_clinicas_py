import flet as ft
import time
from .evoluciones_crud import (
    obtener_historias_clinicas,
    actualizar_historia_clinica,
    obtener_antecedentes_paciente,
    obtener_signos_vitales_paciente,
    obtener_diagnosticos_por_consulta,
    obtener_prescripciones_por_consulta,
    obtener_tratamientos_por_consulta,
    obtener_evoluciones_por_consulta,
    obtener_signos_hoy,
    obtener_cie,
    guardar_signos_vitales,
    guardar_diagnostico,
    guardar_prescripcion,
    guardar_tratamiento,
)
from services.paciente_service import get_paciente
from datetime import datetime
from .evoluciones_ui import crear_evoluciones_ui


def EvolucionesScreen(page: ft.Page, id_usuario: int):
    current_page = 0
    pacientes_per_page = 5
    search_query = ""
    all_historias = []
    selected_historia = None

    def show_alert(message):
        alert_dialog.content = ft.Text(message)
        alert_dialog.open = True
        page.update()

    def build_antecedentes_section(id_paciente):
        antecedentes = obtener_antecedentes_paciente(id_paciente, id_usuario)
        if not antecedentes:
            return ft.Container()

        return ft.ExpansionTile(
            title=ft.Text(
                "📋 ANTECEDENTES MÉDICOS",
                weight=ft.FontWeight.BOLD,
                color=ft.colors.PURPLE_700,
            ),
            controls=[
                ft.Column(
                    [
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text("🩺 Tipo:", weight=ft.FontWeight.BOLD),
                                        ft.Text(ant.tipo),
                                    ],
                                    spacing=5,
                                ),
                                ft.Row(
                                    [
                                        ft.Text(
                                            "📝 Descripción:", weight=ft.FontWeight.BOLD
                                        ),
                                        ft.Text(ant.descripcion),
                                    ],
                                    spacing=5,
                                ),
                                ft.Divider(),
                            ],
                            spacing=5,
                        )
                        for ant in antecedentes
                    ],
                    spacing=10,
                )
            ],
            initially_expanded=False,
        )

    def build_evolucion_section(id_paciente):
        signos = obtener_signos_vitales_paciente(id_paciente, id_usuario)
        if not signos:
            return ft.Container()

        # Agrupar por fecha
        consultas_por_fecha = {}
        for signo in signos:
            fecha_consulta = signo.fecha
            if fecha_consulta not in consultas_por_fecha:
                consultas_por_fecha[fecha_consulta] = {
                    "signos_vitales": signo,
                    "diagnosticos": obtener_diagnosticos_por_consulta(
                        id_paciente, fecha_consulta
                    )
                    or [],
                    "prescripciones": obtener_prescripciones_por_consulta(
                        id_paciente, fecha_consulta
                    )
                    or [],
                    "tratamientos": obtener_tratamientos_por_consulta(
                        id_paciente, fecha_consulta
                    )
                    or [],
                    "evoluciones": obtener_evoluciones_por_consulta(
                        id_paciente, fecha_consulta
                    )
                    or [],
                }

        # Construir la UI para cada consulta
        consultas_ui = []
        for fecha, consulta in sorted(consultas_por_fecha.items(), reverse=True):
            # Sección de Signos Vitales
            signos_ui = (
                ft.ExpansionTile(
                    title=ft.Text(
                        "🩺 SIGNOS VITALES",
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.RED_700,
                    ),
                    controls=[
                        ft.DataTable(
                            column_spacing=20,
                            columns=[
                                ft.DataColumn(
                                    ft.Text(
                                        "PARÁMETRO", weight=ft.FontWeight.BOLD, size=14
                                    )
                                ),
                                ft.DataColumn(
                                    ft.Text("VALOR", weight=ft.FontWeight.BOLD, size=14)
                                ),
                                ft.DataColumn(
                                    ft.Text(
                                        "UNIDAD", weight=ft.FontWeight.BOLD, size=14
                                    )
                                ),
                            ],
                            rows=[
                                # Presión Arterial
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(
                                            ft.Text("Presión Arterial", size=12)
                                        ),
                                        ft.DataCell(
                                            ft.Text(
                                                consulta[
                                                    "signos_vitales"
                                                ].presion_arterial
                                                if consulta[
                                                    "signos_vitales"
                                                ].presion_arterial
                                                else "No registrado"
                                            )
                                        ),
                                        ft.DataCell(ft.Text("mmHg")),
                                    ],
                                    color=ft.colors.GREY_100,
                                ),
                                # Frecuencia Cardíaca
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(
                                            ft.Text("Frecuencia Cardíaca", size=12)
                                        ),
                                        ft.DataCell(
                                            ft.Text(
                                                str(
                                                    consulta[
                                                        "signos_vitales"
                                                    ].frecuencia_cardiaca
                                                )
                                                if consulta[
                                                    "signos_vitales"
                                                ].frecuencia_cardiaca
                                                is not None
                                                else "No registrado"
                                            )
                                        ),
                                        ft.DataCell(ft.Text("lpm")),
                                    ]
                                ),
                                # Frecuencia Respiratoria
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(
                                            ft.Text("Frecuencia Respiratoria", size=12)
                                        ),
                                        ft.DataCell(
                                            ft.Text(
                                                str(
                                                    consulta[
                                                        "signos_vitales"
                                                    ].frecuencia_respiratoria
                                                )
                                                if consulta[
                                                    "signos_vitales"
                                                ].frecuencia_respiratoria
                                                is not None
                                                else "No registrado"
                                            )
                                        ),
                                        ft.DataCell(ft.Text("rpm")),
                                    ],
                                    color=ft.colors.GREY_100,
                                ),
                                # Temperatura
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text("Temperatura", size=12)),
                                        ft.DataCell(
                                            ft.Text(
                                                f"{consulta['signos_vitales'].temperatura:.1f}"
                                                if consulta[
                                                    "signos_vitales"
                                                ].temperatura
                                                is not None
                                                else "No registrado"
                                            )
                                        ),
                                        ft.DataCell(ft.Text("°C")),
                                    ]
                                ),
                                # Peso
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text("Peso", size=12)),
                                        ft.DataCell(
                                            ft.Text(
                                                f"{consulta['signos_vitales'].peso:.1f}"
                                                if consulta["signos_vitales"].peso
                                                is not None
                                                else "No registrado"
                                            )
                                        ),
                                        ft.DataCell(ft.Text("kg")),
                                    ],
                                    color=ft.colors.GREY_100,
                                ),
                                # Talla
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text("Talla", size=12)),
                                        ft.DataCell(
                                            ft.Text(
                                                f"{consulta['signos_vitales'].talla:.0f}"
                                                if consulta["signos_vitales"].talla
                                                is not None
                                                else "No registrado"
                                            )
                                        ),
                                        ft.DataCell(ft.Text("cm")),
                                    ]
                                ),
                                # IMC (calculado)
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(
                                            ft.Text(
                                                "IMC",
                                                size=12,
                                                weight=ft.FontWeight.BOLD,
                                            )
                                        ),
                                        ft.DataCell(
                                            ft.Text(
                                                f"{(consulta['signos_vitales'].peso / ((consulta['signos_vitales'].talla/100) ** 2)):.1f}"
                                                if consulta["signos_vitales"].peso
                                                and consulta["signos_vitales"].talla
                                                else "No calculable"
                                            )
                                        ),
                                        ft.DataCell(ft.Text("kg/m²")),
                                    ],
                                    color=ft.colors.GREY_100,
                                ),
                            ],
                            border=ft.border.all(1, ft.colors.GREY_300),
                            border_radius=10,
                            horizontal_lines=ft.border.BorderSide(
                                1, ft.colors.GREY_200
                            ),
                            vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_200),
                        )
                    ],
                    initially_expanded=True,
                )
                if consulta.get("signos_vitales")
                else None
            )

            # Sección de Diagnósticos
            diagnosticos_ui = (
                ft.ExpansionTile(
                    title=ft.Text(
                        "📋 DIAGNÓSTICOS",
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.PURPLE_700,
                    ),
                    controls=[
                        ft.Column(
                            [
                                ft.ListTile(
                                    title=ft.Text(diag.diagnostico),
                                    subtitle=ft.Text(
                                        f"CIE-10: {diag.cie or 'No especificado'}"
                                    ),
                                    trailing=ft.Text(
                                        (
                                            "DEFINITIVO"
                                            if diag.definitivo
                                            else "PRESUNTIVO"
                                        ),
                                        color=(
                                            ft.colors.GREEN
                                            if diag.definitivo
                                            else ft.colors.ORANGE
                                        ),
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                )
                                for diag in consulta.get("diagnosticos", [])
                            ],
                            spacing=5,
                        )
                    ],
                    initially_expanded=False,
                )
                if consulta.get("diagnosticos")
                else None
            )

            # Sección de Prescripciones
            prescripciones_ui = (
                ft.ExpansionTile(
                    title=ft.Text(
                        "💊 PRESCRIPCIONES",
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.TEAL_700,
                    ),
                    controls=[
                        ft.Column(
                            [
                                ft.ListTile(
                                    leading=ft.Icon(ft.icons.MEDICATION),
                                    title=ft.Text(
                                        f"{presc.medicamento} - {presc.dosis}"
                                    ),
                                    subtitle=ft.Text(
                                        presc.indicaciones or "Sin indicaciones"
                                    ),
                                    trailing=ft.Text(f"Firmado: {presc.firmado_por}"),
                                )
                                for presc in consulta.get("prescripciones", [])
                            ],
                            spacing=5,
                        )
                    ],
                    initially_expanded=False,
                )
                if consulta.get("prescripciones")
                else None
            )

            # Sección de Tratamientos
            tratamientos_ui = (
                ft.ExpansionTile(
                    title=ft.Text(
                        "🩹 TRATAMIENTOS",
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.INDIGO_700,
                    ),
                    controls=[
                        ft.Column(
                            [
                                ft.ListTile(
                                    leading=ft.Icon(ft.icons.HEALING),
                                    title=ft.Text(trat.tratamiento),
                                    # subtitle=ft.Text(trat.observaciones or 'Sin observaciones')
                                )
                                for trat in consulta.get("tratamientos", [])
                            ],
                            spacing=5,
                        )
                    ],
                    initially_expanded=False,
                )
                if consulta.get("tratamientos")
                else None
            )

            # Agregar solo las secciones que tienen contenido
            secciones = [
                s
                for s in [
                    signos_ui,
                    diagnosticos_ui,
                    prescripciones_ui,
                    tratamientos_ui,
                ]
                if s is not None
            ]

            if secciones:
                consultas_ui.append(
                    ft.ExpansionTile(
                        title=ft.Text(
                            f"📅 Consulta del {fecha}", weight=ft.FontWeight.BOLD
                        ),
                        controls=secciones,
                        initially_expanded=False,
                    )
                )

        return ft.ExpansionTile(
            title=ft.Row(
                controls=[
                    ft.Text(
                        "📈 EVOLUCIÓN",
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLUE_700,
                    ),
                    ft.IconButton(
                        icon=ft.icons.ADD,
                        icon_color=ft.colors.GREEN,
                        tooltip="Crear Nueva Consulta",
                        on_click=lambda e, ip=id_paciente, iu=id_usuario: open_create_dialog(
                            ip, iu
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            controls=[ft.Column(consultas_ui, spacing=10)] if consultas_ui else [],
            initially_expanded=False,
        )

    def refresh_pacientes():
        nonlocal all_historias
        pacientes_list.controls.clear()
        all_historias = obtener_historias_clinicas(id_usuario, search_query)

        start_index = current_page * pacientes_per_page
        end_index = start_index + pacientes_per_page

        for historia in all_historias[start_index:end_index]:
            paciente = get_paciente(historia.id_paciente)
            if paciente:
                paciente_nombre = paciente.nombre
                paciente_apellido = paciente.apellido
                paciente_sexo = paciente.sexo
                paciente_fecha_nacimiento = paciente.fecha_nacimiento
                paciente_historia_clinica = paciente.num_historia_clinica

                try:
                    fecha_nac = datetime.strptime(paciente_fecha_nacimiento, "%d-%m-%Y")
                    hoy = datetime.now()
                    edad = (
                        hoy.year
                        - fecha_nac.year
                        - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
                    )
                    edad_str = f"{edad} años"
                except:
                    edad_str = "Fecha inválida"
            else:
                paciente_nombre = "Desconocido"
                paciente_apellido = ""
                paciente_sexo = ""
                paciente_fecha_nacimiento = ""
                paciente_historia_clinica = ""
                edad_str = ""

            # Contenido expandible
            contenido = ft.Column(
                [
                    # Sección de Historia Clínica con botón de edición
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(
                                                "📋 Motivo:", weight=ft.FontWeight.BOLD
                                            ),
                                            ft.Text(historia.motivo_consulta),
                                        ],
                                        spacing=5,
                                    ),
                                    ft.Row(
                                        [
                                            ft.Text(
                                                "🤒 Enfermedad:",
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            ft.Text(historia.enfermedad_actual),
                                        ],
                                        spacing=5,
                                    ),
                                ],
                                expand=True,
                            ),
                            ft.IconButton(
                                ft.icons.EDIT,
                                icon_color=ft.colors.BLUE,
                                tooltip="Editar historia",
                                on_click=lambda e, h=historia: open_edit_dialog(h),
                            ),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    # Sección de Antecedentes Médicos
                    build_antecedentes_section(historia.id_paciente),
                    # Sección de Evolución (que contiene todo lo demás por fecha)
                    build_evolucion_section(historia.id_paciente),
                ],
                spacing=10,
            )

            # Crear la tarjeta principal con ExpansionTile
            paciente_card = ft.Card(
                content=ft.Container(
                    content=ft.ExpansionTile(
                        title=ft.Row(
                            [
                                ft.Text(
                                    f"👤 {paciente_nombre} {paciente_apellido}",
                                    weight=ft.FontWeight.BOLD,
                                    expand=True,
                                ),
                                ft.Text(f"⚥ {paciente_sexo}"),
                                ft.Text(f"🔢 {edad_str}"),
                                ft.Text(f"🏥 {paciente_historia_clinica}"),
                            ],
                            spacing=10,
                        ),
                        controls=[contenido],
                    ),
                    padding=ft.padding.symmetric(vertical=10, horizontal=15),
                ),
                elevation=3,
                margin=ft.margin.symmetric(vertical=5),
                width=page.window_width * 0.95,  # type: ignore
            )
            pacientes_list.controls.append(paciente_card)

        # Actualizar controles de paginación
        pagination_controls.controls[0].disabled = current_page == 0
        pagination_controls.controls[2].disabled = len(all_historias) <= end_index
        page.update()

    def open_edit_dialog(historia):
        nonlocal selected_historia
        selected_historia = historia
        edit_id.value = historia.id_historia
        edit_paciente.value = historia.id_paciente
        edit_motivo.value = historia.motivo_consulta
        edit_enfermedad.value = historia.enfermedad_actual
        edit_dialog.open = True
        page.update()

    def save_edit(e):
        try:
            actualizar_historia_clinica(
                edit_id.value, edit_motivo.value, edit_enfermedad.value, id_usuario
            )
            edit_dialog.open = False
            refresh_pacientes()
            page.update()
        except Exception as e:
            show_alert(f"Error al actualizar: {str(e)}")

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111
    def open_create_dialog(id_paciente, id_usuario):
        print(f"[evidencias_screen] open_create_dialog id_usuario: {id_usuario}")
        try:
            # Obtener datos del paciente
            paciente = get_paciente(id_paciente)
            if not paciente:
                show_alert("No se encontró el paciente")
                return

            # Configurar diálogo de nueva consulta
            new_consult_paciente_info.value = f"{paciente.nombre} {paciente.apellido} - {paciente.num_historia_clinica}"
            new_consult_paciente_id.value = id_paciente
            new_consult_paciente_nombre.value = f"{paciente.nombre} {paciente.apellido}"

            # Verificar si hay signos vitales hoy
            signos_hoy = obtener_signos_hoy(id_paciente, id_usuario)
            print(f"[evoluciones_screen] signos_hoy: {signos_hoy}")
            if signos_hoy is not None:
                # Autocompletar con valores existentes
                # signos_presion.value = getattr(signos_hoy, "presion_arterial", "") or ""
                signos_presion.value = signos_hoy.presion_arterial or ""
                signos_frec_cardiaca.value = signos_hoy.frecuencia_cardiaca or ""
                signos_frec_respi.value = signos_hoy.frecuencia_respiratoria or ""
                signos_temp.value = signos_hoy.temperatura or ""
                signos_peso.value = signos_hoy.peso or ""
                signos_talla.value = signos_hoy.talla or ""
            else:
                # Limpiar campos para llenar manualmente
                signos_presion.value = ""
                signos_frec_cardiaca.value = ""
                signos_frec_respi.value = ""
                signos_temp.value = ""
                signos_peso.value = ""
                signos_talla.value = ""

            # Abrir primer diálogo
            open_signos_dialog()
            page.update()

        except Exception as ex:
            show_alert(f"Error al abrir formulario: {str(ex)}")

    def open_signos_dialog():
        close_all_dialogs()
        signos_dialog.open = True
        page.update()

    def open_diagnostico_dialog():
        # Validar signos vitales primero si es necesario
        if (
            not signos_presion.value
            or not signos_frec_cardiaca.value
            or not signos_frec_respi.value
            or not signos_temp.value
            or not signos_peso.value
            or not signos_talla.value
        ):
            show_alert("Es necesario que se llenen todos los campos de signos vitales")
            time.sleep(1)
            open_signos_dialog()
            return

        close_all_dialogs()
        diagnostico_dialog.open = True
        page.update()

    def open_prescripciones_dialog():
        # Validar diagnóstico primero
        if not diagnostico_cie.value:
            show_alert("El código CIE es obligatorio")
            time.sleep(1)
            open_diagnostico_dialog()
            return

        presc_fecha.value = datetime.now().strftime("%Y-%m-%d")

        close_all_dialogs()
        prescripciones_dialog.open = True
        page.update()

    def open_tratamientos_dialog():
        if (
            not presc_medicamento.value
            or not presc_dosis.value
            or not presc_indicaciones.value
            or not presc_firmado_por.value
        ):
            show_alert("Es necesario llenar todos los campos de la prescripción")
            time.sleep(1)
            open_prescripciones_dialog()
            return

        close_all_dialogs()
        tratamiento_fecha.value = datetime.now().strftime("%Y-%m-%d")
        tratamientos_dialog.open = True
        page.update()

    def save_full_consultation(e):
        if not tratamiento_descripcion.value:
            show_alert("El campo de tratamiento es obligatorio")
            time.sleep(1)
            open_tratamientos_dialog()
            return

        # Esta función se llamará al final para guardar todo
        try:
            # 1. Guardar signos vitales
            result_signos_vitales = guardar_signos_vitales(
                {
                    "id_paciente": new_consult_paciente_id.value,
                    "presion": signos_presion.value,
                    "frecuencia_cardiaca": signos_frec_cardiaca.value,
                    "frecuencia_respiratoria": signos_frec_respi.value,
                    "temperatura": signos_temp.value,
                    "peso": signos_peso.value,
                    "talla": signos_talla.value,
                }
            )

            # 2. Guardar diagnóstico
            result_diagnostico = guardar_diagnostico(
                {
                    "id_paciente": new_consult_paciente_id.value,
                    "id_usuario": id_usuario,
                    "codigo_cie": diagnostico_cie.value,
                    "descripcion_cie": diagnostico_cie_descripcion.value,
                }
            )

            # 3. Guardar prescripciones
            result_prescripcion = guardar_prescripcion(
                {
                    "id_paciente": new_consult_paciente_id.value,
                    "id_usuario": id_usuario,
                    "medicamento": presc_medicamento.value,
                    "dosis": presc_dosis.value,
                    "indicaciones": presc_indicaciones.value,
                    "firmado_por": presc_firmado_por.value,
                    "fecha": presc_fecha.value,
                }
            )

            # 4. Guardar tratamientos
            result_tratamiento = guardar_tratamiento(
                {
                    "id_paciente": new_consult_paciente_id.value,
                    "id_usuario": id_usuario,
                    "descripcion": tratamiento_descripcion.value,
                    "fecha": tratamiento_fecha.value,
                }
            )

            show_alert("Consulta completa guardada exitosamente")
            close_all_dialogs()
            refresh_pacientes()

        except Exception as e:
            show_alert(f"Error al guardar: {str(e)}")

    # Función para cerrar todos los diálogos
    def close_all_dialogs(e=None):
        signos_dialog.open = False
        diagnostico_dialog.open = False
        prescripciones_dialog.open = False
        tratamientos_dialog.open = False

        # Limpiar todos los valores
        # signos_presion.value = ""
        # signos_frec_cardiaca.value = ""
        # signos_frec_respi.value = ""
        # signos_temp.value = ""
        # signos_peso.value = ""
        # signos_talla.value = ""

        page.update()

    def change_page(delta):
        nonlocal current_page
        current_page += delta
        if current_page < 0:
            current_page = 0
        max_pages = max(
            1, (len(all_historias) + pacientes_per_page - 1) // pacientes_per_page
        )
        if current_page >= max_pages:
            current_page = max_pages - 1
        page_number_text.value = f"Página {current_page + 1}"
        refresh_pacientes()

    def on_search(e):
        nonlocal search_query, current_page
        search_query = e.control.value if hasattr(e, "control") else e
        current_page = 0
        page_number_text.value = f"Página {current_page + 1}"
        refresh_pacientes()

    def on_search_cie(e):
        search_query = e.control.value
        refresh_cie(search_query)

    def refresh_cie(search_query=""):
        """Actualiza la lista de CIE según búsqueda"""
        cie_list.controls.clear()

        resultados = obtener_cie(search_query)  # Usa la función del CRUD

        if not resultados:
            cie_list.controls.append(
                ft.ListTile(
                    title=ft.Text("No se encontraron resultados"),
                    leading=ft.Icon(ft.icons.WARNING),
                )
            )
        else:
            for cie in resultados:
                cie_list.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.MEDICAL_SERVICES),
                        title=ft.Text(cie["codigo"]),
                        subtitle=ft.Text(cie["descripcion"], max_lines=2),
                        on_click=lambda e, cie=cie: seleccionar_cie(cie),
                    )
                )
        page.update()

    def seleccionar_cie(cie):
        diagnostico_cie_id.value = str(cie["id"])  # Guarda el ID interno
        diagnostico_cie.value = cie["codigo"]
        diagnostico_cie_descripcion.value = cie["descripcion"]
        page.update()

    # UI
    ui = crear_evoluciones_ui(
        page,
        on_search,
        on_search_cie,
        change_page,
        save_edit,
        open_diagnostico_dialog,
        open_prescripciones_dialog,
        open_signos_dialog,
        open_tratamientos_dialog,
        save_full_consultation,
        close_all_dialogs,
    )
    page_number_text = ui["page_number_text"]
    search_field = ui["search_field"]
    pacientes_list = ui["pacientes_list"]
    pagination_controls = ui["pagination_controls"]
    alert_dialog = ui["alert_dialog"]
    edit_id = ui["edit_id"]
    edit_paciente = ui["edit_paciente"]
    edit_motivo = ui["edit_motivo"]
    edit_enfermedad = ui["edit_enfermedad"]
    edit_dialog = ui["edit_dialog"]
    new_consult_paciente_info = ui["new_consult_paciente_info"]
    new_consult_paciente_id = ui["new_consult_paciente_id"]
    new_consult_paciente_nombre = ui["new_consult_paciente_nombre"]
    signos_dialog = ui["signos_dialog"]
    signos_presion = ui["signos_presion"]
    signos_frec_cardiaca = ui["signos_frec_cardiaca"]
    signos_frec_respi = ui["signos_frec_respi"]
    signos_temp = ui["signos_temp"]
    signos_peso = ui["signos_peso"]
    signos_talla = ui["signos_talla"]
    diagnostico_cie_id = ui["diagnostico_cie_id"]
    diagnostico_cie = ui["diagnostico_cie"]
    diagnostico_cie_descripcion = ui["diagnostico_cie_descripcion"]
    cie_list = ui["cie_list"]
    diagnostico_dialog = ui["diagnostico_dialog"]
    presc_medicamento = ui["presc_medicamento"]
    presc_dosis = ui["presc_dosis"]
    presc_indicaciones = ui["presc_indicaciones"]
    presc_firmado_por = ui["presc_firmado_por"]
    presc_fecha = ui["presc_fecha"]
    prescripciones_dialog = ui["prescripciones_dialog"]
    tratamiento_descripcion = ui["tratamiento_descripcion"]
    tratamiento_fecha = ui["tratamiento_fecha"]
    tratamientos_dialog = ui["tratamientos_dialog"]

    refresh_pacientes()

    return ft.Column(
        [
            ft.Text("Evoluciones de Pacientes", size=24, weight=ft.FontWeight.BOLD),
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
            alert_dialog,
            edit_dialog,
            signos_dialog,
            diagnostico_dialog,
            prescripciones_dialog,
            tratamientos_dialog,
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )
