import flet as ft


def crear_tamizaje_ui(page, save_edit, on_search, change_page):
    # def crear_tamizaje_ui(
    #     page, confirm_delete, add_signo_vital_clicked, save_edit, on_search, change_page
    # ):
    """Crea la interfaz de usuario para la gestión de tamizajes."""
    # Texto dinámico para mostrar el número de página
    page_number_text = ft.Text(f"Página 1")

    # Diálogo de confirmación para eliminar
    # confirm_delete_dialog = ft.AlertDialog(
    #     title=ft.Text("Confirmar eliminación"),
    #     content=ft.Text(
    #         "¿Estás seguro de que deseas eliminar todos los antecedentes y signos vitales de este paciente?"
    #     ),
    #     actions=[
    #         ft.TextButton("Sí", on_click=lambda e: confirm_delete(True)),
    #         ft.TextButton("No", on_click=lambda e: confirm_delete(False)),
    #     ],
    # )

    # Diálogo para agregar nuevos signos vitales
    # add_signo_dialog = ft.AlertDialog(
    #     title=ft.Text("Agregar nuevo signo vital"),
    #     content=ft.Column(
    #         [
    #             ft.TextField(label="Fecha", expand=True),
    #             ft.TextField(label="Presión arterial", expand=True),
    #             ft.TextField(label="Frecuencia cardíaca", expand=True),
    #             ft.TextField(label="Frecuencia respiratoria", expand=True),
    #             ft.TextField(label="Temperatura", expand=True),
    #             ft.TextField(label="Peso", expand=True),
    #             ft.TextField(label="Talla", expand=True),
    #         ],
    #         spacing=10,
    #     ),
    #     actions=[
    #         ft.TextButton("Agregar", on_click=lambda e: add_signo_vital_clicked(e)),
    #         ft.TextButton(
    #             "Cancelar",
    #             on_click=lambda e: setattr(add_signo_dialog, "open", False)
    #             or page.update(),
    #         ),
    #     ],
    # )

    # Diálogo de alerta para mostrar errores
    alert_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row(
            controls=[
                ft.Icon(ft.icons.WARNING_AMBER, color=ft.colors.AMBER),
                ft.Text(" Advertencia", weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        content=ft.Text(""),  # Contenido dinámico
        actions=[
            ft.TextButton(
                "OK",
                on_click=lambda e: setattr(alert_dialog, "open", False) or page.update(),
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )


    # Campo de búsqueda de tamizajes
    search_field = ft.TextField(
        label="Buscar por nombre o apellido del paciente",
        on_change=on_search,
        expand=True,
        suffix=ft.IconButton(ft.icons.SEARCH, on_click=on_search),
    )

    # Lista de tamizajes
    tamizajes_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    # Diálogo de edición
    edit_id = ft.TextField(label="ID Tamizaje", disabled=True)
    edit_tipo = ft.Dropdown(
        label="Tipo de antecedente médico",
        options=[
            ft.dropdown.Option("Personal"),
            ft.dropdown.Option("Familiar"),
        ],
    )
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
            spacing=10,
        ),
        actions=[
            ft.TextButton("Guardar", on_click=save_edit),
            ft.TextButton(
                "Cancelar",
                on_click=lambda e: setattr(edit_dialog, "open", False) or page.update(),
            ),
        ],
    )

    # Controles de paginación
    pagination_controls = ft.Row(
        [
            ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: change_page(-1)),
            page_number_text,
            ft.IconButton(ft.icons.ARROW_FORWARD, on_click=lambda e: change_page(1)),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    return {
        "page_number_text": page_number_text,
        # "confirm_delete_dialog": confirm_delete_dialog,
        # "add_signo_dialog": add_signo_dialog,
        "alert_dialog": alert_dialog,
        "search_field": search_field,
        "tamizajes_list": tamizajes_list,
        "edit_id": edit_id,
        "edit_tipo": edit_tipo,
        "edit_descripcion": edit_descripcion,
        "edit_fecha": edit_fecha,
        "edit_presion_arterial": edit_presion_arterial,
        "edit_frecuencia_cardiaca": edit_frecuencia_cardiaca,
        "edit_frecuencia_respiratoria": edit_frecuencia_respiratoria,
        "edit_temperatura": edit_temperatura,
        "edit_peso": edit_peso,
        "edit_talla": edit_talla,
        "edit_dialog": edit_dialog,
        "pagination_controls": pagination_controls,
    }
