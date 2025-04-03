import flet as ft
import re
from datetime import datetime

# Funciones de validación auxiliares (se añaden sin modificar lo existente)
def validar_fecha(formato_fecha):
    """Valida que la fecha tenga el formato dd-mm-yyyy y sea una fecha válida."""
    if not re.match(r"^\d{2}-\d{2}-\d{4}$", formato_fecha):
        return False
    try:
        dia, mes, anio = map(int, formato_fecha.split("-"))
        datetime(year=anio, month=mes, day=dia)
        return True
    except ValueError:
        return False

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

def validar_presion_arterial(valor):
    """Valida el formato de la presión arterial (ej: 120/80)."""
    return re.match(r"^\d{2,3}\/\d{2,3}$", valor) is not None

def crear_tamizaje_ui(page, save_edit, on_search, change_page):
    """Crea la interfaz de usuario para la gestión de tamizajes."""
    # Texto dinámico para mostrar el número de página
    page_number_text = ft.Text(f"Página 1")

    # Diálogo de alerta para mostrar errores (se mantiene igual)
    alert_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row(
            controls=[
                ft.Icon(ft.icons.WARNING_AMBER, color=ft.colors.AMBER),
                ft.Text(" Advertencia", weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        content=ft.Text(""),
        actions=[
            ft.TextButton(
                "OK",
                on_click=lambda e: setattr(alert_dialog, "open", False) or page.update(),
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Campo de búsqueda de tamizajes (se mantiene igual)
    search_field = ft.TextField(
        label="Buscar por nombre o apellido del paciente",
        on_change=on_search,
        expand=True,
        suffix=ft.IconButton(ft.icons.SEARCH, on_click=on_search),
    )

    # Lista de tamizajes (se mantiene igual)
    tamizajes_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    # Funciones de validación para los campos de edición (nuevas)
    def validar_fecha_campo(campo_fecha):
        if campo_fecha.value and not validar_fecha(campo_fecha.value):
            campo_fecha.error_text = "Formato inválido. Use dd-mm-yyyy."
            page.update()
            return False
        campo_fecha.error_text = None
        page.update()
        return True

    def validar_presion_arterial_campo(campo_presion):
        if campo_presion.value and not validar_presion_arterial(campo_presion.value):
            campo_presion.error_text = "Formato inválido (ej: 120/80)"
            page.update()
            return False
        campo_presion.error_text = None
        page.update()
        return True

    def validar_entero_campo(campo, min_val, max_val):
        if campo.value and not validar_numero_entero(campo.value, min_val, max_val):
            campo.error_text = f"Debe ser un número entero entre {min_val} y {max_val}"
            page.update()
            return False
        campo.error_text = None
        page.update()
        return True

    def validar_decimal_campo(campo, min_val, max_val):
        if campo.value and not validar_numero_decimal(campo.value, min_val, max_val):
            campo.error_text = f"Debe ser un número entre {min_val} y {max_val}"
            page.update()
            return False
        campo.error_text = None
        page.update()
        return True

    def validar_descripcion_campo(campo):
        if not campo.value:
            campo.error_text = "La descripción es requerida"
            page.update()
            return False
        campo.error_text = None
        page.update()
        return True

    # Función para validar todos los campos antes de guardar (nueva)
    def validar_todo():
        valido = True
        
        # Determinar si estamos editando antecedentes o signos vitales
        es_antecedente = edit_tipo.visible if hasattr(edit_tipo, 'visible') else True
        es_signo_vital = edit_fecha.visible if hasattr(edit_fecha, 'visible') else True
        
        # Validar campos de antecedentes solo si son visibles
        if es_antecedente:
            if not edit_tipo.value:
                edit_tipo.error_text = "Seleccione un tipo de antecedente"
                valido = False
            else:
                edit_tipo.error_text = None
                
            valido = validar_descripcion_campo(edit_descripcion) and valido
        
        # Validar campos de signos vitales solo si son visibles
        if es_signo_vital:
            if edit_presion_arterial.value:
                valido = validar_presion_arterial_campo(edit_presion_arterial) and valido
            else:
                edit_presion_arterial.error_text = "Este campo es requerido"
                valido = False
                
            if edit_frecuencia_cardiaca.value:
                valido = validar_entero_campo(edit_frecuencia_cardiaca, 30, 200) and valido
            else:
                edit_frecuencia_cardiaca.error_text = "Este campo es requerido"
                valido = False
                
            if edit_frecuencia_respiratoria.value:
                valido = validar_entero_campo(edit_frecuencia_respiratoria, 10, 60) and valido
            else:
                edit_frecuencia_respiratoria.error_text = "Este campo es requerido"
                valido = False
                
            if edit_temperatura.value:
                valido = validar_decimal_campo(edit_temperatura, 35.0, 42.0) and valido
            else:
                edit_temperatura.error_text = "Este campo es requerido"
                valido = False
                
            if edit_peso.value:
                valido = validar_decimal_campo(edit_peso, 0.5, 300) and valido
            else:
                edit_peso.error_text = "Este campo es requerido"
                valido = False
                
            if edit_talla.value:
                valido = validar_decimal_campo(edit_talla, 30, 250) and valido
            else:
                edit_talla.error_text = "Este campo es requerido"
                valido = False
                
        return valido

    # Wrapper para save_edit que incluye validación (nuevo)
    def save_edit_validado(e):
        if validar_todo():
            save_edit(e)
        else:
            alert_dialog.content = ft.Text("Por favor corrija los errores en el formulario")
            alert_dialog.open = True
            page.update()

    # Diálogo de edición (se mantiene igual en estructura, solo se añaden validaciones)
    edit_id = ft.TextField(label="ID Tamizaje", disabled=True)
    edit_tipo = ft.Dropdown(
        label="Tipo de antecedente médico",
        options=[
            ft.dropdown.Option("Personal"),
            ft.dropdown.Option("Familiar"),
        ],
    )
    edit_descripcion = ft.TextField(
        label="Descripción del antecedente médico",
        on_change=lambda e: validar_descripcion_campo(edit_descripcion)
    )
    edit_fecha = ft.TextField(
        label="Fecha del signo vital",
        read_only=True,
    )
    edit_presion_arterial = ft.TextField(
        label="Presión arterial",
        on_change=lambda e: validar_presion_arterial_campo(edit_presion_arterial)
    )
    edit_frecuencia_cardiaca = ft.TextField(
        label="Frecuencia cardíaca",
        on_change=lambda e: validar_entero_campo(edit_frecuencia_cardiaca, 30, 200)
    )
    edit_frecuencia_respiratoria = ft.TextField(
        label="Frecuencia respiratoria",
        on_change=lambda e: validar_entero_campo(edit_frecuencia_respiratoria, 10, 60)
    )
    edit_temperatura = ft.TextField(
        label="Temperatura",
        on_change=lambda e: validar_decimal_campo(edit_temperatura, 35.0, 42.0)
    )
    edit_peso = ft.TextField(
        label="Peso",
        on_change=lambda e: validar_decimal_campo(edit_peso, 0.5, 300)
    )
    edit_talla = ft.TextField(
        label="Talla",
        on_change=lambda e: validar_decimal_campo(edit_talla, 30, 250)
    )
    
    # Diálogo de edición (se mantiene exactamente igual)
    edit_dialog = ft.AlertDialog(
        title=ft.Text("Editar Tamizaje"),
        content=ft.Column(
            [
                edit_id,
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
            ft.TextButton("Guardar", on_click=save_edit_validado),  # Se cambia a save_edit_validado
            ft.TextButton(
                "Cancelar",
                on_click=lambda e: setattr(edit_dialog, "open", False) or page.update(),
            ),
        ],
    )

    # Controles de paginación (se mantienen igual)
    pagination_controls = ft.Row(
        [
            ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: change_page(-1)),
            page_number_text,
            ft.IconButton(ft.icons.ARROW_FORWARD, on_click=lambda e: change_page(1)),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Retorno del diccionario (se mantiene exactamente igual)
    return {
        "page_number_text": page_number_text,
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