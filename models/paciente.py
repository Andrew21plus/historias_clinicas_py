class Paciente:
    def __init__(
        self,
        id_paciente,
        nombre,
        apellido,
        sexo,
        fecha_nacimiento,
        num_historia_clinica,
        foto,
        id_usuario,
    ):
        self.id_paciente = id_paciente
        self.nombre = nombre
        self.apellido = apellido
        self.sexo = sexo
        self.fecha_nacimiento = fecha_nacimiento
        self.num_historia_clinica = num_historia_clinica
        self.foto = foto  # La foto se almacenará en BLOB
        self.id_usuario = id_usuario  # Nuevo atributo
