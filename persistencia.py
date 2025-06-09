# Funciones para guardar y cargar datos desde archivos CSV y JSON

import os # Importación del módulo os para manejar operaciones del sistema operativo y verificar la existencia de archivos
import csv # Importación del módulo csv para manejar archivos CSV
import json # Importación del módulo json para manejar archivos JSON
import logging # Importación del módulo logging para manejar registros de eventos
from modelos import Dueno, Mascota, Consulta # Importación de las clases Dueno, Mascota y Consulta
from registro import mascotas # Importación de la lista de mascotas desde el módulo registro

# Archivos donde se alamcenrán los datos de las mascotas y sus consultas
archivo_csv = 'mascotas_dueños.csv'
archivo_json = 'consultas.json'


# Función para guardar las mascotas y dueños en un archivo CSV
def guardar_mascotas_csv():
    try:
        if not mascotas:
            logging.warning("No hay mascotas registradas para guardar en el archivo CSV.")
            return
        with open(archivo_csv, mode='w', newline='', encoding='utf-8') as archivo: # "with open" es una forma de abrir un archivo que asegura que se cierre correctamente después de su uso
            writer = csv.writer(archivo)
            writer.writerow(['nombre_mascota', 'especie', 'raza', 'edad',
                             'nombre_dueno', 'telefono', 'direccion'])
            for mascota in mascotas:
                writer.writerow([mascota.nombre, mascota.especie, mascota.raza, mascota.edad,
                                 mascota.dueno.nombre, mascota.dueno.telefono, mascota.dueno.direccion])
        logging.info("Datos de mascotas y dueños guardados en CSV exitosamente")
    except Exception as e:
        logging.exception("Error al guardar datos de mascotas y dueños en CSV.")


# Función para guardar las consultas en un archivo JSON
def guardar_consultas_json():
    try:
        if not any(m.consultas for m in mascotas):
            logging.warning("No hay consultas registradas para guardar en el archivo JSON.")
            return
        datos_consultas = []
        for mascota in mascotas:
            for consulta in mascota.consultas:
                datos_consultas.append({
                    'nombre_mascota': mascota.nombre,
                    'fecha': consulta.fecha,
                    'motivo': consulta.motivo,
                    'diagnostico': consulta.diagnostico
                })
        with open(archivo_json, mode='w', encoding='utf-8') as archivo:
            json.dump(datos_consultas, archivo, indent=4)
        logging.info("Consultas guardadas en JSON exitosamente")
    except Exception as e:
        logging.exception("Error al guardar las consultas en JSON.")


# Función para cargar mascotas y dueños desde un archivo CSV
def cargar_mascotas_csv():
    try:
        if not os.path.exists(archivo_csv):
            logging.warning("Archivo CSV de mascotas no encontrado.")
            return
        with open(archivo_csv, mode='r', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)
            for row in reader:
                if not all(row.values()):
                    logging.warning(f"Fila incompleta en el archivo CSV: {row} . Se omitirá.")
                    continue
                if any(m.nombre == row['nombre_mascota'] for m in mascotas):
                    logging.warning(f"Ya existe una mascota con el nombre {row['nombre_mascota']}. Se omitirá.")
                    continue
                dueno = Dueno(row['nombre_dueno'], row['telefono'], row['direccion'])
                mascota = Mascota(row['nombre_mascota'], row['especie'], row['raza'], int(row['edad']), dueno)
                mascotas.append(mascota)
        logging.info("Datos de mascotas y dueños cargados desde CSV exitosamente")
    except Exception as e:
        logging.exception("Error al cargar datos desde CSV.")


# Función para cargar consultas desde un archivo JSON
def cargar_consultas_json():
    try:
        if not os.path.exists(archivo_json):
            logging.warning("Archivo JSON de consultas no encontrado.")
            return
        with open(archivo_json, mode='r', encoding='utf-8') as archivo:
            datos_consultas = json.load(archivo)
            for item in datos_consultas:
                mascota = next((m for m in mascotas if m.nombre == item['nombre_mascota']), None)
                if mascota:
                    consulta = Consulta(item['fecha'], item['motivo'], item['diagnostico'], mascota)
                    mascota.agregar_consulta(consulta)
        logging.info("Consultas cargadas desde JSON exitosamente")
    except Exception as e:
        logging.exception("Error al cargar consultas desde JSON.")
