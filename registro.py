# Funciones relacionadas con el registro de mascotas y de consultas

from datetime import datetime # Importación del módulo datetime para manejar fechas
import logging # Importación del módulo logging para manejar registros de eventos
from modelos import Dueno, Mascota, Consulta # Importación de las clases Dueno, Mascota y Consulta


# Lista vacía para almacenar todas las mascotas registradas
global mascotas # Se define la variable global mascotas para que pueda ser accedida en otras funciones
mascotas = []


# Función para registrar una nueva mascota y su dueño
def registrar_mascota():
    
    # Validación de posibles errores en la entradas de datos
    try:
        print("\n--- Registrar Nueva Mascota (0 para volver) ---")
        nombre = input("Nombre de la mascota: ")
        if nombre == "0": return

        especie = input("Especie: ")
        if especie == "0": return

        raza = input("Raza: ")
        if raza == "0": return

        edad_input = input("Edad: ")
        if edad_input == "0": return
        edad = int(edad_input)
        if edad < 0:
            raise ValueError("La edad no puede ser un número negativo.")

        print("\n--- Datos del Dueño (0 para volver) ---")
        nombre_dueno = input("Nombre del dueño: ")
        if nombre_dueno == "0": return

        telefono = input("Teléfono: ")
        if telefono == "0": return

        direccion = input("Dirección: ")
        if direccion == "0": return

        dueno = Dueno(nombre_dueno, telefono, direccion)
        mascota = Mascota(nombre, especie, raza, edad, dueno)
        mascotas.append(mascota)
        print("\n¡Mascota registrada exitosamente!\n")

        logging.info(f"Mascota registrada exitosamente: {mascota.nombre}, Dueño: {dueno.nombre}")
    except ValueError as ve: # Captura de errores de valor
        print(f"Error: {ve}")
        logging.error(f"Error al registrar mascota: {ve}") # Registro del error
    except Exception as e: # Captura de errores imprevistos en tiempo de ejecución
        print("Error al registrar la mascota.")
        logging.exception("Excepción general al registrar mascota.") # Registro de la excepción general


# Función para registrar una consulta veterinaria para una mascota
def registrar_consulta():
    try:
        print("\n--- Registrar Consulta (0 para volver) ---")
        if not mascotas:
            print("\nNo hay mascotas registradas.\n")
            return

        for i, mascota in enumerate(mascotas, 1):
            print(f"{i}. {mascota}")

        id_input = input("Seleccione el número de la mascota: ")
        if id_input == "0": return
        idmascota = int(id_input) - 1
        if not (0 <= idmascota < len(mascotas)):
            raise IndexError("Número de mascota no válido.")

        while True:
            fecha = input("Fecha (YYYY-MM-DD): ")
            if fecha == "0": return
            try:
                datetime.strptime(fecha, "%Y-%m-%d") # Validar formato de fecha
                break
            except ValueError:
                print("Formato de fecha inválido. Intente nuevamente.")

        motivo = input("Motivo de la consulta: ")
        if motivo == "0": return

        diagnostico = input("Diagnóstico: ")
        if diagnostico == "0": return

        consulta = Consulta(fecha, motivo, diagnostico, mascotas[idmascota])
        mascotas[idmascota].agregar_consulta(consulta)
        print("\n¡Consulta registrada exitosamente!\n")

        logging.info(f"Consulta registrada para {mascotas[idmascota].nombre} en {fecha}")
    except ValueError: # Captura de errores de valor
        print("Entrada inválida. Por favor ingrese un número válido.")
        logging.error("Valor inválido al seleccionar mascota para realizar consulta.") # Registro del error
    except IndexError as ie: # Captura de errores de índice
        print(f"Error: {ie}")
        logging.warning(f"El número seleccionado está fuera del rango: {ie}") # Registro de la advertencia
    except Exception as e: # Captura de errores imprevistos en tiempo de ejecución
        print("Ocurrió un error al registrar la consulta.")
        logging.exception("Excepción general al registrar consulta.") # Registro de la excepción general