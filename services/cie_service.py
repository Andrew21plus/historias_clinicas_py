from dao.cie_dao import (
    get_all_cie,
    get_cie_by_id,
    add_cie as add_cie_dao,
    update_cie as update_cie_dao,
    delete_cie as delete_cie_dao,
)


def get_cie(search_query=""):
    """Obtiene códigos CIE con filtro opcional"""
    all_cie = get_all_cie()

    if not search_query:
        return all_cie

    search_lower = search_query.lower()
    return [
        cie
        for cie in all_cie
        if search_lower in cie.codigo.lower() or search_lower in cie.descripcion.lower()
    ]


def get_cie_by_id_service(id_cie):
    """Obtiene un CIE por su ID"""
    return get_cie_by_id(id_cie)


def add_cie(codigo, descripcion):
    add_cie_dao(codigo, descripcion)


def update_cie(id_cie, codigo, descripcion):
    update_cie_dao(id_cie, codigo, descripcion)


def delete_cie(id_cie):
    delete_cie_dao(id_cie)
