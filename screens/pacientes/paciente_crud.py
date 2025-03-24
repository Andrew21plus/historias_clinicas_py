import unicodedata

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
        raise ValueError("Error: La cédula ya está registrada.")
    if historia_clinica_existe(num_historia_clinica):
        raise ValueError("Error: El número de historia clínica ya está registrado.")
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
        raise ValueError("Error: La cédula ya está registrada.")
    if historia_clinica_existe(num_historia_clinica, exclude_id=id_paciente):
        raise ValueError("Error: El número de historia clínica ya está registrado.")
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
