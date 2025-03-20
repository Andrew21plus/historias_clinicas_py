from services.antecedente_medico_service import (
    add_antecedente_medico,
    update_antecedente_medico,
    delete_antecedente_medico,
    get_antecedentes_medicos_by_paciente,
)
from services.signo_vital_service import (
    add_signo_vital,
    update_signo_vital,
    delete_signo_vital,
    get_signos_vitales_by_paciente,
)
from services.paciente_service import get_pacientes_by_id_usuario

def obtener_tamizajes(id_usuario, search_query=""):
    """Obtiene todos los tamizajes (antecedentes médicos y signos vitales) para un usuario."""
    all_tamizajes = []

    # Obtener todos los pacientes asociados al usuario
    pacientes = get_pacientes_by_id_usuario(id_usuario)

    # Obtener antecedentes médicos y signos vitales para cada paciente
    for paciente in pacientes:
        antecedentes = get_antecedentes_medicos_by_paciente(paciente.id_paciente, id_usuario)
        signos_vitales = get_signos_vitales_by_paciente(paciente.id_paciente, id_usuario)

        # Si el paciente tiene antecedentes o signos, agregarlo a la lista
        if antecedentes or signos_vitales:
            all_tamizajes.append({
                "paciente": paciente,
                "antecedentes": antecedentes,
                "signos_vitales": signos_vitales
            })

    # Filtrar tamizajes por nombre o apellido del paciente (si hay una búsqueda)
    if search_query:
        all_tamizajes = [
            t for t in all_tamizajes
            if search_query.lower() in t["paciente"].nombre.lower() or
            search_query.lower() in t["paciente"].apellido.lower()
        ]

    return all_tamizajes

def eliminar_tamizaje(paciente, id_usuario):
    """Elimina todos los antecedentes médicos y signos vitales asociados al paciente."""
    # Eliminar todos los antecedentes médicos del paciente
    antecedentes = get_antecedentes_medicos_by_paciente(paciente.id_paciente, id_usuario)
    for antecedente in antecedentes:
        delete_antecedente_medico(antecedente.id_antecedente)

    # Eliminar todos los signos vitales del paciente
    signos_vitales = get_signos_vitales_by_paciente(paciente.id_paciente, id_usuario)
    for signo in signos_vitales:
        delete_signo_vital(signo.id_signo)

def agregar_antecedente_medico(paciente_id, tipo, descripcion):
    """Agrega un nuevo antecedente médico."""
    if not tipo or not descripcion:
        raise ValueError("El tipo y la descripción del antecedente médico no pueden ser nulos.")
    add_antecedente_medico(paciente_id, tipo, descripcion)

def agregar_signo_vital(paciente_id, fecha, presion_arterial, frecuencia_cardiaca, frecuencia_respiratoria, temperatura, peso, talla):
    """Agrega un nuevo signo vital."""
    add_signo_vital(paciente_id, fecha, presion_arterial, frecuencia_cardiaca, frecuencia_respiratoria, temperatura, peso, talla)

def agregar_tamizaje(paciente_id, tipo, descripcion, fecha, presion_arterial, frecuencia_cardiaca, frecuencia_respiratoria, temperatura, peso, talla):
    """Agrega un nuevo tamizaje (antecedente médico y signo vital)."""
    if not tipo or not descripcion:
        raise ValueError("El tipo y la descripción del antecedente médico no pueden ser nulos.")
    agregar_antecedente_medico(paciente_id, tipo, descripcion)
    agregar_signo_vital(paciente_id, fecha, presion_arterial, frecuencia_cardiaca, frecuencia_respiratoria, temperatura, peso, talla)

def actualizar_tamizaje(tamizaje, tipo=None, descripcion=None, fecha=None, presion_arterial=None, frecuencia_cardiaca=None, frecuencia_respiratoria=None, temperatura=None, peso=None, talla=None):
    """Actualiza un tamizaje existente (antecedente médico o signo vital)."""
    if hasattr(tamizaje, "tipo"):  # Si es un antecedente médico
        update_antecedente_medico(tamizaje.id_antecedente, tipo, descripcion)
    else:  # Si es un signo vital
        update_signo_vital(tamizaje.id_signo, fecha, presion_arterial, frecuencia_cardiaca, frecuencia_respiratoria, temperatura, peso, talla)

def paciente_tiene_tamizaje(paciente_id, all_tamizajes):
    """Verifica si un paciente ya tiene un tamizaje."""
    for tamizaje in all_tamizajes:
        if tamizaje["paciente"].id_paciente == paciente_id:
            return True
    return False