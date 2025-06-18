from clases import Alumno, Curso, Servidor, Servicio
import yaml
import uuid

alumnos = []
cursos = []
servidores = []  # ⬅️ ESTA LÍNEA ESTABA FALTANDO
conexiones = []
archivo_datos = None




def mostrar_menu():
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Importar datos")
    print("2. Exportar datos")
    print("3. Cursos")
    print("4. Alumnos")
    print("5. Servidores")
    print("6. Políticas")
    print("7. Conexiones")
    print("0. Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre = input("Ingrese el nombre del archivo YAML (ej: datos.yaml): ")
            importar_datos(nombre)
        elif opcion == '2':
            exportar_datos()
        elif opcion == '3':
            menu_cursos()
        elif opcion == '4':
            menu_alumnos()
        elif opcion == '5':
            menu_servidores()
        elif opcion == '6':
            menu_politicas()
        elif opcion == '7':
            menu_conexiones()
        elif opcion == '0':
            print("Saliendo...")
            break
        else:
            print("Opción inválida")






#-----------------------1) IMPORTAR---------------------------------#

from clases import Alumno, Curso, Servidor, Servicio

def importar_datos(nombre_archivo):
    global alumnos, cursos, servidores, archivo_datos
    archivo_datos = nombre_archivo
    try:
        with open(nombre_archivo, 'r') as f:
            datos = yaml.safe_load(f)

            alumnos.clear()
            cursos.clear()
            servidores.clear()

            # --- Cargar alumnos ---
            for a in datos.get("alumnos", []):
                alumno = Alumno(a["nombre"], a["codigo"], a["mac"])
                alumnos.append(alumno)

            # --- Cargar cursos ---
            for c in datos.get("cursos", []):
                curso = Curso(c["codigo"], c["nombre"], c["estado"])
                curso.alumnos = c.get("alumnos", [])
                curso.servidores = c.get("servidores", [])
                cursos.append(curso)

            # --- Cargar servidores ---
            for s in datos.get("servidores", []):
                lista_servicios = []
                for serv in s.get("servicios", []):
                    lista_servicios.append(Servicio(serv["nombre"], serv["protocolo"], serv["puerto"]))
                servidor = Servidor(s["nombre"], s["ip"], lista_servicios)
                servidores.append(servidor)

            print("✅ Datos importados correctamente.")

    except FileNotFoundError:
        print(" Archivo no encontrado.")
    except yaml.YAMLError as e:
        print(" Error al parsear YAML:", e)


#----------------------------------------------------------------------------------#




#-------------------------2) EXPORTAR-------------------------------------------#
def exportar_datos():
    print("Función exportar aun no implemesdsdntada.")
#-------------------------------------------------------------------------------#





#-----------------------------3) CURSOS-----------------------------------------#
def menu_cursos():
    print("\n--- GESTIÓN DE CURSOS ---")
    print("1. Crear curso")
    print("2. Ver todos los cursos")
    print("3. Ver detalles de un curso")
    print("4. Actualizar curso")
    print("5. Eliminar curso")
    print("0. Volver al menú principal")
    opcion = input("Seleccione una opción: ")

    if opcion == '2':
        listar_cursos()
    elif opcion == '3':
        ver_detalles_curso()
    elif opcion == '4':
        actualizar_curso()




def listar_cursos():
    global cursos
    if not cursos:
        print("No hay cursos cargados.")
        return

    print("\n--- Lista de cursos ---")
    for curso in cursos:
        print(f"{curso.codigo} - {curso.nombre} ({curso.estado})")




def ver_detalles_curso():
    global cursos, alumnos
    codigo = input("Ingrese el código del curso: ").strip()
    curso = next((c for c in cursos if c.codigo == codigo), None)
    
    if not curso:
        print("Curso no encontrado.")
        return

    print(f"\nCurso: {curso.nombre} ({curso.estado})")
    print(f"Código: {curso.codigo}")

    print("\nAlumnos matriculados:")
    for cod_alumno in curso.alumnos:
        alumno = next((a for a in alumnos if a.codigo == cod_alumno), None)
        if alumno:
            print(f" - {alumno.nombre} ({alumno.mac})")

    print("\nServidores asignados:")
    for servidor in curso.servidores:
        print(f" - {servidor['nombre']}")
        for servicio in servidor['servicios_permitidos']:
            print(f"   ▸ {servicio}")





    
def actualizar_curso():
    global cursos, alumnos
    codigo = input("Código del curso a actualizar: ").strip()
    curso = next((c for c in cursos if c.codigo == codigo), None)
    if not curso:
        print("Curso no encontrado.")
        return

    print(f"\nCurso: {curso.nombre}")
    print("1. Agregar alumno")
    print("2. Eliminar alumno")
    opcion = input("Seleccione una opción: ")

    if opcion == '1':
        print("Alumnos disponibles:")
        for a in alumnos:
            print(f" - {a.codigo}: {a.nombre}")
        cod = input("Ingrese código del alumno a agregar: ").strip()
        if cod not in [a.codigo for a in curso.alumnos]:
            alumno = next((a for a in alumnos if a.codigo == cod), None)
            if alumno:
                curso.alumnos.append(alumno)
                print("Alumno agregado.")
            else:
                print("Alumno no encontrado.")
        else:
            print("El alumno ya está en el curso.")

    elif opcion == '2':
        print("Alumnos en el curso:")
        for a in curso.alumnos:
            print(f" - {a.codigo}: {a.nombre}")
        cod = input("Ingrese código del alumno a eliminar: ").strip()
        alumno = next((a for a in curso.alumnos if a.codigo == cod), None)
        if alumno:
            curso.alumnos.remove(alumno)
            print("Alumno eliminado.")
        else:
            print("El alumno no está en el curso.")


#----------------------------------------------------------------------------#






#----------------------------------4) ALUMNOS--------------------------------------#
def menu_alumnos():
    print("\n--- MENÚ ALUMNOS ---")
    print("1. Listar Alumnos")
    print("2. Mostrar Detalles")
    print("3. Crear")
    print("4. Actualizar")
    print("5. Borrar")
    print("0. Volver al menú principal")

    opcion = input("Seleccione una opción: ")

    if opcion == '1':
        listar_alumnos()
    elif opcion == '2':
        ver_detalles_alumno()
    elif opcion == '3':
        crear_alumno()




def listar_alumnos():
    if not alumnos:
        print("No hay alumnos.")
        return
    print("\n--- Alumnos ---")
    for a in alumnos:
        print(f"{a.codigo} - {a.nombre} (MAC: {a.mac})")



def ver_detalles_alumno():
    global alumnos
    codigo = input("Ingrese el código del alumno: ").strip()
    alumno = next((a for a in alumnos if str(a.codigo) == codigo), None)

    if alumno:
        print(f"\n--- Detalles del Alumno ---")
        print(f"Nombre: {alumno.nombre}")
        print(f"Código: {alumno.codigo}")
        print(f"MAC: {alumno.mac}")
    else:
        print("Alumno no encontrado.")


def crear_alumno():
    global alumnos, archivo_datos

    print("\n--- Crear Nuevo Alumno ---")
    codigo = input("Ingrese código del alumno: ").strip()
    
    # Verificar si ya existe
    if any(a.codigo == codigo for a in alumnos):
        print(" Ya existe un alumno con ese código.")
        return

    nombre = input("Ingrese nombre del alumno: ").strip()
    mac = input("Ingrese dirección MAC: ").strip().lower()

    nuevo = Alumno(codigo, nombre, mac)
    alumnos.append(nuevo)
    print(" Alumno creado correctamente.")

    if archivo_datos:
        try:
            with open(archivo_datos, 'r') as f:
                datos = yaml.safe_load(f) or {}

            datos['alumnos'] = [
                {'codigo': a.codigo, 'nombre': a.nombre, 'mac': a.mac}
                for a in alumnos
            ]

            with open(archivo_datos, 'w') as f:
                yaml.dump(datos, f)

            print(f" Alumno guardado en {archivo_datos}.")
        except Exception as e:
            print(f" Error al guardar en YAML: {e}")
    else:
        print(" No se ha importado ningún archivo YAML. No se guardó el alumno.")


#---------------------------------------------------------------------------#




#----------------------------------5) --------------------------------------#

def menu_servidores():
    print("\n--- MENÚ SERVIDORES ---")
    print("1. Listar servidores")
    print("2. Mostrar detalle de un servidor")
    print("3. Actualizar (no implementado)")
    print("4. Borrar (no implementado)")
    print("0. Volver al menú principal")
    opcion = input("Seleccione una opción: ")

    if opcion == '1':
        listar_servidores()
    elif opcion == '2':
        ver_detalles_servidor()






def listar_servidores():
    global servidores
    if not servidores:
        print("No hay servidores registrados.")
        return

    print("\n--- Lista de servidores ---")
    for s in servidores:
        print(f" - {s.nombre} (IP: {s.ip})")






def ver_detalles_servidor():
    global servidores
    nombre = input("Ingrese el nombre del servidor: ").strip()
    servidor = next((s for s in servidores if s.nombre.lower() == nombre.lower()), None)

    if not servidor:
        print("Servidor no encontrado.")
        return

    print(f"\n--- Detalles de {servidor.nombre} ---")
    print(f"IP: {servidor.ip}")
    print("Servicios:")
    for servicio in servidor.servicios:
        print(f" - {servicio.nombre} ({servicio.protocolo}:{servicio.puerto})")


#---------------------------------------------------------------------------#





#----------------------------------6) POLÍTICAS--------------------------------------#

def menu_politicas():
    print('Aun no implementado')


#---------------------------------------------------------------------------#





#----------------------------------7) CONEXIONES--------------------------------------#


def menu_conexiones():
    print("\n--- MENÚ CONEXIONES ---")
    print("1. Crear conexión")
    print("2. Listar conexiones")
    print("3. Mostrar detalle de una conexión")
    print("4. Recalcular ruta (no implementado)")
    print("5. Actualizar ruta (no implementado)")
    print("6. Borrar conexión")
    print("0. Volver al menú principal")
    opcion = input("Seleccione una opción: ")

    if opcion == '1':
        crear_conexion()
    elif opcion == '2':
        listar_conexiones()
    elif opcion == '3':
        mostrar_detalle_conexion()
    elif opcion == '6':
        borrar_conexion()
    elif opcion == '0':
        return
    else:
        print("Opción inválida.")

def obtener_ruta(mac_origen, ip_destino):
    # Implementa esta función según actividad 2
    return [{"dpid": "00:00:00:00:00:00:00:01", "port": 1}, {"dpid": "00:00:00:00:00:00:00:02", "port": 2}]

def insertar_flows(ruta, mac_src, ip_dst, servicio):
    # Implementa esta función según actividad 3
    # Debe insertar match L2, L3, L4 y ARP bidireccionalmente
    print(f"[DEBUG] Insertando flows para ruta {ruta}")





def crear_conexion():
    global conexiones, alumnos, cursos, servidores

    mac = input("Ingrese la MAC del alumno: ").strip().lower()
    alumno = next((a for a in alumnos if a.mac.lower() == mac), None)
    if not alumno:
        print("❌ Alumno no encontrado.")
        return

    # Filtrar cursos DICTANDO donde esté el alumno
    cursos_dictando = [
        c for c in cursos 
        if alumno.codigo in c.alumnos and c.estado.upper() == "DICTANDO"
    ]

    if not cursos_dictando:
        print("❌ El alumno no está matriculado en ningún curso dictando.")
        return

    # Mostrar cursos válidos
    print("\nCursos disponibles:")
    for idx, c in enumerate(cursos_dictando):
        print(f"{idx+1}. {c.codigo} - {c.nombre}")

    i = int(input("Seleccione el curso: ")) - 1
    curso = cursos_dictando[i]

    if not curso.servidores:
        print("❌ Este curso no tiene servidores asignados.")
        return

    # Mostrar servidores
    print("\nServidores disponibles:")
    for idx, s in enumerate(curso.servidores):
        print(f"{idx+1}. {s['nombre']} - Servicios: {', '.join(s['servicios_permitidos'])}")

    i = int(input("Seleccione el servidor: ")) - 1
    servidor_ref = curso.servidores[i]

    servidor_real = next((s for s in servidores if s.nombre == servidor_ref['nombre']), None)
    if not servidor_real:
        print("❌ Servidor no encontrado.")
        return

    # Servicios disponibles
    servicios_disponibles = [
        s for s in servidor_real.servicios if s['nombre'] in servidor_ref['servicios_permitidos']
    ]
    print("\nServicios disponibles:")
    for idx, s in enumerate(servicios_disponibles):
        print(f"{idx+1}. {s['nombre']} ({s['protocolo']}:{s['puerto']})")

    i = int(input("Seleccione el servicio: ")) - 1
    servicio = servicios_disponibles[i]

    # TODO: Obtener ruta (actividad 2 previa)
    ruta = obtener_ruta(mac_origen=alumno.mac, ip_destino=servidor_real.ip)  # Placeholder

    # TODO: Insertar flows (actividad 3 previa)
    insertar_flows(ruta, alumno.mac, servidor_real.ip, servicio)

    handler = str(uuid.uuid4())[:8]
    conexion = {
        "handler": handler,
        "mac_alumno": alumno.mac,
        "curso": curso.codigo,
        "servidor": servidor_real.nombre,
        "servicio": servicio
    }
    conexiones.append(conexion)
    print(f"✅ Conexión creada con handler: {handler}")








def listar_conexiones():
    if not conexiones:
        print("No hay conexiones activas.")
        return
    print("\n--- Conexiones ---")
    for c in conexiones:
        print(f"🔗 {c['handler']} | MAC: {c['mac_alumno']} | Servidor: {c['servidor']} | Servicio: {c['servicio']['nombre']}")








def mostrar_detalle_conexion():
    handler = input("Ingrese el handler: ").strip()
    conexion = next((c for c in conexiones if c['handler'] == handler), None)
    if not conexion:
        print("❌ Conexión no encontrada.")
        return
    print(f"\n--- Detalles de conexión ---")
    print(f"Handler: {conexion['handler']}")
    print(f"MAC alumno: {conexion['mac_alumno']}")
    print(f"Curso: {conexion['curso']}")
    print(f"Servidor: {conexion['servidor']}")
    servicio = conexion['servicio']
    print(f"Servicio: {servicio['nombre']} ({servicio['protocolo']}:{servicio['puerto']})")








def borrar_conexion():
    global conexiones
    handler = input("Ingrese el handler a eliminar: ").strip()
    before = len(conexiones)
    conexiones = [c for c in conexiones if c['handler'] != handler]
    if len(conexiones) < before:
        print(" Conexión eliminada.")
    else:
        print(" Handler no encontrado.")


#---------------------------------------------------------------------------#







if __name__ == "__main__":
    main()
