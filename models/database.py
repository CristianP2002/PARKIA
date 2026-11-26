# models/database.py
import sqlite3

class BaseDeDatos:
    def __init__(self, nombre_bd="parkia.db"):
        self.nombre_bd = nombre_bd
        self.crear_tablas()

    def conectar(self):
        # Crea la conexión con el archivo de la base de datos
        return sqlite3.connect(self.nombre_bd)

    def crear_tablas(self):
        # 'with' guarda los cambios automáticamente al terminar
        with self.conectar() as conexion:
            
            # 1. Tabla de tarifas
            conexion.execute("""
                CREATE TABLE IF NOT EXISTS tarifas (
                    id INTEGER PRIMARY KEY,
                    valor_hora REAL,
                    valor_fraccion REAL
                )
            """)
            # Guarda una tarifa por defecto si la tabla está vacía
            conexion.execute("""
                INSERT OR IGNORE INTO tarifas (id, valor_hora, valor_fraccion) 
                VALUES (1, 4000, 1500)
            """)

            # 2. Tabla de vehículos
            conexion.execute("""
                CREATE TABLE IF NOT EXISTS vehiculos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    placa TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    hora_entrada TEXT NOT NULL,
                    hora_salida TEXT,
                    estado TEXT DEFAULT 'ACTIVO'
                )
            """)

            # 3. Tabla de descuentos
            conexion.execute("""
                CREATE TABLE IF NOT EXISTS descuentos (
                    codigo TEXT PRIMARY KEY,
                    porcentaje REAL,
                    activo INTEGER DEFAULT 1
                )
            """)

            # 4. Tabla de pagos
            conexion.execute("""
                CREATE TABLE IF NOT EXISTS pagos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehiculo_id INTEGER,
                    monto_bruto REAL,
                    descuento_aplicado REAL,
                    monto_final REAL,
                    metodo_pago TEXT,
                    fecha_pago TEXT
                )
            """)
