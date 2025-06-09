# Funciones para listar mascotas y ver historial de consultas

import logging
from modelos import Mascota # Importación de la clase Mascota para manejar las mascotas registradas


# La lista de mascotas es compartida ya que se definió de forma global en el módulo registro
from registro import mascotas


# Función para mostrar todas las mascotas registradas
def listar_mascotas():
    print("\n--- Lista de Mascotas ---")
    if not mascotas:
        print("No hay mascotas registradas.\n")
        logging.info("Listado solicitado con éxito. No hay mascotas registradas") # Registro del evento ocurrido
        return
    for i, mascota in enumerate(mascotas, 1): # "enumerate" es una función que permite recorrer una lista y obtener el índice y el valor de cada elemento
        print(f"{i}. {mascota}")


# Función para mostrar el historial de consultas veterinarias de una mascota
def ver_historial_consultas():
    
    # Validación de posibles errores en la consulta del historial
    try:
        print("\n--- Historial de Consultas (0 para volver) ---")
        if not mascotas:
            print("\nNo hay mascotas registradas.\n")
            logging.info("Listado solicitado con éxito. No hay consultas registradas.")
            return

        listar_mascotas()
        id_input = input("Seleccione el número (ID) de la mascota: ")
        if id_input == "0": return
        idmascota = int(id_input) - 1
        if not (0 <= idmascota < len(mascotas)):
            raise IndexError("ID de mascota no válido.")

        mascota = mascotas[idmascota]
        if not mascota.consultas:
            print("\nNo hay consultas registradas para esta mascota.\n")
            logging.info(f"No hay consultas para la mascota {mascota.nombre}")
        else:
            print(f"\nHistorial de consultas para {mascota.nombre}:")
            for consulta in mascota.consultas:
                print(consulta)
    except ValueError: # Captura de errores de valor
        print("Entrada inválida. Por favor ingrese un número válido.")
        logging.error("Valor inválido para ver historial de consultas.") # Registro del error
    except IndexError as ie: # Captura de errores de índice
        print(f"Error: {ie}") 
        logging.warning(f"El índice seleccionado está fuera del rango: {ie}") # Registro del error
    except Exception as e: # Captura de errores imprevistos en tiempo de ejecución
        print("Ocurrió un error al ver el historial.")
        logging.exception("Excepción general al ver historial.") # Registro de la excepción general