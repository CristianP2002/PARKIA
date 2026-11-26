# models/database.py
import sqlite3

class Database:
    def __init__(self, db_name="parkia.db"):
        self.db_name = db_name
        self.crear_tablas()

    def conectar(self):
        return sqlite3.connect(self.db_name, check_same_thread=False)

    def crear_tablas(self):
        conn = self.conectar()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tarifas (
                id INTEGER PRIMARY KEY,
                valor_hora REAL NOT NULL,
                valor_fraccion REAL NOT NULL
            )
        """)
        cursor.execute("INSERT OR IGNORE INTO tarifas (id, valor_hora, valor_fraccion) VALUES (1, 4000, 1500)")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehiculos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                placa TEXT NOT NULL,
                tipo TEXT NOT NULL,
                hora_entrada TEXT NOT NULL,
                hora_salida TEXT,
                estado TEXT DEFAULT 'ACTIVO'
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS descuentos (
                codigo TEXT PRIMARY KEY,
                porcentaje REAL NOT NULL,
                activo INTEGER DEFAULT 1
            )
        """)

        cursor.execute("""
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
        conn.commit()
        conn.close()