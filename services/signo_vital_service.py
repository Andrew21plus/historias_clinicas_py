from dao.signo_vital_dao import (
    get_all_signos_vitales, 
    add_signo_vital as add_signo_vital_dao, 
    update_signo_vital as update_signo_vital_dao, 
    delete_signo_vital as delete_signo_vital_dao
)

def get_signos_vitales():
    return get_all_signos_vitales()

def add_signo_vital(id_paciente, fecha, presion_arterial, frecuencia_cardiaca, frecuencia_respiratoria, temperatura, peso, talla):
    add_signo_vital_dao(id_paciente, fecha, presion_arterial, frecuencia_cardiaca, frecuencia_respiratoria, temperatura, peso, talla)

def update_signo_vital(id_signo, fecha, presion_arterial, frecuencia_cardiaca, frecuencia_respiratoria, temperatura, peso, talla):
    update_signo_vital_dao(id_signo, fecha, presion_arterial, frecuencia_cardiaca, frecuencia_respiratoria, temperatura, peso, talla)

def delete_signo_vital(id_signo):
    delete_signo_vital_dao(id_signo)