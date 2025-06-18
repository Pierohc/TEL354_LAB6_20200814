class Alumno:
    def __init__(self, codigo, nombre, mac):
        self.codigo = codigo
        self.nombre = nombre
        self.mac = mac

class Servicio:
    def __init__(self, nombre, protocolo, puerto):
        self.nombre = nombre
        self.protocolo = protocolo
        self.puerto = puerto

class Servidor:
    def __init__(self, nombre, ip, servicios):
        self.nombre = nombre
        self.ip = ip
        self.servicios = servicios  # lista de objetos Servicio

class Curso:
    def __init__(self, codigo, nombre, estado, alumnos=None, servidores=None):
        self.codigo = codigo
        self.nombre = nombre
        self.estado = estado
        self.alumnos = alumnos if alumnos else []
        self.servidores = servidores if servidores else []
        



