import sqlite3
from models.evolucion import Evolucion
from dao.database import DB_NAME

def get_all_evoluciones():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM Evoluciones")
    rows = c.fetchall()
    evoluciones = [Evolucion(*row) for row in rows]
    conn.close()
    return evoluciones

def get_evolucion_by_id(id_evolucion):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM Evoluciones WHERE id_evolucion = ?", (id_evolucion,))
    row = c.fetchone()
    conn.close()
    return Evolucion(*row) if row else None

def add_evolucion(id_paciente, fecha, hora, notas):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO Evoluciones (id_paciente, fecha, hora, notas)
        VALUES (?, ?, ?, ?)
    """, (id_paciente, fecha, hora, notas))
    conn.commit()
    conn.close()

def update_evolucion(id_evolucion, fecha, hora, notas):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        UPDATE Evoluciones 
        SET fecha = ?, hora = ?, notas = ?
        WHERE id_evolucion = ?
    """, (fecha, hora, notas, id_evolucion))
    conn.commit()
    conn.close()

def delete_evolucion(id_evolucion):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM Evoluciones WHERE id_evolucion = ?", (id_evolucion,))
    conn.commit()
    conn.close()