from dao.diagnostico_dao import (
    get_all_diagnosticos, 
    add_diagnostico as add_diagnostico_dao, 
    update_diagnostico as update_diagnostico_dao, 
    delete_diagnostico as delete_diagnostico_dao
)

def get_diagnosticos():
    return get_all_diagnosticos()

def add_diagnostico(id_paciente, fecha, diagnostico, cie, definitivo):
    add_diagnostico_dao(id_paciente, fecha, diagnostico, cie, definitivo)

def update_diagnostico(id_diagnostico, fecha, diagnostico, cie, definitivo):
    update_diagnostico_dao(id_diagnostico, fecha, diagnostico, cie, definitivo)

def delete_diagnostico(id_diagnostico):
    delete_diagnostico_dao(id_diagnostico)