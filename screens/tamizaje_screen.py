import flet as ft
from services.antecedente_medico_service import (
    get_antecedentes_medicos_by_paciente,
    add_antecedente_medico,
    update_antecedente_medico,
    delete_antecedente_medico,
)
from services.signo_vital_service import (
    get_signos_vitales_by_paciente,
    add_signo_vital,
    update_signo_vital,
    delete_signo_vital,
)
from services.paciente_service import get_paciente, get_pacientes_by_id_usuario
from utils.formulario_tamizaje import crear_formulario_tamizaje


def TamizajeScreen(page: ft.Page, id_usuario: int):
    selected_tamizaje = None  # Variable para almacenar el tamizaje seleccionado
    current_page = 0  # Página actual de la paginación
    tamizajes_per_page = 5  # Número de tamizajes por página
    search_query = ""  # Variable para almacenar la consulta de búsqueda
    all_tamizajes = []  # Lista para almacenar todos los tamizajes

    # Texto dinámico para mostrar el número de página
    page_number_text = ft.Text(f"Página {current_page + 1}")

    # Diálogo de confirmación para eliminar
    confirm_delete_dialog = ft.AlertDialog(
        title=ft.Text("Confirmar eliminación"),
        content=ft.Text("¿Estás seguro de que deseas eliminar este tamizaje?"),
        actions=[
            ft.TextButton("Sí", on_click=lambda e: confirm_delete(True)),
            ft.TextButton("No", on_click=lambda e: confirm_delete(False)),
        ],
    )

    # Diálogo para agregar nuevos signos vitales
    add_signo_dialog = ft.AlertDialog(
        title=ft.Text("Agregar nuevo signo vital"),
        content=ft.Column(
            [
                ft.TextField(label="Fecha", expand=True),
                ft.TextField(label="Presión arterial", expand=True),
                ft.TextField(label="Frecuencia cardíaca", expand=True),
                ft.TextField(label="Frecuencia respiratoria", expand=True),
                ft.TextField(label="Temperatura", expand=True),
                ft.TextField(label="Peso", expand=True),
                ft.TextField(label="Talla", expand=True),
            ],
            spacing=10
        ),
        actions=[
            ft.TextButton("Agregar", on_click=lambda e: add_signo_vital_clicked(e)),
            ft.TextButton("Cancelar", on_click=lambda e: setattr(add_signo_dialog, "open", False) or page.update())
        ],
    )

    # Diálogo de alerta para mostrar errores
    alert_dialog = ft.AlertDialog(
        title=ft.Text("Error"),
        content=ft.Text(""),
        actions=[
            ft.TextButton(
                "OK",
                on_click=lambda e: setattr(alert_dialog, "open", False) or page.update(),
            )
        ],
    )

    def show_alert(message):
        """Muestra un diálogo de alerta con el mensaje proporcionado."""
        alert_dialog.content = ft.Text(message)
        alert_dialog.open = True
        page.update()

    def confirm_delete(confirmed):
        """Maneja la confirmación de eliminación."""
        nonlocal selected_tamizaje
        confirm_delete_dialog.open = False
        page.update()
        if confirmed:
            remove_tamizaje(selected_tamizaje)
        selected_tamizaje = None  # Reiniciar el tamizaje seleccionado

    def remove_tamizaje(tamizaje):
        """Elimina el tamizaje."""
        if hasattr(tamizaje, "tipo"):  # Si es un antecedente médico
            delete_antecedente_medico(tamizaje.id_antecedente)
        else:  # Si es un signo vital
            delete_signo_vital(tamizaje.id_signo)
        refresh_tamizajes()

    def refresh_tamizajes():
        """Actualiza la lista de tamizajes (antecedentes médicos y signos vitales)."""
        nonlocal all_tamizajes
        tamizajes_list.controls.clear()
        all_tamizajes = []

        # Obtener todos los pacientes asociados al usuario
        pacientes = get_pacientes_by_id_usuario(id_usuario)

        # Obtener antecedentes médicos y signos vitales para cada paciente
        for paciente in pacientes:
            antecedentes = get_antecedentes_medicos_by_paciente(paciente.id_paciente, id_usuario)
            signos_vitales = get_signos_vitales_by_paciente(paciente.id_paciente, id_usuario)

            # Si el paciente tiene antecedentes o signos, agregarlo a la lista
            if antecedentes or signos_vitales:
                all_tamizajes.append({
                    "paciente": paciente,
                    "antecedentes": antecedentes,
                    "signos_vitales": signos_vitales
                })

        # Filtrar tamizajes por nombre o apellido del paciente (si hay una búsqueda)
        if search_query:
            all_tamizajes = [
                t for t in all_tamizajes
                if search_query.lower() in t["paciente"].nombre.lower() or
                   search_query.lower() in t["paciente"].apellido.lower()
            ]

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
                contenido.controls.append(ft.Text("Antecedentes Médicos", weight=ft.FontWeight.BOLD))
                for antecedente in antecedentes:
                    contenido.controls.extend([
                        ft.Text(f"Tipo: {antecedente.tipo}"),
                        ft.Text(f"Descripción: {antecedente.descripcion}"),
                        ft.Row(
                            [
                                ft.IconButton(ft.icons.EDIT, on_click=lambda e, t=antecedente: open_edit_dialog(t)),
                                ft.IconButton(ft.icons.DELETE, on_click=lambda e, t=antecedente: confirm_delete_dialog_handler(t))
                            ],
                            alignment=ft.MainAxisAlignment.END
                        ),
                        ft.Divider(height=10, color=ft.colors.GREY_300),
                    ])

            # Sección de signos vitales
            if signos_vitales:
                signos_content = ft.Column(spacing=5)
                for signo in signos_vitales:
                    signos_content.controls.extend([
                        ft.Text(f"Fecha: {signo.fecha}"),
                        ft.Text(f"Presión arterial: {signo.presion_arterial}"),
                        ft.Text(f"Frecuencia cardíaca: {signo.frecuencia_cardiaca}"),
                        ft.Text(f"Frecuencia respiratoria: {signo.frecuencia_respiratoria}"),
                        ft.Text(f"Temperatura: {signo.temperatura}"),
                        ft.Text(f"Peso: {signo.peso}"),
                        ft.Text(f"Talla: {signo.talla}"),
                        ft.Row(
                            [
                                ft.IconButton(ft.icons.EDIT, on_click=lambda e, t=signo: open_edit_dialog(t)),
                                ft.IconButton(ft.icons.DELETE, on_click=lambda e, t=signo: confirm_delete_dialog_handler(t))
                            ],
                            alignment=ft.MainAxisAlignment.END
                        ),
                        ft.Divider(height=10, color=ft.colors.GREY_300),
                    ])

                # ExpansionTile para los signos vitales
                signos_expansion = ft.ExpansionTile(
                    title=ft.Row(
                        [
                            ft.Text("Signos Vitales", weight=ft.FontWeight.BOLD),
                            ft.IconButton(ft.icons.ADD, on_click=lambda e, p=paciente: open_add_signo_dialog(p)),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    controls=[signos_content],
                )
                contenido.controls.append(signos_expansion)

            tamizaje_card = ft.ExpansionTile(
                title=ft.Text(f"Paciente: {paciente.nombre} {paciente.apellido}", weight=ft.FontWeight.BOLD),
                controls=[contenido],
            )

            tamizajes_list.controls.append(tamizaje_card)
        page.update()

    def confirm_delete_dialog_handler(tamizaje):
        """Abre el diálogo de confirmación para eliminar."""
        nonlocal selected_tamizaje
        selected_tamizaje = tamizaje  # Guardar el tamizaje seleccionado
        confirm_delete_dialog.open = True
        page.update()

    def add_tamizaje_clicked(e):
        """Agrega un nuevo tamizaje (antecedente médico o signo vital)."""
        if all([tamizaje_paciente.value, tamizaje_tipo.value, tamizaje_descripcion.value, tamizaje_fecha.value, tamizaje_presion_arterial.value, tamizaje_frecuencia_cardiaca.value, tamizaje_frecuencia_respiratoria.value, tamizaje_temperatura.value, tamizaje_peso.value, tamizaje_talla.value]):
            try:
                # Verificar si el paciente ya tiene un tamizaje
                paciente_id = tamizaje_paciente.value
                if paciente_tiene_tamizaje(paciente_id, all_tamizajes):  # Usar la función de validación del formulario
                    show_alert("Este paciente ya tiene un tamizaje.")  # Mostrar alerta
                    return  # Salir de la función si el paciente ya tiene un tamizaje

                # Agregar antecedente médico
                add_antecedente_medico(
                    paciente_id, tamizaje_tipo.value, tamizaje_descripcion.value
                )
                # Agregar signo vital
                add_signo_vital(
                    paciente_id, tamizaje_fecha.value, tamizaje_presion_arterial.value, tamizaje_frecuencia_cardiaca.value, tamizaje_frecuencia_respiratoria.value, tamizaje_temperatura.value, tamizaje_peso.value, tamizaje_talla.value
                )
                clear_fields()
                refresh_tamizajes()
                # Colapsar el panel del formulario
                form_panel.expanded = False
                page.update()
            except ValueError as e:
                show_alert(f"Error al agregar tamizaje: {str(e)}")  # Mostrar alerta de error

    def paciente_tiene_tamizaje(paciente_id, all_tamizajes):
        """Verifica si un paciente ya tiene un tamizaje."""
        for tamizaje in all_tamizajes:
            if tamizaje["paciente"].id_paciente == paciente_id:
                return True
        return False

    def open_edit_dialog(tamizaje):
        """Abre el diálogo de edición para un tamizaje."""
        nonlocal selected_tamizaje
        selected_tamizaje = tamizaje  # Guardar el tamizaje seleccionado

        if hasattr(tamizaje, "tipo"):  # Si es un antecedente médico
            edit_id.value = tamizaje.id_antecedente
            edit_tipo.value = tamizaje.tipo
            edit_descripcion.value = tamizaje.descripcion
            edit_dialog.content.controls = [edit_tipo, edit_descripcion]  # Mostrar solo campos de antecedentes
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
        if hasattr(selected_tamizaje, "tipo"):  # Si es un antecedente médico
            update_antecedente_medico(
                edit_id.value, edit_tipo.value, edit_descripcion.value
            )
        else:  # Si es un signo vital
            update_signo_vital(
                edit_id.value, edit_fecha.value, edit_presion_arterial.value, edit_frecuencia_cardiaca.value, edit_frecuencia_respiratoria.value, edit_temperatura.value, edit_peso.value, edit_talla.value
            )
        edit_dialog.open = False
        refresh_tamizajes()

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
        """Busca pacientes por nombre o apellido."""
        search_text = paciente_search_field.value.lower()
        if search_text:
            resultados = [
                p for p in get_pacientes_by_id_usuario(id_usuario)
                if search_text in p.nombre.lower() or search_text in p.apellido.lower()
            ]
            paciente_results.controls = [
                ft.ListTile(
                    title=ft.Text(f"{p.nombre} {p.apellido}"),
                    subtitle=ft.Text(f"ID: {p.id_paciente}"),
                    on_click=lambda e, p=p: select_paciente(p)
                ) for p in resultados
            ]
        else:
            paciente_results.controls = []
        page.update()

    def select_paciente(paciente):
        """Selecciona un paciente y completa el campo de ID."""
        nonlocal tamizaje_paciente, paciente_search_field, paciente_results

        # Verificar si el paciente ya tiene un tamizaje
        if paciente_tiene_tamizaje(paciente.id_paciente, all_tamizajes):  # Usar la función de validación del formulario
            show_alert("Este paciente ya tiene un tamizaje.")  # Mostrar alerta
            return  # Salir de la función si el paciente ya tiene un tamizaje

        tamizaje_paciente.value = paciente.id_paciente
        paciente_search_field.value = f"{paciente.nombre} {paciente.apellido}"
        paciente_results.controls = []
        page.update()

    def open_add_signo_dialog(paciente):
        """Abre el diálogo para agregar nuevos signos vitales."""
        nonlocal selected_tamizaje
        selected_tamizaje = paciente
        add_signo_dialog.content.controls[0].value = ""  # Limpiar campo de fecha
        add_signo_dialog.content.controls[1].value = ""  # Limpiar campo de presión arterial
        add_signo_dialog.content.controls[2].value = ""  # Limpiar campo de frecuencia cardíaca
        add_signo_dialog.content.controls[3].value = ""  # Limpiar campo de frecuencia respiratoria
        add_signo_dialog.content.controls[4].value = ""  # Limpiar campo de temperatura
        add_signo_dialog.content.controls[5].value = ""  # Limpiar campo de peso
        add_signo_dialog.content.controls[6].value = ""  # Limpiar campo de talla
        add_signo_dialog.open = True
        page.update()

    def add_signo_vital_clicked(e):
        """Agrega un nuevo signo vital."""
        if all([field.value for field in add_signo_dialog.content.controls]):
            try:
                add_signo_vital(
                    selected_tamizaje.id_paciente,
                    add_signo_dialog.content.controls[0].value,  # Fecha
                    add_signo_dialog.content.controls[1].value,  # Presión arterial
                    add_signo_dialog.content.controls[2].value,  # Frecuencia cardíaca
                    add_signo_dialog.content.controls[3].value,  # Frecuencia respiratoria
                    add_signo_dialog.content.controls[4].value,  # Temperatura
                    add_signo_dialog.content.controls[5].value,  # Peso
                    add_signo_dialog.content.controls[6].value,  # Talla
                )
                add_signo_dialog.open = False
                refresh_tamizajes()
                page.update()
            except ValueError as e:
                show_alert(f"Error al agregar signo vital: {str(e)}")  # Mostrar alerta de error

    # Crear el formulario de tamizaje
    formulario = crear_formulario_tamizaje(
        page,
        add_tamizaje_clicked,
        on_paciente_search,
        select_paciente,
        all_tamizajes  # Pasar la lista de tamizajes al formulario
    )

    # Acceder a los componentes del formulario
    form_content = formulario["form_content"]
    tamizaje_paciente = formulario["tamizaje_paciente"]
    tamizaje_tipo = formulario["tamizaje_tipo"]
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
    paciente_tiene_tamizaje = formulario["paciente_tiene_tamizaje"]  # Obtener la función de validación

    # Crear el ExpansionPanel para el formulario
    form_panel = ft.ExpansionPanel(
        header=ft.ListTile(
            title=ft.Text("Agregar Nuevo Tamizaje"),
            on_click=lambda e: setattr(form_panel, "expanded", not form_panel.expanded) or page.update(),
        ),
        content=ft.Container(content=form_content),
        expanded=False,  # Inicialmente colapsado
    )

    # Crear el ExpansionPanelList para contener el panel del formulario
    expansion_panel_list = ft.ExpansionPanelList(
        controls=[form_panel],
        on_change=lambda e: page.update(),
    )

    # Campo de búsqueda de tamizajes
    search_field = ft.TextField(
        label="Buscar por nombre o apellido del paciente",
        on_change=on_search,
        expand=True,
        suffix=ft.IconButton(ft.icons.SEARCH, on_click=on_search)
    )

    # Lista de tamizajes
    tamizajes_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    # Diálogo de edición
    edit_id = ft.TextField(label="ID Tamizaje", disabled=True)
    edit_tipo = ft.TextField(label="Tipo de antecedente médico")
    edit_descripcion = ft.TextField(label="Descripción del antecedente médico")
    edit_fecha = ft.TextField(label="Fecha del signo vital")
    edit_presion_arterial = ft.TextField(label="Presión arterial")
    edit_frecuencia_cardiaca = ft.TextField(label="Frecuencia cardíaca")
    edit_frecuencia_respiratoria = ft.TextField(label="Frecuencia respiratoria")
    edit_temperatura = ft.TextField(label="Temperatura")
    edit_peso = ft.TextField(label="Peso")
    edit_talla = ft.TextField(label="Talla")
    edit_dialog = ft.AlertDialog(
        title=ft.Text("Editar Tamizaje"),
        content=ft.Column(
            [
                edit_tipo,
                edit_descripcion,
                edit_fecha,
                edit_presion_arterial,
                edit_frecuencia_cardiaca,
                edit_frecuencia_respiratoria,
                edit_temperatura,
                edit_peso,
                edit_talla,
            ],
            spacing=10
        ),
        actions=[
            ft.TextButton("Guardar", on_click=save_edit),
            ft.TextButton("Cancelar", on_click=lambda e: setattr(edit_dialog, "open", False) or page.update())
        ],
    )

    # Controles de paginación
    pagination_controls = ft.Row(
        [
            ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: change_page(-1)),
            page_number_text,
            ft.IconButton(ft.icons.ARROW_FORWARD, on_click=lambda e: change_page(1)),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

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
                alignment=ft.alignment.top_center
            ),
            pagination_controls,
            edit_dialog,
            confirm_delete_dialog,
            add_signo_dialog,
            alert_dialog  # Asegúrate de incluir el diálogo de alerta
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )