import sqlite3
from models.antecedente_medico import AntecedenteMedico
from dao.database import DB_NAME

def get_all_antecedentes_medicos():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM Antecedentes_Medicos")
    rows = c.fetchall()
    antecedentes = [AntecedenteMedico(*row) for row in rows]
    conn.close()
    return antecedentes

def get_antecedente_medico_by_id(id_antecedente):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM Antecedentes_Medicos WHERE id_antecedente = ?", (id_antecedente,))
    row = c.fetchone()
    conn.close()
    return AntecedenteMedico(*row) if row else None

def add_antecedente_medico(id_paciente, tipo, descripcion):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO Antecedentes_Medicos (id_paciente, tipo, descripcion)
        VALUES (?, ?, ?)
    """, (id_paciente, tipo, descripcion))
    conn.commit()
    conn.close()

def update_antecedente_medico(id_antecedente, tipo, descripcion):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        UPDATE Antecedentes_Medicos 
        SET tipo = ?, descripcion = ?
        WHERE id_antecedente = ?
    """, (tipo, descripcion, id_antecedente))
    conn.commit()
    conn.close()

def delete_antecedente_medico(id_antecedente):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM Antecedentes_Medicos WHERE id_antecedente = ?", (id_antecedente,))
    conn.commit()
    conn.close()