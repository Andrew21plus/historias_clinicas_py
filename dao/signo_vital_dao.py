import sqlite3
from models.signo_vital import SignoVital
from dao.database import DB_NAME

def get_all_signos_vitales():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM Signos_Vitales")
    rows = c.fetchall()
    signos = [SignoVital(*row) for row in rows]
    conn.close()
    return signos

def get_signo_vital_by_id(id_signo):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM Signos_Vitales WHERE id_signo = ?", (id_signo,))
    row = c.fetchone()
    conn.close()
    return SignoVital(*row) if row else None

def add_signo_vital(id_paciente, fecha, presion_arterial, frecuencia_cardiaca, frecuencia_respiratoria, temperatura, peso, talla):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO Signos_Vitales (id_paciente, fecha, presion_arterial, frecuencia_cardiaca, frecuencia_respiratoria, temperatura, peso, talla)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (id_paciente, fecha, presion_arterial, frecuencia_cardiaca, frecuencia_respiratoria, temperatura, peso, talla))
    conn.commit()
    conn.close()

def update_signo_vital(id_signo, fecha, presion_arterial, frecuencia_cardiaca, frecuencia_respiratoria, temperatura, peso, talla):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        UPDATE Signos_Vitales 
        SET fecha = ?, presion_arterial = ?, frecuencia_cardiaca = ?, frecuencia_respiratoria = ?, temperatura = ?, peso = ?, talla = ?
        WHERE id_signo = ?
    """, (fecha, presion_arterial, frecuencia_cardiaca, frecuencia_respiratoria, temperatura, peso, talla, id_signo))
    conn.commit()
    conn.close()

def delete_signo_vital(id_signo):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM Signos_Vitales WHERE id_signo = ?", (id_signo,))
    conn.commit()
    conn.close()