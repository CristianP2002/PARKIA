# models/descuento.py
from models.database import Database

class Descuento:
    def __init__(self):
        self.db = Database()

    def crear_codigo(self, codigo: str, porcentaje: float):
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO descuentos (codigo, porcentaje, activo) VALUES (?, ?, 1)", (codigo.upper().strip(), porcentaje))
        conn.commit()
        conn.close()

    def validar_codigo(self, codigo: str) -> float:
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT porcentaje FROM descuentos WHERE codigo = ? AND activo = 1", (codigo.upper().strip(),))
        fila = cursor.fetchone()
        conn.close()
        return fila[0] if fila else 0.0