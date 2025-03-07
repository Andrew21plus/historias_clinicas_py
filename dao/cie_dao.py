from models.cie import CIE
from dao.database import get_connection  # Importar get_connection

def get_all_cie():
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("SELECT * FROM CIE")
    rows = c.fetchall()
    cie_list = [CIE(*row) for row in rows]
    conn.close()
    return cie_list

def get_cie_by_id(id_cie):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("SELECT * FROM CIE WHERE id_cie = ?", (id_cie,))
    row = c.fetchone()
    conn.close()
    return CIE(*row) if row else None

def add_cie(codigo, descripcion):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("""
        INSERT INTO CIE (codigo, descripcion)
        VALUES (?, ?)
    """, (codigo, descripcion))
    conn.commit()
    conn.close()

def update_cie(id_cie, codigo, descripcion):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("""
        UPDATE CIE 
        SET codigo = ?, descripcion = ?
        WHERE id_cie = ?
    """, (codigo, descripcion, id_cie))
    conn.commit()
    conn.close()

def delete_cie(id_cie):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("DELETE FROM CIE WHERE id_cie = ?", (id_cie,))
    conn.commit()
    conn.close()