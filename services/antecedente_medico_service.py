from dao.antecedente_medico_dao import (
    get_all_antecedentes_medicos, 
    add_antecedente_medico as add_antecedente_medico_dao, 
    update_antecedente_medico as update_antecedente_medico_dao, 
    delete_antecedente_medico as delete_antecedente_medico_dao
)

def get_antecedentes_medicos():
    return get_all_antecedentes_medicos()

def add_antecedente_medico(id_paciente, tipo, descripcion):
    add_antecedente_medico_dao(id_paciente, tipo, descripcion)

def update_antecedente_medico(id_antecedente, tipo, descripcion):
    update_antecedente_medico_dao(id_antecedente, tipo, descripcion)

def delete_antecedente_medico(id_antecedente):
    delete_antecedente_medico_dao(id_antecedente)