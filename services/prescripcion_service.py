from dao.prescripcion_dao import (
    get_all_prescripciones, 
    add_prescripcion as add_prescripcion_dao, 
    update_prescripcion as update_prescripcion_dao, 
    delete_prescripcion as delete_prescripcion_dao
)

def get_prescripciones():
    return get_all_prescripciones()

def add_prescripcion(id_paciente, fecha, medicamento, dosis, indicaciones, firmado_por):
    add_prescripcion_dao(id_paciente, fecha, medicamento, dosis, indicaciones, firmado_por)

def update_prescripcion(id_prescripcion, fecha, medicamento, dosis, indicaciones, firmado_por):
    update_prescripcion_dao(id_prescripcion, fecha, medicamento, dosis, indicaciones, firmado_por)

def delete_prescripcion(id_prescripcion):
    delete_prescripcion_dao(id_prescripcion)