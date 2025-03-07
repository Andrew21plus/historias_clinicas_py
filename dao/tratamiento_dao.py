import sqlite3
from models.tratamiento import Tratamiento
from dao.database import DB_NAME

def get_all_tratamientos():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM Tratamientos")
    rows = c.fetchall()
    tratamientos = [Tratamiento(*row) for row in rows]
    conn.close()
    return tratamientos

def get_tratamiento_by_id(id_tratamiento):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM Tratamientos WHERE id_tratamiento = ?", (id_tratamiento,))
    row = c.fetchone()
    conn.close()
    return Tratamiento(*row) if row else None

def add_tratamiento(id_paciente, fecha, tratamiento):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO Tratamientos (id_paciente, fecha, tratamiento)
        VALUES (?, ?, ?)
    """, (id_paciente, fecha, tratamiento))
    conn.commit()
    conn.close()

def update_tratamiento(id_tratamiento, fecha, tratamiento):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        UPDATE Tratamientos 
        SET fecha = ?, tratamiento = ?
        WHERE id_tratamiento = ?
    """, (fecha, tratamiento, id_tratamiento))
    conn.commit()
    conn.close()

def delete_tratamiento(id_tratamiento):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM Tratamientos WHERE id_tratamiento = ?", (id_tratamiento,))
    conn.commit()
    conn.close()