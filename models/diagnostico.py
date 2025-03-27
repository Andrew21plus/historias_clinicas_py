class Diagnostico:
    def __init__(self, id_diagnostico, id_paciente, fecha, diagnostico, cie, definitivo, id_usuario):
        self.id_diagnostico = id_diagnostico
        self.id_paciente = id_paciente
        self.fecha = fecha
        self.diagnostico = diagnostico
        self.cie = cie
        self.definitivo = definitivo
        self.id_usuario = id_usuario