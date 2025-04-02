import flet as ft
import re
from datetime import datetime


# Funciones de validación auxiliares para signos vitales
def validar_presion_arterial(valor):
    """Valida el formato de la presión arterial (ej: 120/80)."""
    return re.match(r"^\d{2,3}\/\d{2,3}$", valor) is not None


def validar_numero_entero(valor, min_val=None, max_val=None):
    """Valida que el valor sea un número entero y esté dentro del rango opcional."""
    try:
        num = int(valor)
        if min_val is not None and num < min_val:
            return False
        if max_val is not None and num > max_val:
            return False
        return True
    except ValueError:
        return False


def validar_numero_decimal(valor, min_val=None, max_val=None):
    """Valida que el valor sea un número decimal y esté dentro del rango opcional."""
    try:
        num = float(valor)
        if min_val is not None and num < min_val:
            return False
        if max_val is not None and num > max_val:
            return False
        return True
    except ValueError:
        return False


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
    agregar_diagnostico,
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
    # Funciones de validación para signos vitales
    def validar_signos():
        valido = True

        # Validar presión arterial
        if signos_presion.value and not validar_presion_arterial(signos_presion.value):
            signos_presion.error_text = "Formato inválido (ej: 120/80)"
            valido = False
        else:
            signos_presion.error_text = None

        # Validar frecuencia cardíaca
        if signos_frec_cardiaca.value and not validar_numero_entero(
            signos_frec_cardiaca.value, 30, 200
        ):
            signos_frec_cardiaca.error_text = "Debe ser entre 30 y 200 lpm"
            valido = False
        else:
            signos_frec_cardiaca.error_text = None

        # Validar frecuencia respiratoria
        if signos_frec_respi.value and not validar_numero_entero(
            signos_frec_respi.value, 10, 60
        ):
            signos_frec_respi.error_text = "Debe ser entre 10 y 60 rpm"
            valido = False
        else:
            signos_frec_respi.error_text = None

        # Validar temperatura
        if signos_temp.value and not validar_numero_decimal(
            signos_temp.value, 35.0, 42.0
        ):
            signos_temp.error_text = "Debe ser entre 35.0 y 42.0 °C"
            valido = False
        else:
            signos_temp.error_text = None

        # Validar peso
        if signos_peso.value and not validar_numero_decimal(
            signos_peso.value, 0.5, 300
        ):
            signos_peso.error_text = "Debe ser entre 0.5 y 300 kg"
            valido = False
        else:
            signos_peso.error_text = None

        # Validar talla
        if signos_talla.value and not validar_numero_decimal(
            signos_talla.value, 30, 250
        ):
            signos_talla.error_text = "Debe ser entre 30 y 250 cm"
            valido = False
        else:
            signos_talla.error_text = None

        page.update()
        return valido

    # Función wrapper para continuar con validación
    def continuar_con_signos(e):
        if validar_signos():
            open_diagnostico_dialog()
        else:
            alert_dialog.content = ft.Text(
                "Por favor corrija los errores en los signos vitales"
            )
            alert_dialog.open = True
            page.update()

    # Campos de signos vitales con validación en tiempo real
    signos_presion = ft.TextField(
        label="Presión Arterial (ej: 120/80)",
        hint_text="Ej: 120/80",
        on_change=lambda e: (
            (
                setattr(signos_presion, "error_text", None)
                if validar_presion_arterial(signos_presion.value)
                or not signos_presion.value
                else setattr(
                    signos_presion, "error_text", "Formato inválido (ej: 120/80)"
                )
            ),
            page.update(),
        ),
    )

    signos_frec_cardiaca = ft.TextField(
        label="Frecuencia Cardíaca (lpm)",
        hint_text="Ej: 72",
        on_change=lambda e: (
            (
                setattr(signos_frec_cardiaca, "error_text", None)
                if validar_numero_entero(signos_frec_cardiaca.value, 30, 200)
                or not signos_frec_cardiaca.value
                else setattr(
                    signos_frec_cardiaca, "error_text", "Debe ser entre 30 y 200"
                )
            ),
            page.update(),
        ),
    )

    signos_frec_respi = ft.TextField(
        label="Frecuencia Respiratoria (rpm)",
        hint_text="Ej: 16",
        on_change=lambda e: (
            (
                setattr(signos_frec_respi, "error_text", None)
                if validar_numero_entero(signos_frec_respi.value, 10, 60)
                or not signos_frec_respi.value
                else setattr(signos_frec_respi, "error_text", "Debe ser entre 10 y 60")
            ),
            page.update(),
        ),
    )

    signos_temp = ft.TextField(
        label="Temperatura (°C)",
        hint_text="Ej: 36.5",
        on_change=lambda e: (
            (
                setattr(signos_temp, "error_text", None)
                if validar_numero_decimal(signos_temp.value, 35.0, 42.0)
                or not signos_temp.value
                else setattr(signos_temp, "error_text", "Debe ser entre 35.0 y 42.0")
            ),
            page.update(),
        ),
    )

    signos_peso = ft.TextField(
        label="Peso (kg)",
        hint_text="Ej: 68.5",
        on_change=lambda e: (
            (
                setattr(signos_peso, "error_text", None)
                if validar_numero_decimal(signos_peso.value, 0.5, 300)
                or not signos_peso.value
                else setattr(signos_peso, "error_text", "Debe ser entre 0.5 y 300")
            ),
            page.update(),
        ),
    )

    signos_talla = ft.TextField(
        label="Talla (cm)",
        hint_text="Ej: 170",
        on_change=lambda e: (
            (
                setattr(signos_talla, "error_text", None)
                if validar_numero_decimal(signos_talla.value, 30, 250)
                or not signos_talla.value
                else setattr(signos_talla, "error_text", "Debe ser entre 30 y 250")
            ),
            page.update(),
        ),
    )

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
            ft.TextButton("Continuar", on_click=continuar_con_signos),
            ft.TextButton("Cancelar", on_click=close_all_dialogs),
        ],
    )

    # --- Diálogo 2: Diagnóstico ---
    diagnostico_buscador = ft.TextField(
        label="Buscar CIE...",
        on_change=on_search_cie,
        width=page.window_width * 0.9,
        suffix_icon=ft.icons.SEARCH,
    )

    # Botón para buscar externamente (inicialmente oculto)
    btn_buscar_externo = ft.ElevatedButton(
        "Buscar en cpockets.com",
        on_click=lambda _: page.launch_url("https://cpockets.com/cie10"),
        icon=ft.icons.PUBLIC,
        visible=False,
    )

    diagnostico_cie = ft.TextField(label="Código CIE")
    diagnostico_cie_descripcion = ft.TextField(label="Descripción", multiline=True)
    diagnostico_cie_id = ft.TextField(visible=False)
    diagnostico_definitivo = ft.Dropdown(
        label="Estado",
        options=[
            ft.dropdown.Option("Definitivo"),
            ft.dropdown.Option("Presuntivo"),
        ],
    )

    cie_list = ft.ListView(expand=True, spacing=10, height=200, auto_scroll=True)
    diagnostico_lista = ft.ListView(
        expand=True, spacing=10, height=200, auto_scroll=True
    )
    btn_agregar_diagnostico = ft.ElevatedButton(
        "Agregar Diagnóstico", on_click=agregar_diagnostico
    )

    diagnostico_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Diagnóstico"),
        content=ft.Column(
            [
                diagnostico_buscador,
                ft.Row(
                    controls=[
                        ft.Container(
                            content=cie_list,
                            height=200,
                            width=450,
                            border=ft.border.all(1, ft.colors.GREY_300),
                            padding=5,
                        ),
                        ft.Container(
                            content=diagnostico_lista,
                            height=200,
                            width=450,
                            border=ft.border.all(1, ft.colors.GREY_300),
                            padding=5,
                        ),
                    ],
                    spacing=10,
                ),
                btn_buscar_externo,
                diagnostico_cie_id,
                ft.Row([diagnostico_cie, diagnostico_definitivo]),
                diagnostico_cie_descripcion,
                btn_agregar_diagnostico,
            ],
            spacing=10,
            width=900,
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
        "diagnostico_lista": diagnostico_lista,
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
        "btn_buscar_externo": btn_buscar_externo,
    }
