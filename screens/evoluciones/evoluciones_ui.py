import flet as ft


def crear_evoluciones_ui(
    page,
    on_search,
    on_search_cie,
    change_page,
    save_edit,
    open_diagnostico_dialog,
    open_prescripciones_dialog,
    open_signos_dialog,
    open_tratamientos_dialog,
    open_consulta_dialog,
    agregar_medicamento,
    cancelar_edicion,
    save_full_consultation,
    close_all_dialogs,
):
    page_number_text = ft.Text(f"Página 1")

    # Diálogos
    alert_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Aviso"),
        actions=[
            ft.TextButton(
                "OK",
                on_click=lambda e: setattr(alert_dialog, "open", False)
                or page.update(),
            )
        ],
    )

    # Controles para EDICIÓN
    edit_id = ft.TextField(visible=False)
    edit_paciente = ft.TextField(visible=False)
    edit_motivo = ft.TextField(label="Motivo de consulta", multiline=True)
    edit_enfermedad = ft.TextField(label="Enfermedad actual", multiline=True)

    # Diálogo de edición
    edit_id = ft.TextField(label="ID Historia Clínica", disabled=True)
    edit_paciente = ft.TextField(label="ID Paciente", disabled=True)
    edit_motivo = ft.TextField(label="Motivo de consulta")
    edit_enfermedad = ft.TextField(label="Enfermedad actual")
    edit_dialog = ft.AlertDialog(
        title=ft.Text("Editar Historia Clínica"),
        content=ft.Column(
            [
                edit_motivo,
                edit_enfermedad,
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

    # Controles para NUEVA CONSULTA
    new_consult_paciente_info = ft.TextField(label="Paciente", disabled=True)
    new_consult_paciente_id = ft.TextField(label="ID Paciente", visible=False)
    new_consult_paciente_nombre = ft.TextField(
        label="Nombre del paciente", visible=False
    )

    # --- Diálogo 1: Signos Vitales ---
    signos_presion = ft.TextField(label="Presión Arterial")
    signos_frec_cardiaca = ft.TextField(label="Frecuencia Cardíaca")
    signos_frec_respi = ft.TextField(label="Frecuencia Respiratoria")
    signos_temp = ft.TextField(label="Temperatura")
    signos_peso = ft.TextField(label="Peso")
    signos_talla = ft.TextField(label="Talla")

    signos_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Signos Vitales"),
        content=ft.Column(
            [
                new_consult_paciente_info,
                ft.Row([signos_presion, signos_frec_cardiaca]),
                ft.Row([signos_frec_respi, signos_temp]),
                ft.Row([signos_peso, signos_talla]),
            ],
            spacing=10,
            width=900,
        ),
        actions=[
            ft.TextButton("Continuar", on_click=lambda e: open_diagnostico_dialog()),
            ft.TextButton("Cancelar", on_click=close_all_dialogs),
        ],
    )

    # --- Diálogo 2: Diagnóstico ---
    diagnostico_buscador = ft.TextField(
        label="Buscar cie...",
        on_change=on_search_cie,
        width=page.window_width * 0.9,
        suffix_icon=ft.icons.SEARCH,
    )
    diagnostico_cie = ft.TextField(label="Codigo cie", multiline=True)
    diagnostico_cie_descripcion = ft.TextField(label="Descripcion", visible=True)
    diagnostico_cie_id = ft.TextField(visible=False)
    diagnostico_definitivo = ft.Dropdown(
        label="Estado",
        options=[
            ft.dropdown.DropdownOption("Definitivo"),
            ft.dropdown.DropdownOption("Presuntivo"),
        ],
    )

    cie_list = ft.ListView(expand=True, spacing=10)

    diagnostico_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Diagnóstico"),
        content=ft.Column(
            [
                diagnostico_buscador,
                ft.Container(
                    content=cie_list,
                    height=200,
                    width=900,
                    border=ft.border.all(1, ft.colors.GREY_300),
                ),
                diagnostico_cie_id,
                ft.Row(
                    [diagnostico_cie, diagnostico_definitivo],
                ),
                diagnostico_cie_descripcion,
            ],
            spacing=10,
        ),
        actions=[
            ft.TextButton("Continuar", on_click=lambda e: open_prescripciones_dialog()),
            ft.TextButton("Atrás", on_click=lambda e: open_signos_dialog()),
            ft.TextButton("Cancelar", on_click=close_all_dialogs),
        ],
    )

    # --- Diálogo 3: Prescripciones ---
    prescripciones_lista = ft.ListView(
        expand=True,
        spacing=10,
        height=200,  # Altura fija para el scroll
        auto_scroll=True,
    )
    presc_fecha = ft.TextField(label="Fecha", disabled=True)
    presc_medicamento = ft.TextField(label="Medicamento*")
    presc_dosis = ft.TextField(label="Dosis*")
    presc_indicaciones = ft.TextField(label="Indicaciones", multiline=True)
    presc_firmado_por = ft.TextField(label="Firmado por", disabled=True)

    # Definir botones de acción con visibilidad controlada
    btn_agregar = ft.ElevatedButton("Agregar Medicamento", on_click=agregar_medicamento)
    btn_guardar = ft.ElevatedButton(
        "Guardar cambios", on_click=agregar_medicamento, visible=False
    )
    btn_cancelar = ft.ElevatedButton(
        "Cancelar edición", on_click=lambda e: cancelar_edicion(e), visible=False
    )

    prescripciones_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Prescripciones Médicas"),
        content=ft.Column(
            [
                ft.Text("Medicamentos prescritos:", weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=prescripciones_lista, height=200, border=ft.border.all(1)
                ),
                ft.Divider(),
                ft.Text("Agregar nuevo medicamento:", weight=ft.FontWeight.BOLD),
                ft.Row([presc_medicamento, presc_dosis]),
                presc_indicaciones,
                # Usamos una fila fija para los botones de acción
                ft.Row(
                    [
                        presc_firmado_por,
                        presc_fecha,
                        btn_agregar,
                        btn_guardar,
                        btn_cancelar,
                    ],
                ),
            ],
            spacing=10,
            width=900,
        ),
        actions=[
            ft.TextButton("Continuar", on_click=lambda e: open_tratamientos_dialog()),
            ft.TextButton(
                "Atrás",
                on_click=lambda e, from_signos=False: open_diagnostico_dialog(
                    from_signos
                ),
            ),
            ft.TextButton("Cancelar", on_click=close_all_dialogs),
        ],
    )

    # --- Diálogo 4: Tratamientos ---
    tratamiento_descripcion = ft.TextField(label="Tratamiento*")
    tratamiento_fecha = ft.TextField(label="Fecha", disabled=True)

    tratamientos_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Tratamientos y Procedimientos"),
        content=ft.Column(
            [
                tratamiento_descripcion,
                tratamiento_fecha,
            ],
            spacing=10,
            width=900,
        ),
        actions=[
            ft.TextButton("Continuar", on_click=lambda e: open_consulta_dialog()),
            ft.TextButton("Atrás", on_click=lambda e: open_prescripciones_dialog()),
            ft.TextButton("Cancelar", on_click=close_all_dialogs),
        ],
    )

    # --- Diálogo 5: Nota Extra de Consulta ---
    consulta_nota = ft.TextField(label="Nota", multiline=True, min_lines=5)

    consulta_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Notas de Consulta"),
        content=ft.Column(
            [consulta_nota],
            spacing=10,
            width=900,
        ),
        actions=[
            ft.TextButton(
                "Guardar Todo",
                on_click=lambda e: save_full_consultation(
                    e, new_consult_paciente_id.value
                ),
            ),
            ft.TextButton("Atrás", on_click=lambda e: open_tratamientos_dialog()),
            ft.TextButton("Cancelar", on_click=close_all_dialogs),
        ],
    )

    # Componentes principales
    search_field = ft.TextField(
        label="Buscar paciente...",
        on_change=on_search,
        width=page.window_width * 0.9,
        suffix_icon=ft.icons.SEARCH,
    )

    pacientes_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

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
        "alert_dialog": alert_dialog,
        "search_field": search_field,
        "pacientes_list": pacientes_list,
        "pagination_controls": pagination_controls,
        "edit_id": edit_id,
        "edit_paciente": edit_paciente,
        "edit_motivo": edit_motivo,
        "edit_enfermedad": edit_enfermedad,
        "edit_dialog": edit_dialog,
        "new_consult_paciente_info": new_consult_paciente_info,
        "new_consult_paciente_id": new_consult_paciente_id,
        "new_consult_paciente_nombre": new_consult_paciente_nombre,
        "signos_dialog": signos_dialog,
        "signos_presion": signos_presion,
        "signos_frec_cardiaca": signos_frec_cardiaca,
        "signos_frec_respi": signos_frec_respi,
        "signos_temp": signos_temp,
        "signos_peso": signos_peso,
        "signos_talla": signos_talla,
        "diagnostico_buscador": diagnostico_buscador,
        "diagnostico_cie_id": diagnostico_cie_id,
        "diagnostico_cie": diagnostico_cie,
        "diagnostico_cie_descripcion": diagnostico_cie_descripcion,
        "diagnostico_definitivo": diagnostico_definitivo,
        "cie_list": cie_list,
        "diagnostico_dialog": diagnostico_dialog,
        "prescripciones_lista": prescripciones_lista,
        "presc_medicamento": presc_medicamento,
        "presc_dosis": presc_dosis,
        "presc_indicaciones": presc_indicaciones,
        "presc_firmado_por": presc_firmado_por,
        "presc_fecha": presc_fecha,
        "btn_agregar": btn_agregar,
        "btn_guardar": btn_guardar,
        "btn_cancelar": btn_cancelar,
        "prescripciones_dialog": prescripciones_dialog,
        "tratamiento_descripcion": tratamiento_descripcion,
        "tratamiento_fecha": tratamiento_fecha,
        "tratamientos_dialog": tratamientos_dialog,
        "consulta_nota": consulta_nota,
        "consulta_dialog": consulta_dialog,
    }
