import sqlite3

DB_NAME = "clinica.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Tabla de Pacientes
    c.execute('''CREATE TABLE IF NOT EXISTS Pacientes (
        id_paciente TEXT PRIMARY KEY,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        sexo TEXT CHECK(sexo IN ('M', 'F', 'O')) NOT NULL,
        fecha_nacimiento DATE NOT NULL,
        num_historia_clinica TEXT UNIQUE NOT NULL,
        foto BLOB
    )''')

    # Tabla de Historias Clínicas
    c.execute('''CREATE TABLE IF NOT EXISTS Historias_Clinicas (
        id_historia INTEGER PRIMARY KEY AUTOINCREMENT,
        id_paciente TEXT NOT NULL,
        motivo_consulta TEXT,
        enfermedad_actual TEXT,
        FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente) ON DELETE CASCADE
    )''')

    # Tabla de Evolución del Paciente
    c.execute('''CREATE TABLE IF NOT EXISTS Evoluciones (
        id_evolucion INTEGER PRIMARY KEY AUTOINCREMENT,
        id_paciente TEXT NOT NULL,
        fecha DATE NOT NULL,
        hora TIME NOT NULL,
        notas TEXT,
        FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente) ON DELETE CASCADE
    )''')

    # Tabla de Prescripciones Médicas
    c.execute('''CREATE TABLE IF NOT EXISTS Prescripciones (
        id_prescripcion INTEGER PRIMARY KEY AUTOINCREMENT,
        id_paciente TEXT NOT NULL,
        fecha DATE NOT NULL,
        medicamento TEXT NOT NULL,
        dosis TEXT NOT NULL,
        indicaciones TEXT,
        firmado_por TEXT NOT NULL,
        FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente) ON DELETE CASCADE
    )''')

    # Tabla de Signos Vitales
    c.execute('''CREATE TABLE IF NOT EXISTS Signos_Vitales (
        id_signo INTEGER PRIMARY KEY AUTOINCREMENT,
        id_paciente TEXT NOT NULL,
        fecha DATE NOT NULL,
        presion_arterial TEXT,
        frecuencia_cardiaca INTEGER,
        frecuencia_respiratoria INTEGER,
        temperatura REAL,
        peso REAL,
        talla REAL,
        FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente) ON DELETE CASCADE
    )''')

    # Tabla de Antecedentes Médicos
    c.execute('''CREATE TABLE IF NOT EXISTS Antecedentes_Medicos (
        id_antecedente INTEGER PRIMARY KEY AUTOINCREMENT,
        id_paciente TEXT NOT NULL,
        tipo TEXT CHECK(tipo IN ('Personal', 'Familiar')) NOT NULL,
        descripcion TEXT NOT NULL,
        FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente) ON DELETE CASCADE
    )''')

    # Tabla de Diagnósticos
    c.execute('''CREATE TABLE IF NOT EXISTS Diagnosticos (
        id_diagnostico INTEGER PRIMARY KEY AUTOINCREMENT,
        id_paciente TEXT NOT NULL,
        fecha DATE NOT NULL,
        diagnostico TEXT NOT NULL,
        cie TEXT,
        definitivo BOOLEAN NOT NULL CHECK(definitivo IN (0, 1)),
        FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente) ON DELETE CASCADE
    )''')

    # Tabla de CIE (Código Internacional de Enfermedades)
    c.execute('''CREATE TABLE IF NOT EXISTS CIE (
        id_cie INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE NOT NULL,
        descripcion TEXT NOT NULL
    )''')

    # Tabla de Tratamientos
    c.execute('''CREATE TABLE IF NOT EXISTS Tratamientos (
        id_tratamiento INTEGER PRIMARY KEY AUTOINCREMENT,
        id_paciente TEXT NOT NULL,
        fecha DATE NOT NULL,
        tratamiento TEXT NOT NULL,
        FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente) ON DELETE CASCADE
    )''')

    conn.commit()
    conn.close()

# Ejecutar la inicialización al importar el módulo
init_db()