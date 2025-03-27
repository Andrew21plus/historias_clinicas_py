from dao.diagnostico_dao import (
    get_all_diagnosticos, 
    add_diagnostico as add_diagnostico_dao, 
    update_diagnostico as update_diagnostico_dao, 
    delete_diagnostico as delete_diagnostico_dao,
    get_diagnosticos_by_paciente_and_fecha
)

def get_diagnosticos():
    return get_all_diagnosticos()

def add_diagnostico(id_paciente, fecha, diagnostico, cie, definitivo, id_usuario):
    add_diagnostico_dao(id_paciente, fecha, diagnostico, cie, definitivo, id_usuario)

def update_diagnostico(id_diagnostico, fecha, diagnostico, cie, definitivo):
    update_diagnostico_dao(id_diagnostico, fecha, diagnostico, cie, definitivo)

def delete_diagnostico(id_diagnostico):
    delete_diagnostico_dao(id_diagnostico)

def get_diagnosticos_by_consulta(id_paciente, fecha_consulta):
    """Obtiene diagnósticos por paciente y fecha de consulta"""
    return get_diagnosticos_by_paciente_and_fecha(id_paciente, fecha_consulta)
