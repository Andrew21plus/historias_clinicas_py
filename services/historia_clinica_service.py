from dao.historia_clinica_dao import (
    get_all_historias_clinicas,
    add_historia_clinica as add_historia_clinica_dao,
    update_historia_clinica as update_historia_clinica_dao,
    delete_historia_clinica as delete_historia_clinica_dao,
    get_historia_clinica_by_paciente,
    get_historias_clinicas_by_usuario as get_historias_clinicas_by_usuario_dao,
)


def get_historias_clinicas():
    return get_all_historias_clinicas()


def paciente_tiene_historia(id_paciente):
    """Verifica si un paciente ya tiene una historia clínica"""
    return get_historia_clinica_by_paciente(id_paciente) is not None


def add_historia_clinica(id_paciente, motivo_consulta, enfermedad_actual, id_usuario):
    """Agrega una nueva historia clínica si el paciente no tiene una"""
    if paciente_tiene_historia(id_paciente):
        raise ValueError("El paciente ya tiene una historia clínica.")
    add_historia_clinica_dao(
        id_paciente, motivo_consulta, enfermedad_actual, id_usuario
    )


def update_historia_clinica(
    id_historia, motivo_consulta, enfermedad_actual, id_usuario
):
    update_historia_clinica_dao(id_historia, motivo_consulta, enfermedad_actual)


def delete_historia_clinica(id_historia):
    delete_historia_clinica_dao(id_historia)


def get_historias_clinicas_by_usuario(id_usuario):
    """Obtiene todas las historias clínicas asociadas a un usuario específico"""
    return get_historias_clinicas_by_usuario_dao(id_usuario)
