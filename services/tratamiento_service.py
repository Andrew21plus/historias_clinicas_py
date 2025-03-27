from dao.tratamiento_dao import (
    get_all_tratamientos, 
    add_tratamiento as add_tratamiento_dao, 
    update_tratamiento as update_tratamiento_dao, 
    delete_tratamiento as delete_tratamiento_dao,
    get_tratamientos_by_paciente_and_fecha 
)

def get_tratamientos():
    return get_all_tratamientos()

def add_tratamiento(id_paciente, fecha, tratamiento, id_usuario):
    add_tratamiento_dao(id_paciente, fecha, tratamiento, id_usuario)

def update_tratamiento(id_tratamiento, fecha, tratamiento):
    update_tratamiento_dao(id_tratamiento, fecha, tratamiento)

def delete_tratamiento(id_tratamiento):
    delete_tratamiento_dao(id_tratamiento)

def get_tratamientos_by_consulta(id_paciente, fecha_consulta):
    """Obtiene tratamientos por paciente y fecha de consulta"""
    return get_tratamientos_by_paciente_and_fecha(id_paciente, fecha_consulta)