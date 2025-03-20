from services.historia_clinica_service import (
    get_historias_clinicas_by_usuario,
    add_historia_clinica,
    update_historia_clinica,
    delete_historia_clinica,
)
from services.paciente_service import get_paciente

def obtener_historias_clinicas(id_usuario, search_query=""):
    """Obtiene todas las historias clínicas filtradas por id_usuario y search_query."""
    historias = get_historias_clinicas_by_usuario(id_usuario)
    if search_query:
        historias = [
            h for h in historias
            if search_query.lower() in get_paciente(h.id_paciente).nombre.lower() or
               search_query.lower() in get_paciente(h.id_paciente).apellido.lower()
        ]
    return historias

def agregar_historia_clinica(id_paciente, motivo_consulta, enfermedad_actual, id_usuario):
    """Agrega una nueva historia clínica."""
    return add_historia_clinica(id_paciente, motivo_consulta, enfermedad_actual, id_usuario)

def actualizar_historia_clinica(id_historia, motivo_consulta, enfermedad_actual, id_usuario):
    """Actualiza una historia clínica existente."""
    return update_historia_clinica(id_historia, motivo_consulta, enfermedad_actual, id_usuario)

def eliminar_historia_clinica(id_historia):
    """Elimina una historia clínica."""
    return delete_historia_clinica(id_historia)

def paciente_tiene_historia(id_paciente, historias):
    """Verifica si un paciente ya tiene una historia clínica."""
    return any(h.id_paciente == id_paciente for h in historias)