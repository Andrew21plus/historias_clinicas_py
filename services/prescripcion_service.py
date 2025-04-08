from dao.prescripcion_dao import (
    get_all_prescripciones, 
    add_prescripcion as add_prescripcion_dao, 
    update_prescripcion as update_prescripcion_dao, 
    delete_prescripcion as delete_prescripcion_dao,
    get_prescripciones_by_paciente_and_fecha,
    get_prescripciones_by_usuario as get_prescripciones_by_usuario_dao
)

def get_prescripciones():
    return get_all_prescripciones()

def add_prescripcion(id_paciente, fecha, medicamento, dosis, indicaciones, firmado_por, id_usuario):
    add_prescripcion_dao(id_paciente, fecha, medicamento, dosis, indicaciones, firmado_por, id_usuario)

def update_prescripcion(id_prescripcion, fecha, medicamento, dosis, indicaciones, firmado_por):
    update_prescripcion_dao(id_prescripcion, fecha, medicamento, dosis, indicaciones, firmado_por)

def delete_prescripcion(id_prescripcion):
    delete_prescripcion_dao(id_prescripcion)

def get_prescripciones_by_consulta(id_paciente, fecha_consulta):
    """Obtiene prescripciones por paciente y fecha de consulta"""
    return get_prescripciones_by_paciente_and_fecha(id_paciente, fecha_consulta)

def get_prescripciones_by_usuario(id_usuario):
    
    return get_prescripciones_by_usuario_dao(id_usuario)