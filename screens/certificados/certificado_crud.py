from services.diagnostico_service import get_diagnosticos_by_consulta
from services.paciente_service import get_pacientes_by_id_usuario

def buscar_pacientes(id_usuario, search_query=""):
    """Busca pacientes con filtro por nombre/apellido"""
    pacientes = get_pacientes_by_id_usuario(id_usuario)
    if search_query:
        return [p for p in pacientes if search_query.lower() in f"{p.nombre} {p.apellido}".lower()]
    return pacientes

def obtener_diagnosticos_paciente(id_paciente, fecha_consulta):
    """Obtiene diagnósticos previos del paciente"""
    return get_diagnosticos_by_consulta(id_paciente, fecha_consulta)
