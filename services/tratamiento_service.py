from dao.tratamiento_dao import (
    get_all_tratamientos, 
    add_tratamiento as add_tratamiento_dao, 
    update_tratamiento as update_tratamiento_dao, 
    delete_tratamiento as delete_tratamiento_dao
)

def get_tratamientos():
    return get_all_tratamientos()

def add_tratamiento(id_paciente, fecha, tratamiento):
    add_tratamiento_dao(id_paciente, fecha, tratamiento)

def update_tratamiento(id_tratamiento, fecha, tratamiento):
    update_tratamiento_dao(id_tratamiento, fecha, tratamiento)

def delete_tratamiento(id_tratamiento):
    delete_tratamiento_dao(id_tratamiento)