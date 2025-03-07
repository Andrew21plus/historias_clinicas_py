class Prescripcion:
    def __init__(self, id_prescripcion, id_paciente, fecha, medicamento, dosis, indicaciones, firmado_por):
        self.id_prescripcion = id_prescripcion
        self.id_paciente = id_paciente
        self.fecha = fecha
        self.medicamento = medicamento
        self.dosis = dosis
        self.indicaciones = indicaciones
        self.firmado_por = firmado_por