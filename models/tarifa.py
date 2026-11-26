# models/tarifa.py
from models.database import Database

class Tarifa:
    def __init__(self):
        self.db = Database()

    def obtener_tarifa(self):
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT valor_hora, valor_fraccion FROM tarifas WHERE id = 1")
        fila = cursor.fetchone()
        conn.close()
        return {"hora": fila[0], "fraccion": fila[1]}

    def actualizar_tarifa(self, valor_hora: float, valor_fraccion: float):
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE tarifas SET valor_hora = ?, valor_fraccion = ? WHERE id = 1", (valor_hora, valor_fraccion))
        conn.commit()
        conn.close()