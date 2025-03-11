from dao.paciente_dao import (
    get_all_pacientes, 
    add_paciente as add_paciente_dao, 
    update_paciente as update_paciente_dao, 
    delete_paciente as delete_paciente_dao,
    get_paciente_by_id
)

def get_pacientes():
    """ Obtiene todos los pacientes """
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

def cedula_existe(cedula, exclude_id=None):
    """ Verifica si una cédula ya está registrada """
    pacientes = get_all_pacientes()
    for paciente in pacientes:
        if paciente.id_paciente == cedula and (exclude_id is None or paciente.id_paciente != exclude_id):
            return True
    return False

def historia_clinica_existe(historia_clinica, exclude_id=None):
    """ Verifica si un número de historia clínica ya está registrado """
    pacientes = get_all_pacientes()
    for paciente in pacientes:
        if paciente.num_historia_clinica == historia_clinica and (exclude_id is None or paciente.id_paciente != exclude_id):
            return True
    return False