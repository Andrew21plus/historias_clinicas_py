import unicodedata
import flet as ft
from .tamizaje_crud import (
    obtener_tamizajes,
    eliminar_tamizaje,
    agregar_tamizaje,
    agregar_signo_vital,
    actualizar_tamizaje,
    paciente_tiene_tamizaje,
)
from .tamizaje_ui import crear_tamizaje_ui
from utils.formulario_tamizaje import crear_formulario_tamizaje
from services.paciente_service import get_pacientes_by_id_usuario
from services.historia_clinica_service import paciente_tiene_historia


def TamizajeScreen(page: ft.Page, id_usuario: int):
    selected_tamizaje = None  # Variable para almacenar el tamizaje seleccionado
    current_page = 0  # Página actual de la paginación
    tamizajes_per_page = 5  # Número de tamizajes por página
    search_query = ""  # Variable para almacenar la consulta de búsqueda
    all_tamizajes = []  # Lista para almacenar todos los tamizajes

    def show_alert(message):
        """Muestra un diálogo de alerta con el mensaje proporcionado."""
        alert_dialog.content = ft.Text(message)
        alert_dialog.open = True
        page.update()

    def validar_campos_requeridos(campos):
        campos_faltantes = [campo for campo in campos if not campo.value]
        if campos_faltantes:
            show_alert(
                f"Por favor, complete los siguientes campos: {', '.join([campo.label for campo in campos_faltantes])}"
            )
            return False
        return True

    # def confirm_delete(confirmed):
    #     """Maneja la confirmación de eliminación."""
    #     nonlocal selected_tamizaje
    #     confirm_delete_dialog.open = False
    #     page.update()
    #     if confirmed:
    #         remove_tamizaje(selected_tamizaje)
    #     selected_tamizaje = None  # Reiniciar el tamizaje seleccionado

    def remove_tamizaje(paciente):
        """Elimina todos los antecedentes médicos y signos vitales asociados al paciente."""
        eliminar_tamizaje(paciente, id_usuario)  # Usar la función de tamizaje_crud
        refresh_tamizajes()

    def refresh_tamizajes():
        """Actualiza la lista de tamizajes (antecedentes médicos y signos vitales)."""
        nonlocal all_tamizajes
        tamizajes_list.controls.clear()
        all_tamizajes = obtener_tamizajes(
            id_usuario, search_query
        )  # Usar la función de tamizaje_crud

        # Paginación
        start_index = current_page * tamizajes_per_page
        end_index = start_index + tamizajes_per_page

        for tamizaje in all_tamizajes[start_index:end_index]:
            paciente = tamizaje["paciente"]
            antecedentes = tamizaje["antecedentes"]
            signos_vitales = tamizaje["signos_vitales"]

            # Crear la tarjeta expandible
            contenido = ft.Column(spacing=10)

            # Sección de antecedentes médicos
            if antecedentes:
                antecedentes_content = ft.Column(spacing=5)
                for antecedente in antecedentes:
                    antecedentes_content.controls.extend(
                        [
                            ft.Row(
                                [
                                    ft.Text("🩺 Tipo:", weight=ft.FontWeight.BOLD),
                                    ft.Text(antecedente.tipo),
                                ],
                                spacing=5,
                            ),
                            ft.Row(
                                [
                                    ft.Text(
                                        "📝 Descripción:", weight=ft.FontWeight.BOLD
                                    ),
                                    ft.Text(antecedente.descripcion),
                                ],
                                spacing=5,
                            ),
                            ft.Row(
                                [
                                    ft.IconButton(
                                        ft.icons.EDIT,
                                        icon_color=ft.colors.BLUE,
                                        tooltip="Editar antecedente",
                                        on_click=lambda e, t=antecedente: open_edit_dialog(
                                            t
                                        ),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                            ft.Divider(height=10, color=ft.colors.GREY_300),
                        ]
                    )

                # ExpansionTile para antecedentes médicos
                antecedentes_expansion = ft.ExpansionTile(
                    title=ft.Text("📋 Antecedentes Médicos", weight=ft.FontWeight.BOLD),
                    controls=[antecedentes_content],
                )
                contenido.controls.append(antecedentes_expansion)

            # Sección de signos vitales
            if signos_vitales:
                signos_content = ft.Column(spacing=5)
                for signo in signos_vitales:
                    signos_content.controls.extend(
                        [
                            ft.Row(
                                [
                                    ft.Text("📅 Fecha:", weight=ft.FontWeight.BOLD),
                                    ft.Text(signo.fecha),
                                ],
                                spacing=5,
                            ),
                            ft.Row(
                                [
                                    ft.Text(
                                        "🩺 Presión arterial:",
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(signo.presion_arterial),
                                ],
                                spacing=5,
                            ),
                            ft.Row(
                                [
                                    ft.Text(
                                        "❤️ Frecuencia cardíaca:",
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(signo.frecuencia_cardiaca),
                                ],
                                spacing=5,
                            ),
                            ft.Row(
                                [
                                    ft.Text(
                                        "🌬️ Frecuencia respiratoria:",
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(signo.frecuencia_respiratoria),
                                ],
                                spacing=5,
                            ),
                            ft.Row(
                                [
                                    ft.Text(
                                        " 🌡️ Temperatura:", weight=ft.FontWeight.BOLD
                                    ),
                                    ft.Text(signo.temperatura),
                                ],
                                spacing=5,
                            ),
                            ft.Row(
                                [
                                    ft.Text("⚖️ Peso:", weight=ft.FontWeight.BOLD),
                                    ft.Text(signo.peso),
                                ],
                                spacing=5,
                            ),
                            ft.Row(
                                [
                                    ft.Text("📏 Talla:", weight=ft.FontWeight.BOLD),
                                    ft.Text(signo.talla),
                                ],
                                spacing=5,
                            ),
                            ft.Row(
                                [
                                    ft.IconButton(
                                        ft.icons.EDIT,
                                        icon_color=ft.colors.BLUE,
                                        tooltip="Editar signos vitales",
                                        on_click=lambda e, t=signo: open_edit_dialog(t),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                            ft.Divider(height=10, color=ft.colors.GREY_300),
                        ]
                    )

                # ExpansionTile para los signos vitales
                signos_expansion = ft.ExpansionTile(
                    title=ft.Text("🩺 Signos Vitales", weight=ft.FontWeight.BOLD),
                    controls=[signos_content],
                )
                contenido.controls.append(signos_expansion)

            # Crear la tarjeta principal del paciente
            tamizaje_card = ft.Card(
                content=ft.Container(
                    content=ft.ExpansionTile(
                        title=ft.Text(
                            f"👤 Paciente: {paciente.nombre} {paciente.apellido}",
                            weight=ft.FontWeight.BOLD,
                        ),
                        controls=[contenido],
                    ),
                    padding=ft.padding.symmetric(vertical=10, horizontal=15),
                ),
                elevation=3,
                margin=ft.margin.symmetric(vertical=5),
                width=page.window_width * 0.95,  # type: ignore
            )

            tamizajes_list.controls.append(tamizaje_card)
        page.update()

    # def confirm_delete_dialog_handler(paciente):
    #     """Abre el diálogo de confirmación para eliminar todos los antecedentes y signos vitales del paciente."""
    #     nonlocal selected_tamizaje
    #     selected_tamizaje = paciente  # Guardar el paciente seleccionado 
    #     confirm_delete_dialog.open = True
    #     page.update()

    def add_tamizaje_clicked(e):
        """Agrega un nuevo tamizaje (antecedente médico o signo vital)."""
        # Validar campos requeridos
        campos_requeridos = [
            tamizaje_paciente,
            tamizaje_tipo,
            tamizaje_descripcion,
            tamizaje_fecha,
            tamizaje_presion_arterial,
            tamizaje_frecuencia_cardiaca,
            tamizaje_frecuencia_respiratoria,
            tamizaje_temperatura,
            tamizaje_peso,
            tamizaje_talla,
        ]

        if not validar_campos_requeridos(campos_requeridos):
            return

        try:
            # Verificar si el paciente ya tiene un tamizaje
            paciente_id = tamizaje_paciente.value
            if paciente_tiene_tamizaje(paciente_id, all_tamizajes):
                show_alert("Este paciente ya tiene un tamizaje.")
                return

            # Agregar tamizaje usando la función de tamizaje_crud
            agregar_tamizaje(
                paciente_id,
                tamizaje_tipo.value,
                tamizaje_descripcion.value,
                tamizaje_fecha.value,
                tamizaje_presion_arterial.value,
                tamizaje_frecuencia_cardiaca.value,
                tamizaje_frecuencia_respiratoria.value,
                tamizaje_temperatura.value,
                tamizaje_peso.value,
                tamizaje_talla.value,
            )

            clear_fields()
            refresh_tamizajes()
            # Colapsar el panel del formulario
            form_panel.expanded = False
            page.update()
        except ValueError as e:
            show_alert(f"Error al agregar tamizaje: {str(e)}")

    def open_edit_dialog(tamizaje):
        """Abre el diálogo de edición para un tamizaje."""
        nonlocal selected_tamizaje
        selected_tamizaje = tamizaje  # Guardar el tamizaje seleccionado

        if hasattr(tamizaje, "tipo"):  # Si es un antecedente médico
            edit_id.value = tamizaje.id_antecedente
            edit_tipo.value = tamizaje.tipo
            edit_descripcion.value = tamizaje.descripcion
            edit_dialog.content.controls = [
                edit_tipo,
                edit_descripcion,
            ]  # Mostrar solo campos de antecedentes
        else:  # Si es un signo vital
            edit_id.value = tamizaje.id_signo
            edit_fecha.value = tamizaje.fecha
            edit_presion_arterial.value = tamizaje.presion_arterial
            edit_frecuencia_cardiaca.value = tamizaje.frecuencia_cardiaca
            edit_frecuencia_respiratoria.value = tamizaje.frecuencia_respiratoria
            edit_temperatura.value = tamizaje.temperatura
            edit_peso.value = tamizaje.peso
            edit_talla.value = tamizaje.talla
            edit_dialog.content.controls = [  # Mostrar solo campos de signos vitales
                edit_fecha,
                edit_presion_arterial,
                edit_frecuencia_cardiaca,
                edit_frecuencia_respiratoria,
                edit_temperatura,
                edit_peso,
                edit_talla,
            ]

        edit_dialog.open = True
        page.update()

    def save_edit(e):
        """Guarda los cambios realizados en el tamizaje."""
        nonlocal selected_tamizaje

        # Validar campos requeridos
        campos_requeridos = []
        if hasattr(selected_tamizaje, "tipo"):
            campos_requeridos.extend([edit_tipo, edit_descripcion])
        else:
            campos_requeridos.extend(
                [
                    edit_fecha,
                    edit_presion_arterial,
                    edit_frecuencia_cardiaca,
                    edit_frecuencia_respiratoria,
                    edit_temperatura,
                    edit_peso,
                    edit_talla,
                ]
            )

        if not validar_campos_requeridos(campos_requeridos):
            return

        try:
            actualizar_tamizaje(
                selected_tamizaje,
                tipo=edit_tipo.value if hasattr(selected_tamizaje, "tipo") else None,
                descripcion=(
                    edit_descripcion.value
                    if hasattr(selected_tamizaje, "tipo")
                    else None
                ),
                fecha=(
                    edit_fecha.value if not hasattr(selected_tamizaje, "tipo") else None
                ),
                presion_arterial=(
                    edit_presion_arterial.value
                    if not hasattr(selected_tamizaje, "tipo")
                    else None
                ),
                frecuencia_cardiaca=(
                    edit_frecuencia_cardiaca.value
                    if not hasattr(selected_tamizaje, "tipo")
                    else None
                ),
                frecuencia_respiratoria=(
                    edit_frecuencia_respiratoria.value
                    if not hasattr(selected_tamizaje, "tipo")
                    else None
                ),
                temperatura=(
                    edit_temperatura.value
                    if not hasattr(selected_tamizaje, "tipo")
                    else None
                ),
                peso=(
                    edit_peso.value if not hasattr(selected_tamizaje, "tipo") else None
                ),
                talla=(
                    edit_talla.value if not hasattr(selected_tamizaje, "tipo") else None
                ),
            )
            edit_dialog.open = False
            refresh_tamizajes()
        except Exception as e:
            show_alert(f"Error al actualizar tamizaje: {str(e)}")

    def clear_fields():
        """Limpia los campos del formulario."""
        tamizaje_paciente.value = ""
        tamizaje_tipo.value = ""
        tamizaje_descripcion.value = ""
        tamizaje_fecha.value = ""
        tamizaje_presion_arterial.value = ""
        tamizaje_frecuencia_cardiaca.value = ""
        tamizaje_frecuencia_respiratoria.value = ""
        tamizaje_temperatura.value = ""
        tamizaje_peso.value = ""
        tamizaje_talla.value = ""
        page.update()

    def change_page(delta):
        """Cambia la página actual."""
        nonlocal current_page
        current_page += delta
        if current_page < 0:
            current_page = 0
        max_pages = (len(all_tamizajes) + tamizajes_per_page - 1) // tamizajes_per_page
        if current_page >= max_pages:
            current_page = max_pages - 1
        page_number_text.value = f"Página {current_page + 1}"
        refresh_tamizajes()

    def on_search(e):
        """Filtra los tamizajes según la consulta de búsqueda."""
        nonlocal search_query, current_page
        search_query = search_field.value
        current_page = 0
        page_number_text.value = f"Página {current_page + 1}"
        refresh_tamizajes()

    def on_paciente_search(e):
        """Busca pacientes por nombre o apellido, manejando caracteres especiales y acentos."""

        def normalize_string(s):
            """Normaliza un string removiendo acentos y caracteres especiales."""
            if not s:
                return ""
            return (
                unicodedata.normalize("NFKD", str(s))
                .encode("ASCII", "ignore")
                .decode("ASCII")
                .lower()
            )

        search_text = paciente_search_field.value
        if search_text:
            # Normalizamos el texto de búsqueda
            normalized_search = normalize_string(search_text)

            resultados = [
                p
                for p in get_pacientes_by_id_usuario(id_usuario)
                if (normalized_search in normalize_string(p.nombre))
                or (normalized_search in normalize_string(p.apellido))
            ]

            paciente_results.controls = [
                ft.ListTile(
                    title=ft.Text(f"{p.nombre} {p.apellido}"),
                    subtitle=ft.Text(f"ID: {p.id_paciente}"),
                    on_click=lambda e, p=p: select_paciente(p),
                )
                for p in resultados
            ]
        else:
            paciente_results.controls = []

        page.update()

    def select_paciente(paciente):
        """Selecciona un paciente y completa el campo de ID."""
        nonlocal tamizaje_paciente, paciente_search_field, paciente_results

        # Verificar si el paciente tiene una historia clínica
        if not paciente_tiene_historia(
            paciente.id_paciente
        ):  # Usar la función de verificación
            show_alert(
                "Este paciente no tiene una historia clínica. Registre una historia clínica primero."
            )  # Mostrar alerta
            return  # Salir de la función si el paciente no tiene una historia clínica

        # Verificar si el paciente ya tiene un tamizaje
        if paciente_tiene_tamizaje(paciente.id_paciente, all_tamizajes):
            show_alert("Este paciente ya tiene un tamizaje registrado.")
            # Limpiar campos pero mantener la búsqueda
            tamizaje_paciente.value = ""
            paciente_results.controls = []
            agregar_button.disabled = True
            return

        # Si el paciente tiene una historia clínica y no tiene un tamizaje, seleccionarlo
        tamizaje_paciente.value = paciente.id_paciente
        paciente_search_field.value = f"{paciente.nombre} {paciente.apellido}"
        paciente_results.controls = []
        agregar_button.disabled = False  # Asegurarnos que el botón esté habilitado
        page.update()

    # def open_add_signo_dialog(paciente):
    #     """Abre el diálogo para agregar nuevos signos vitales."""
    #     nonlocal selected_tamizaje
    #     selected_tamizaje = paciente
    #     add_signo_dialog.content.controls[0].value = ""  # Limpiar campo de fecha
    #     add_signo_dialog.content.controls[1].value = (
    #         ""  # Limpiar campo de presión arterial
    #     )
    #     add_signo_dialog.content.controls[2].value = (
    #         ""  # Limpiar campo de frecuencia cardíaca
    #     )
    #     add_signo_dialog.content.controls[3].value = (
    #         ""  # Limpiar campo de frecuencia respiratoria
    #     )
    #     add_signo_dialog.content.controls[4].value = ""  # Limpiar campo de temperatura
    #     add_signo_dialog.content.controls[5].value = ""  # Limpiar campo de peso
    #     add_signo_dialog.content.controls[6].value = ""  # Limpiar campo de talla
    #     add_signo_dialog.open = True
    #     page.update()

    # def add_signo_vital_clicked(e):
    #     """Agrega un nuevo signo vital."""
    #     if all([field.value for field in add_signo_dialog.content.controls]):
    #         try:
    #             agregar_signo_vital(  # Usar la nueva función
    #                 selected_tamizaje.id_paciente,  # type: ignore
    #                 add_signo_dialog.content.controls[0].value,  # Fecha
    #                 add_signo_dialog.content.controls[1].value,  # Presión arterial
    #                 add_signo_dialog.content.controls[2].value,  # Frecuencia cardíaca
    #                 add_signo_dialog.content.controls[
    #                     3
    #                 ].value,  # Frecuencia respiratoria
    #                 add_signo_dialog.content.controls[4].value,  # Temperatura
    #                 add_signo_dialog.content.controls[5].value,  # Peso
    #                 add_signo_dialog.content.controls[6].value,  # Talla
    #             )
    #             add_signo_dialog.open = False
    #             refresh_tamizajes()
    #             page.update()
    #         except ValueError as e:
    #             show_alert(
    #                 f"Error al agregar signo vital: {str(e)}"
    #             )  # Mostrar alerta de error

    # Crear el formulario de tamizaje
    formulario = crear_formulario_tamizaje(
        page,
        add_tamizaje_clicked,
        on_paciente_search,
        select_paciente,
        all_tamizajes,  # Pasar la lista de tamizajes al formulario
    )

    # Acceder a los componentes del formulario
    form_content = formulario["form_content"]
    tamizaje_paciente = formulario["tamizaje_paciente"]
    tamizaje_tipo = formulario["tamizaje_tipo"]
    tamizaje_tipo.value = "Personal"
    tamizaje_descripcion = formulario["tamizaje_descripcion"]
    tamizaje_fecha = formulario["tamizaje_fecha"]
    tamizaje_presion_arterial = formulario["tamizaje_presion_arterial"]
    tamizaje_frecuencia_cardiaca = formulario["tamizaje_frecuencia_cardiaca"]
    tamizaje_frecuencia_respiratoria = formulario["tamizaje_frecuencia_respiratoria"]
    tamizaje_temperatura = formulario["tamizaje_temperatura"]
    tamizaje_peso = formulario["tamizaje_peso"]
    tamizaje_talla = formulario["tamizaje_talla"]
    paciente_search_field = formulario["paciente_search_field"]
    paciente_results = formulario["paciente_results"]
    agregar_button = formulario["agregar_button"]

    # Crear el ExpansionPanel para el formulario
    form_panel = ft.ExpansionPanel(
        header=ft.ListTile(
            title=ft.Text("Agregar Nuevo Tamizaje"),
            on_click=lambda e: setattr(form_panel, "expanded", not form_panel.expanded)
            or page.update(),
        ),
        content=ft.Container(content=form_content),
        expanded=False,  # Inicialmente colapsado
    )

    # Crear el ExpansionPanelList para contener el panel del formulario
    expansion_panel_list = ft.ExpansionPanelList(
        controls=[form_panel],
        on_change=lambda e: page.update(),
    )

    # Crear la interfaz de usuario
    ui = crear_tamizaje_ui(
        page,
        # confirm_delete,
        # add_signo_vital_clicked,
        save_edit,
        on_search,
        change_page,
    )

    # Acceder a los componentes de la UI
    page_number_text = ui["page_number_text"]
    # confirm_delete_dialog = ui["confirm_delete_dialog"]
    # add_signo_dialog = ui["add_signo_dialog"]
    alert_dialog = ui["alert_dialog"]
    search_field = ui["search_field"]
    tamizajes_list = ui["tamizajes_list"]
    edit_id = ui["edit_id"]
    edit_tipo = ui["edit_tipo"]
    edit_descripcion = ui["edit_descripcion"]
    edit_fecha = ui["edit_fecha"]
    edit_presion_arterial = ui["edit_presion_arterial"]
    edit_frecuencia_cardiaca = ui["edit_frecuencia_cardiaca"]
    edit_frecuencia_respiratoria = ui["edit_frecuencia_respiratoria"]
    edit_temperatura = ui["edit_temperatura"]
    edit_peso = ui["edit_peso"]
    edit_talla = ui["edit_talla"]
    edit_dialog = ui["edit_dialog"]
    pagination_controls = ui["pagination_controls"]

    refresh_tamizajes()

    return ft.Column(
        [
            ft.Text("Gestión de Tamizajes", size=24, weight=ft.FontWeight.BOLD),
            expansion_panel_list,  # Mostrar el panel del formulario
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
            ft.Row([search_field], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
            ft.Container(
                content=tamizajes_list,
                expand=True,
                padding=10,
                alignment=ft.alignment.top_center,
            ),
            pagination_controls,
            edit_dialog,
            # confirm_delete_dialog,
            # add_signo_dialog,
            alert_dialog,  # Asegúrate de incluir el diálogo de alerta
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )
