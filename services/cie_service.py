from dao.cie_dao import (
    get_all_cie, 
    add_cie as add_cie_dao, 
    update_cie as update_cie_dao, 
    delete_cie as delete_cie_dao
)

def get_cie():
    return get_all_cie()

def add_cie(codigo, descripcion):
    add_cie_dao(codigo, descripcion)

def update_cie(id_cie, codigo, descripcion):
    update_cie_dao(id_cie, codigo, descripcion)

def delete_cie(id_cie):
    delete_cie_dao(id_cie)