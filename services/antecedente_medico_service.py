from dao.antecedente_medico_dao import (
    get_all_antecedentes_medicos, 
    add_antecedente_medico as add_antecedente_medico_dao, 
    update_antecedente_medico as update_antecedente_medico_dao, 
    delete_antecedente_medico as delete_antecedente_medico_dao,
    get_antecedentes_medicos_by_paciente as get_antecedentes_medicos_by_paciente_dao
)

def get_antecedentes_medicos():
    return get_all_antecedentes_medicos()

def add_antecedente_medico(id_paciente, tipo, descripcion):
    add_antecedente_medico_dao(id_paciente, tipo, descripcion)

def update_antecedente_medico(id_antecedente, tipo, descripcion):
    update_antecedente_medico_dao(id_antecedente, tipo, descripcion)

def delete_antecedente_medico(id_antecedente):
    delete_antecedente_medico_dao(id_antecedente)

def get_antecedentes_medicos_by_paciente(id_paciente, id_usuario):
    """
    Obtiene todos los antecedentes médicos de un paciente específico asociados al usuario logueado.
    
    Args:
        id_paciente (str): El ID del paciente.
        id_usuario (int): El ID del usuario logueado.
    
    Returns:
        list[AntecedenteMedico]: Una lista de objetos AntecedenteMedico.
    """
    return get_antecedentes_medicos_by_paciente_dao(id_paciente, id_usuario)