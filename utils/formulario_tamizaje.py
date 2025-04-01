import flet as ft
import re
from datetime import datetime


def paciente_tiene_tamizaje(paciente_id, all_tamizajes):
    """Verifica si un paciente ya tiene un tamizaje."""
    for tamizaje in all_tamizajes:
        if tamizaje["paciente"].id_paciente == paciente_id:
            return True
    return False


def validar_fecha(formato_fecha):
    # Expresión regular para validar el formato dd-mm-yyyy
    if not re.match(r"^\d{2}-\d{2}-\d{4}$", formato_fecha):
        return False

    # Verificar si la fecha es válida
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


def crear_formulario_tamizaje(
    page, add_tamizaje_clicked, on_paciente_search, select_paciente, all_tamizajes
):
    ancho_campo = 300
    
    # Función para validar todos los campos antes de permitir el guardado
    def validar_campos():
        campos_validos = True
        
        # Validar paciente seleccionado
        if not tamizaje_paciente.value:
            tamizaje_paciente.error_text = "Debe seleccionar un paciente"
            campos_validos = False
        else:
            tamizaje_paciente.error_text = None
        
        # Validar tipo de antecedente
        if not tamizaje_tipo.value:
            tamizaje_tipo.error_text = "Seleccione un tipo de antecedente"
            campos_validos = False
        else:
            tamizaje_tipo.error_text = None
        
        # Validar descripción
        if not tamizaje_descripcion.value:
            tamizaje_descripcion.error_text = "La descripción es requerida"
            campos_validos = False
        else:
            tamizaje_descripcion.error_text = None
        
        # Validar fecha
        if not tamizaje_fecha.value or not validar_fecha(tamizaje_fecha.value):
            tamizaje_fecha.error_text = "Fecha inválida (use formato dd-mm-yyyy)"
            campos_validos = False
        else:
            tamizaje_fecha.error_text = None
        
        # Validar presión arterial
        if tamizaje_presion_arterial.value and not validar_presion_arterial(tamizaje_presion_arterial.value):
            tamizaje_presion_arterial.error_text = "Formato inválido (ej: 120/80)"
            campos_validos = False
        else:
            tamizaje_presion_arterial.error_text = None
        
        # Validar frecuencia cardíaca
        if tamizaje_frecuencia_cardiaca.value and not validar_numero_entero(tamizaje_frecuencia_cardiaca.value, 30, 200):
            tamizaje_frecuencia_cardiaca.error_text = "Debe ser un número entre 30 y 200"
            campos_validos = False
        else:
            tamizaje_frecuencia_cardiaca.error_text = None
        
        # Validar frecuencia respiratoria
        if tamizaje_frecuencia_respiratoria.value and not validar_numero_entero(tamizaje_frecuencia_respiratoria.value, 10, 60):
            tamizaje_frecuencia_respiratoria.error_text = "Debe ser un número entre 10 y 60"
            campos_validos = False
        else:
            tamizaje_frecuencia_respiratoria.error_text = None
        
        # Validar temperatura
        if tamizaje_temperatura.value and not validar_numero_decimal(tamizaje_temperatura.value, 35.0, 42.0):
            tamizaje_temperatura.error_text = "Debe ser un número entre 35.0 y 42.0"
            campos_validos = False
        else:
            tamizaje_temperatura.error_text = None
        
        # Validar peso
        if tamizaje_peso.value and not validar_numero_decimal(tamizaje_peso.value, 0.5, 300):
            tamizaje_peso.error_text = "Debe ser un número entre 0.5 y 300"
            campos_validos = False
        else:
            tamizaje_peso.error_text = None
        
        # Validar talla
        if tamizaje_talla.value and not validar_numero_decimal(tamizaje_talla.value, 30, 250):
            tamizaje_talla.error_text = "Debe ser un número entre 30 y 250"
            campos_validos = False
        else:
            tamizaje_talla.error_text = None
        
        page.update()
        return campos_validos
    
    # Modificar la función add_tamizaje_clicked para incluir validaciones
    def add_tamizaje_clicked_wrapper(e):
        if validar_campos():
            add_tamizaje_clicked(e)
    
    # Campos del formulario
    tamizaje_paciente = ft.TextField(
        label="ID Paciente", 
        width=200, 
        read_only=True
    )
    
    tamizaje_tipo = ft.Dropdown(
        label="Tipo de antecedente médico",
        options=[
            ft.dropdown.DropdownOption("Personal"),
            ft.dropdown.DropdownOption("Familiar"),
        ],
        width=ancho_campo,
    )
    
    tamizaje_descripcion = ft.TextField(
        label="Descripción del antecedente médico", 
        expand=True
    )
    
    # Establecer fecha actual como valor por defecto
    fecha_actual = datetime.now().strftime("%d-%m-%Y")
    tamizaje_fecha = ft.TextField(
        label="Fecha del signo vital (dd-mm-yyyy)",
        width=ancho_campo,
        value=fecha_actual,
        hint_text="Ej: 15-05-1990",
        on_change=lambda e: validar_fecha_campo(tamizaje_fecha),
    )
    
    tamizaje_presion_arterial = ft.TextField(
        label="Presión arterial (ej: 120/80)", 
        expand=True,
        hint_text="Ej: 120/80",
        on_change=lambda e: validar_presion_arterial_campo(tamizaje_presion_arterial)
    )
    
    tamizaje_frecuencia_cardiaca = ft.TextField(
        label="Frecuencia cardíaca (lpm)", 
        expand=True,
        hint_text="Ej: 72",
        on_change=lambda e: validar_entero_campo(tamizaje_frecuencia_cardiaca, 30, 200)
    )
    
    tamizaje_frecuencia_respiratoria = ft.TextField(
        label="Frecuencia respiratoria (rpm)", 
        expand=True,
        hint_text="Ej: 16",
        on_change=lambda e: validar_entero_campo(tamizaje_frecuencia_respiratoria, 10, 60)
    )
    
    tamizaje_temperatura = ft.TextField(
        label="Temperatura (°C)", 
        expand=True,
        hint_text="Ej: 36.5",
        on_change=lambda e: validar_decimal_campo(tamizaje_temperatura, 35.0, 42.0)
    )
    
    tamizaje_peso = ft.TextField(
        label="Peso (kg)", 
        expand=True,
        hint_text="Ej: 68.5",
        on_change=lambda e: validar_decimal_campo(tamizaje_peso, 0.5, 300)
    )
    
    tamizaje_talla = ft.TextField(
        label="Talla (cm)", 
        expand=True,
        hint_text="Ej: 170",
        on_change=lambda e: validar_decimal_campo(tamizaje_talla, 30, 250)
    )

    # Funciones de validación por campo
    def validar_fecha_campo(campo_fecha):
        if campo_fecha.value:
            if not validar_fecha(campo_fecha.value):
                campo_fecha.error_text = "Formato inválido. Use dd-mm-yyyy."
            else:
                campo_fecha.error_text = None
        page.update()
    
    def validar_presion_arterial_campo(campo_presion):
        if campo_presion.value:
            if not validar_presion_arterial(campo_presion.value):
                campo_presion.error_text = "Formato inválido (ej: 120/80)"
            else:
                campo_presion.error_text = None
        page.update()
    
    def validar_entero_campo(campo, min_val, max_val):
        if campo.value:
            if not validar_numero_entero(campo.value, min_val, max_val):
                campo.error_text = f"Debe ser un número entero entre {min_val} y {max_val}"
            else:
                campo.error_text = None
        page.update()
    
    def validar_decimal_campo(campo, min_val, max_val):
        if campo.value:
            if not validar_numero_decimal(campo.value, min_val, max_val):
                campo.error_text = f"Debe ser un número entre {min_val} y {max_val}"
            else:
                campo.error_text = None
        page.update()

    # Campo de búsqueda de pacientes
    paciente_search_field = ft.TextField(
        label="Buscar paciente por nombre o apellido",
        on_change=on_paciente_search,
        expand=True,
    )
    paciente_results = ft.Column()

    # Botón de agregar con validación
    agregar_button = ft.ElevatedButton(
        "Agregar", 
        on_click=add_tamizaje_clicked_wrapper
    )

    # Crear el contenido del formulario
    form_content = ft.Column(
        [
            ft.Divider(height=10, color=ft.colors.TRANSPARENT),
            paciente_search_field,
            paciente_results,
            ft.Row(
                [tamizaje_paciente, tamizaje_tipo, tamizaje_descripcion], 
                spacing=15
            ),
            ft.Row(
                [
                    tamizaje_fecha,
                    tamizaje_presion_arterial,
                    tamizaje_frecuencia_cardiaca,
                ],
                spacing=15,
            ),
            ft.Row(
                [
                    tamizaje_frecuencia_respiratoria,
                    tamizaje_temperatura,
                    tamizaje_peso,
                    tamizaje_talla,
                ],
                spacing=15,
            ),
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
            ft.Row([agregar_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
        ],
        spacing=10,
    )

    return {
        "form_content": form_content,
        "tamizaje_paciente": tamizaje_paciente,
        "tamizaje_tipo": tamizaje_tipo,
        "tamizaje_descripcion": tamizaje_descripcion,
        "tamizaje_fecha": tamizaje_fecha,
        "tamizaje_presion_arterial": tamizaje_presion_arterial,
        "tamizaje_frecuencia_cardiaca": tamizaje_frecuencia_cardiaca,
        "tamizaje_frecuencia_respiratoria": tamizaje_frecuencia_respiratoria,
        "tamizaje_temperatura": tamizaje_temperatura,
        "tamizaje_peso": tamizaje_peso,
        "tamizaje_talla": tamizaje_talla,
        "paciente_search_field": paciente_search_field,
        "paciente_results": paciente_results,
        "agregar_button": agregar_button,
        "paciente_tiene_tamizaje": paciente_tiene_tamizaje,
        "validar_campos": validar_campos,
    }