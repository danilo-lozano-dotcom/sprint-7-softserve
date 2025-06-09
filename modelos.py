# Clases utilizadas en el sistema

# Definición de la clase Dueño que almacena información del dueño de la mascota
class Dueno:
    def __init__(self, nombre, telefono, direccion):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion

    # Método para mostrar la información del dueño
    def __str__(self):
        return f"Dueño: {self.nombre}, Teléfono: {self.telefono}, Dirección: {self.direccion}"


# Definición de la clase Mascota que almacena información de la mascota y su dueño
class Mascota:
    def __init__(self, nombre, especie, raza, edad, dueno):
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.edad = edad
        self.dueno = dueno
        self.consultas = []

    def agregar_consulta(self, consulta):
        self.consultas.append(consulta)

    # Método para mostrar la información de la mascota y su dueño
    def __str__(self):
        return (f"Nombre: {self.nombre}, Especie: {self.especie}, Raza: {self.raza}, "
                f"Edad: {self.edad}, {self.dueno}")


# Definición de la clase Consulta que almacena información de una consulta veterinaria
class Consulta:
    def __init__(self, fecha, motivo, diagnostico, mascota):
        self.fecha = fecha
        self.motivo = motivo
        self.diagnostico = diagnostico
        self.mascota = mascota

    # Método para mostrar la información de la consulta veterinaria
    def __str__(self):
        return (f"Fecha: {self.fecha}, Motivo consulta: {self.motivo}, "
                f"Diagnóstico: {self.diagnostico}")
