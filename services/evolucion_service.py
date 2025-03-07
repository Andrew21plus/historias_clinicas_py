from dao.evolucion_dao import (
    get_all_evoluciones, 
    add_evolucion as add_evolucion_dao, 
    update_evolucion as update_evolucion_dao, 
    delete_evolucion as delete_evolucion_dao
)

def get_evoluciones():
    return get_all_evoluciones()

def add_evolucion(id_paciente, fecha, hora, notas):
    add_evolucion_dao(id_paciente, fecha, hora, notas)

def update_evolucion(id_evolucion, fecha, hora, notas):
    update_evolucion_dao(id_evolucion, fecha, hora, notas)

def delete_evolucion(id_evolucion):
    delete_evolucion_dao(id_evolucion)