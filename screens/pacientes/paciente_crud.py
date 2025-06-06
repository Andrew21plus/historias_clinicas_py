import unicodedata
from datetime import datetime
from services.paciente_service import (
    get_pacientes_by_id_usuario,
    add_paciente,
    update_paciente,
    delete_paciente,
    cedula_existe,
    historia_clinica_existe,
)
from utils.formulario_paciente import (
    validar_cedula_ecuatoriana,
    validar_fecha,
)


def obtener_pacientes(id_usuario, search_query=""):
    """Obtiene todos los pacientes filtrados por id_usuario y search_query.
    Maneja caracteres especiales y acentos en las búsquedas."""

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

    pacientes = get_pacientes_by_id_usuario(id_usuario)

    if search_query:
        # Normalizamos la query de búsqueda
        normalized_query = normalize_string(search_query)

        pacientes = [
            p
            for p in pacientes
            if normalized_query in normalize_string(p.nombre)
            or normalized_query in normalize_string(p.apellido)
        ]

    return pacientes


def agregar_paciente(
    id_paciente,
    nombre,
    apellido,
    sexo,
    fecha_nacimiento,
    num_historia_clinica,
    foto,
    id_usuario,
):
    """Agrega un nuevo paciente."""
    if not validar_cedula_ecuatoriana(id_paciente):
        raise ValueError(
            "Cédula inválida. Por favor, ingrese una cédula ecuatoriana válida."
        )
    if not validar_fecha(fecha_nacimiento):
        raise ValueError("Formato de fecha inválido. Use dd-mm-yyyy.")
    if cedula_existe(id_paciente):
        raise ValueError("La cédula ya está registrada.")
    if historia_clinica_existe(num_historia_clinica):
        raise ValueError("El número de historia clínica ya está registrado.")
    return add_paciente(
        id_paciente,
        nombre,
        apellido,
        sexo,
        fecha_nacimiento,
        num_historia_clinica,
        foto,
        id_usuario,
    )


def actualizar_paciente(
    id_paciente,
    nombre,
    apellido,
    sexo,
    fecha_nacimiento,
    num_historia_clinica,
    id_usuario,
    foto,
):
    """Actualiza un paciente existente."""
    if not validar_cedula_ecuatoriana(id_paciente):
        raise ValueError(
            "Cédula inválida. Por favor, ingrese una cédula ecuatoriana válida."
        )
    if not validar_fecha(fecha_nacimiento):
        raise ValueError("Formato de fecha inválido. Use dd-mm-yyyy.")
    if cedula_existe(id_paciente, exclude_id=id_paciente):
        raise ValueError("La cédula ya está registrada.")
    if historia_clinica_existe(num_historia_clinica, exclude_id=id_paciente):
        raise ValueError("El número de historia clínica ya está registrado.")
    return update_paciente(
        id_paciente,
        nombre,
        apellido,
        sexo,
        fecha_nacimiento,
        num_historia_clinica,
        id_usuario,
        foto,
    )


def eliminar_paciente(id_paciente):
    """Elimina un paciente."""
    return delete_paciente(id_paciente)

def calcular_edad(fecha_nacimiento_str, formato_fecha="%d-%m-%Y"):
    """Calcula la edad a partir de una fecha de nacimiento.
    
    Args:
        fecha_nacimiento_str (str): Fecha en formato string
        formato_fecha (str): Formato de la fecha (por defecto dd-mm-yyyy)
    
    Returns:
        str: Edad en formato "X años" o "Fecha inválida" si hay error
    """
    try:
        fecha_nac = datetime.strptime(fecha_nacimiento_str, formato_fecha)
        hoy = datetime.now()
        edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
        return f"{edad} años"
    except (ValueError, TypeError):
        return "Fecha inválida"