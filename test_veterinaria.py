# Pruebas unitarias para el sistema de gestión de veterinaria. Estas pruebas verifican el correcto funcionamiento de las clases y funciones del sistema

import unittest # Importación del módulo unittest para realizar pruebas unitarias
import os # Importación del módulo os para manejar operaciones del sistema operativo
import logging # Importación del módulo logging para manejar registros de eventos
import csv # Importación del módulo csv para manejar archivos CSV
import json # Importación del módulo json para manejar archivos JSON
from io import StringIO # Importación de "StringIO" del módulo "io" para simular archivos de texto en memoria (útil en pruebas de entrada/salida)
from unittest.mock import patch # Importación de "patch" para sustituir temporalmente funciones u objetos durante pruebas (mocking)
from datetime import datetime # Importación del módulo datetime para manejar fechas y horas

# Importaciones del sistema a probar
from modelos import Dueno, Mascota, Consulta
from registro import registrar_mascota, registrar_consulta, mascotas
from consultas import listar_mascotas, ver_historial_consultas
from persistencia import (guardar_mascotas_csv, guardar_consultas_json,
                         cargar_mascotas_csv, cargar_consultas_json,
                         archivo_csv, archivo_json)


# Clase de pruebas para las clases del módulo modelos.py 
class TestModelos(unittest.TestCase):
    
    # Configuración inicial para las pruebas
    def setUp(self):
        self.dueno = Dueno("Juan Pérez", "555-1234", "Calle Falsa 123")
        self.mascota = Mascota("Firulais", "Perro", "Labrador", 5, self.dueno)
        self.consulta = Consulta("2023-01-01", "Control anual", "Saludable", self.mascota)
    
    # Limpieza después de cada prueba
    def test_creacion_dueno(self):
        self.assertEqual(self.dueno.nombre, "Juan Pérez")
        self.assertEqual(self.dueno.telefono, "555-1234")
        self.assertEqual(self.dueno.direccion, "Calle Falsa 123")
    
    # Verifica la representación en string de Dueño    
    def test_str_dueno(self):
        self.assertEqual(str(self.dueno), 
                         "Dueño: Juan Pérez, Teléfono: 555-1234, Dirección: Calle Falsa 123")
    
    # Verifica la creación correcta de un objeto Mascota
    def test_creacion_mascota(self):
        self.assertEqual(self.mascota.nombre, "Firulais")
        self.assertEqual(self.mascota.especie, "Perro")
        self.assertEqual(self.mascota.raza, "Labrador")
        self.assertEqual(self.mascota.edad, 5)
        self.assertIsInstance(self.mascota.dueno, Dueno)
    
    # Verifica que se puedan agregar consultas a una mascota
    def test_agregar_consulta(self):
        self.assertEqual(len(self.mascota.consultas), 0)
        self.mascota.agregar_consulta(self.consulta)
        self.assertEqual(len(self.mascota.consultas), 1)
        self.assertIsInstance(self.mascota.consultas[0], Consulta)
    
    # Verifica la creación correcta de un objeto Consulta
    def test_creacion_consulta(self):
        self.assertEqual(self.consulta.fecha, "2023-01-01")
        self.assertEqual(self.consulta.motivo, "Control anual")
        self.assertEqual(self.consulta.diagnostico, "Saludable")
        self.assertIsInstance(self.consulta.mascota, Mascota)


# Clase de pruebas para las funciones del módulo registro.py
class TestRegistro(unittest.TestCase):
    
    # Configuración inicial para las pruebas
    def setUp(self):
        mascotas.clear()
        self.log_stream = StringIO()
        logging.basicConfig(stream=self.log_stream, level=logging.INFO)
    
    # Limpieza después de cada prueba
    def tearDown(self):
        mascotas.clear()
        logging.getLogger().handlers.clear()
    
    # Simulación de entrada de datos para registrar una mascota. Esto simula múltiples entradas de usuario. "@patch" permite reemplazar la función "input" por una lista de valores predefinidos
    @patch('builtins.input', side_effect=[
        'Rex', 'Perro', 'Pastor Alemán', '3',  # Datos mascota
        'María González', '555-9876', 'Av. Siempreviva 742'  # Datos dueño
    ])
    def test_registro_mascota_valido(self, mock_input):     # Verifica el registro correcto de una mascota con datos válidos"
        registrar_mascota()
        self.assertEqual(len(mascotas), 1)
        self.assertEqual(mascotas[0].nombre, "Rex")
        self.assertEqual(mascotas[0].dueno.nombre, "María González")
        
        logs = self.log_stream.getvalue() # Captura de los logs generados durante la prueba
        self.assertIn("Mascota registrada exitosamente: Rex", logs)
    
    # Simulación de entrada del usuario para registrar una mascota, con datos válidos excepto una edad negativa (inválida)
    @patch("builtins.print")
    @patch('builtins.input', side_effect=[ # Simulación de entradas del usuario con datos válidos excepto una edad negativa (inválida), seguida de '0' para cancelar el registro tras detectar el error
        'Rex', 'Perro', 'Pastor Alemán', '-5',  # Edad inválida
        '0'  # Cancelar
    ])
    def test_registro_mascota_edad_invalida(self, mock_input, mock_print): # Verifica el manejo de una edad inválida al registrar una mascota
        registrar_mascota()
    
        # Verifica que no se agregó ninguna mascota
        self.assertEqual(len(mascotas), 0)
        
        # Verifica que se imprimió el mensaje de error
        mock_print.assert_any_call("Error: La edad no puede ser un número negativo.")
        
        # Verifica que el error se registró en logs
        logs = self.log_stream.getvalue()
        self.assertIn("Error al registrar mascota: La edad no puede ser un número negativo", logs)
    
    # Simulación de entradas del usuario para registrar una consulta veterinaria, con datos válidos
    @patch('builtins.input', side_effect=['1', '2023-01-01', 'Control', 'Saludable'])
    def test_registro_consulta_valida(self, mock_input): # Verifica el registro correcto de una consulta veterinaria
        # Primero registramos una mascota
        dueno = Dueno("Ana", "555-1111", "Calle 1")
        mascota = Mascota("Luna", "Gato", "Siamés", 2, dueno)
        mascotas.append(mascota)
        
        registrar_consulta()
        self.assertEqual(len(mascotas[0].consultas), 1) # "assertEqual" verifica que el número de consultas sea 1
        self.assertEqual(mascotas[0].consultas[0].motivo, "Control") # Verifica que el motivo de la consulta sea "Control". "assertEqual" compara dos valores y verifica que sean iguales
        
        logs = self.log_stream.getvalue()
        self.assertIn("Consulta registrada para Luna en 2023-01-01", logs)


# Clase de pruebas para las funciones del módulo consultas.py
class TestConsultas(unittest.TestCase):
    
    # Configuración inicial para las pruebas
    def setUp(self):
        mascotas.clear()
        dueno = Dueno("Carlos", "555-2222", "Calle 2")
        self.mascota = Mascota("Thor", "Perro", "Husky", 4, dueno)
        mascotas.append(self.mascota)
        
        # Configurar logging para capturar salida
        self.log_stream = StringIO()
        logging.basicConfig(stream=self.log_stream, level=logging.INFO)
    
    # Limpieza después de cada prueba
    def tearDown(self):
        mascotas.clear()
        logging.getLogger().handlers.clear()
    
    # Prueba para listar mascotas registradas cuando no hay mascota
    @patch('builtins.print')
    def test_listar_mascotas_sin_mascotas(self, mock_print): # Verifica que se muestre un mensaje adecuado cuando no hay mascotas registradas
        mascotas.clear()
        listar_mascotas()

        mock_print.assert_any_call("No hay mascotas registradas.\n")
        logs = self.log_stream.getvalue()
        self.assertIn("Listado solicitado con éxito. No hay mascotas registradas", logs)
    
    # Prueba para listar mascotas registradas cuando hay una mascotas
    @patch('builtins.print')
    def test_listar_mascotas_con_datos(self, mock_print): # Verifica que se muestre la información de una mascota registrada
        mascotas.clear()
        dueno = Dueno("Carlos", "555-2222", "Calle 2")
        mascota = Mascota("Thor", "Perro", "Husky", 4, dueno)
        mascotas.append(mascota)

        listar_mascotas()

        mock_print.assert_any_call("1. Nombre: Thor, Especie: Perro, Raza: Husky, Edad: 4, Dueño: Carlos, Teléfono: 555-2222, Dirección: Calle 2")    
    
    @patch('builtins.input', return_value='1') # Simula selección de la mascota
    @patch('builtins.print') # Captura las salidas por consola
    def test_ver_historial_consultas(self, mock_print, mock_input): # Verifica que se muestre el historial de consultas de una mascota específica
        mascotas.clear() # Limpiar la lista de mascotas antes de la prueba
        
        # Agregar una consulta de prueba
        dueno  = Dueno("Laura", "555-3333", "Calle 3")
        mascota = Mascota("Luna", "Gato", "Siamés", 2, dueno)
        consulta = Consulta("2023-01-01", "Vacunación", "Aplicada vacuna antirrábica", mascota)
        mascota.agregar_consulta(consulta)
        mascotas.append(mascota)
        
        ver_historial_consultas()
        
        # Verifica que se haya llamado a print con el mensaje correcto
        printed_lines = [str(call.args[0]) for call in mock_print.call_args_list]
        # Verifica que se imprima la información de la consulta
        self.assertTrue(any("Fecha: 2023-01-01, Motivo consulta: Vacunación, Diagnóstico: Aplicada vacuna antirrábica" in line for line in printed_lines))

# Pruebas unitarias para las funciones del módulo persistencia.py
class TestPersistencia(unittest.TestCase):
    
    # Configuración inicial para las pruebas
    def setUp(self):
        mascotas.clear()
        
        # Crear datos de prueba
        dueno1 = Dueno("Laura", "555-3333", "Calle 3")
        mascota1 = Mascota("Milo", "Gato", "Persa", 3, dueno1)
        mascotas.append(mascota1)
        
        dueno2 = Dueno("Pedro", "555-4444", "Calle 4")
        mascota2 = Mascota("Bella", "Perro", "Golden", 5, dueno2)
        mascota2.agregar_consulta(Consulta("2023-02-01", "Dolor", "Artritis", mascota2))
        mascotas.append(mascota2)
        
        # Configurar logging para capturar salida
        self.log_stream = StringIO()
        logging.basicConfig(stream=self.log_stream, level=logging.INFO)
        
        # Eliminar archivos de prueba si existen
        if os.path.exists(archivo_csv):
            os.remove(archivo_csv)
        if os.path.exists(archivo_json):
            os.remove(archivo_json)
    
    # Limpieza después de cada prueba
    def tearDown(self):
        mascotas.clear()
        logging.getLogger().handlers.clear()
        
        # Eliminar archivos de prueba si existen
        if os.path.exists(archivo_csv):
            os.remove(archivo_csv)
        if os.path.exists(archivo_json):
            os.remove(archivo_json)
    
    # Verifica el guardado y carga correcta de datos CSV
    def test_guardar_cargar_csv(self):
        # Guardar datos
        guardar_mascotas_csv()
        self.assertTrue(os.path.exists(archivo_csv))
        
        # Verificar contenido del archivo
        with open(archivo_csv, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 3)  # Encabezado + 2 mascotas
            self.assertIn("Milo", rows[1])
            self.assertIn("Bella", rows[2])
        
        # Limpiar datos y cargar desde archivo
        mascotas.clear()
        cargar_mascotas_csv()
        self.assertEqual(len(mascotas), 2)
        self.assertEqual(mascotas[0].nombre, "Milo")
        self.assertEqual(mascotas[1].dueno.nombre, "Pedro")
        
        logs = self.log_stream.getvalue()
        self.assertIn("Datos de mascotas y dueños guardados en CSV exitosamente", logs)
        self.assertIn("Datos de mascotas y dueños cargados desde CSV exitosamente", logs)
    
    # Verifica el guardado y carga correcta de datos JSON
    def test_guardar_cargar_json(self):
        # Guardar datos
        guardar_consultas_json()
        self.assertTrue(os.path.exists(archivo_json))
        
        # Verificar contenido del archivo
        with open(archivo_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)  # Solo Bella tiene consulta
            self.assertEqual(data[0]['nombre_mascota'], "Bella")
            self.assertEqual(data[0]['motivo'], "Dolor")
        
        # Limpiar consultas y cargar desde archivo
        for m in mascotas:
            m.consultas.clear()
        cargar_consultas_json()
        self.assertEqual(len(mascotas[1].consultas), 1)  # Bella debería tener su consulta de vuelta
        self.assertEqual(mascotas[1].consultas[0].diagnostico, "Artritis")
        
        logs = self.log_stream.getvalue()
        self.assertIn("Consultas guardadas en JSON exitosamente", logs)
        self.assertIn("Consultas cargadas desde JSON exitosamente", logs)
    
    # Verifica el manejo de archivo CSV inexistente
    def test_cargar_csv_inexistente(self):
        cargar_mascotas_csv()
        logs = self.log_stream.getvalue()
        self.assertIn("Archivo CSV de mascotas no encontrado", logs)
    
    # Verifica el manejo de archivo JSON inexistente
    def test_cargar_json_inexistente(self):
        cargar_consultas_json()
        logs = self.log_stream.getvalue()
        self.assertIn("Archivo JSON de consultas no encontrado", logs)

# Ejecución de las pruebas unitarias
if __name__ == '__main__':
    unittest.main(verbosity=2)