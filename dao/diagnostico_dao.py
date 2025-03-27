from models.diagnostico import Diagnostico
from dao.database import get_connection  # Importar get_connection


def get_all_diagnosticos():
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("SELECT * FROM Diagnosticos")
    rows = c.fetchall()
    diagnosticos = [Diagnostico(*row) for row in rows]
    conn.close()
    return diagnosticos


def get_diagnostico_by_id(id_diagnostico):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("SELECT * FROM Diagnosticos WHERE id_diagnostico = ?", (id_diagnostico,))
    row = c.fetchone()
    conn.close()
    return Diagnostico(*row) if row else None


def add_diagnostico(id_paciente, fecha, diagnostico, cie, definitivo, id_usuario):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO Diagnosticos (id_paciente, fecha, diagnostico, cie, definitivo, id_usuario)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (id_paciente, fecha, diagnostico, cie, definitivo, id_usuario),
    )
    conn.commit()
    conn.close()


def update_diagnostico(id_diagnostico, fecha, diagnostico, cie, definitivo):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute(
        """
        UPDATE Diagnosticos 
        SET fecha = ?, diagnostico = ?, cie = ?, definitivo = ?
        WHERE id_diagnostico = ?
    """,
        (fecha, diagnostico, cie, definitivo, id_diagnostico),
    )
    conn.commit()
    conn.close()


def delete_diagnostico(id_diagnostico):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("DELETE FROM Diagnosticos WHERE id_diagnostico = ?", (id_diagnostico,))

def get_diagnosticos_by_paciente_and_fecha(id_paciente, fecha):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT * FROM Diagnosticos 
        WHERE id_paciente = ? AND fecha = ?
        ORDER BY fecha DESC
    """, (id_paciente, fecha))
    rows = c.fetchall()
    diagnosticos = [Diagnostico(*row) for row in rows]
    conn.close()
    return diagnosticos