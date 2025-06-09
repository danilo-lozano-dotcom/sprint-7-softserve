# Módulo central que coordina la ejecución del sistema

import logging # Importación del módulo logging para manejar registros de eventos
from registro import registrar_mascota, registrar_consulta, mascotas # Importación de funciones para registrar mascotas y consultas
from consultas import listar_mascotas, ver_historial_consultas # Importación de funciones para listar mascotas y ver historial de consultas
from persistencia import guardar_mascotas_csv, guardar_consultas_json, cargar_mascotas_csv, cargar_consultas_json # Importación de funciones para guardar y cargar datos en formatos CSV y JSON


# Configuración del sistema de logging para registrar eventos, errores y excepciones
logging.basicConfig(
    filename='clinica_veterinaria.log',
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s')


# Menú principal de la aplicación
def menu():
    logging.info("Inicio de la aplicación.") # Registro del inicio de la aplicación
    while True:
        print("\n--- Clínica Veterinaria Amigos Peludos ---")
        print("1. Registrar mascota")
        print("2. Agendar consulta")
        print("3. Listar mascotas")
        print("4. Ver historial de consultas de una mascota específica")
        print("5. Exportar datos (CSV/JSON)")
        print("6. Importar datos (CSV/JSON)")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")

        # Validación de posibles errores en la entrada del menú
        try:
            if opcion == "1":
                registrar_mascota()
            elif opcion == "2":
                registrar_consulta()
            elif opcion == "3":
                listar_mascotas()
            elif opcion == "4":
                ver_historial_consultas()
            elif opcion == "5":
                guardar_mascotas_csv()
                guardar_consultas_json()
                print("Datos exportados exitosamente.")
            elif opcion == "6":
                if mascotas: # Verifica si hay mascotas registradas antes de importar
                    confirmacion = input("¿Está seguro de que desea importar datos? Esto sobrescribirá los datos actuales (S/N): ").lower()
                    if confirmacion != 's':
                        print("Importación cancelada.")
                        logging.info("Importación de datos cancelada por el usuario.")
                        continue
                    mascotas.clear() # Esto evita duplicados al cargar los archivos
                cargar_mascotas_csv()
                cargar_consultas_json()
                print("\n¡Datos importados exitosamente!")
            elif opcion == "7":
                print("¡Hasta luego!")
                logging.info("Cierre de la aplicación.") # Registro del cierre de la aplicación
                break
            else:
                print("Opción inválida. Intente de nuevo.\n")
        except Exception as e: # Captura de errores imprevistos en tiempo de ejecución
            print("Error en el menú principal.")
            logging.exception("Error en el menú principal") # Registro de la excepción general
 
            
# Punto de entrada de la aplicación
if __name__ == "__main__":
    
    # Cargar datos de mascotas y consultas al iniciar la aplicación
    cargar_mascotas_csv()
    cargar_consultas_json()
    
    # Iniciar el menú principal de la aplicación
    menu()
    
    # Guardar los datos de mascotas y consultas al cerrar la aplicación
    guardar_mascotas_csv()
    guardar_consultas_json()