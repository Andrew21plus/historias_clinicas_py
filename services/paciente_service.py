from dao.paciente_dao import (
    get_all_pacientes, 
    add_paciente as add_paciente_dao, 
    update_paciente as update_paciente_dao, 
    delete_paciente as delete_paciente_dao,
    get_paciente_by_id
)

def get_pacientes():
    return get_all_pacientes()

def get_paciente(id_paciente):
    """ Obtiene un paciente por su ID """
    return get_paciente_by_id(id_paciente)

def add_paciente(id_paciente, nombre, apellido, sexo, fecha_nacimiento, num_historia_clinica, foto=None):
    """ Agrega un nuevo paciente, incluyendo la foto si está presente """
    add_paciente_dao(id_paciente, nombre, apellido, sexo, fecha_nacimiento, num_historia_clinica, foto)

def update_paciente(id_paciente, nombre, apellido, sexo, fecha_nacimiento, num_historia_clinica, foto=None):
    """ Actualiza los datos de un paciente, incluyendo la foto """
    update_paciente_dao(id_paciente, nombre, apellido, sexo, fecha_nacimiento, num_historia_clinica, foto)

def delete_paciente(id_paciente):
    """ Elimina un paciente de la base de datos """
    delete_paciente_dao(id_paciente)
