# models/vehiculo.py
from datetime import datetime
import math
from models.database import Database
from models.tarifa import Tarifa

class Vehiculo:
    def __init__(self):
        self.db = Database()
        self.tarifa_model = Tarifa()

    def registrar_entrada(self, placa: str, tipo: str = "Carro"):
        conn = self.db.conectar()
        cursor = conn.cursor()
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO vehiculos (placa, tipo, hora_entrada) VALUES (?, ?, ?)", (placa.upper().strip(), tipo, ahora))
        conn.commit()
        conn.close()

    def obtener_activos(self):
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, placa, tipo, hora_entrada FROM vehiculos WHERE estado = 'ACTIVO'")
        filas = cursor.fetchall()
        conn.close()
        return filas

    def calcular_cobro(self, hora_entrada_str: str):
        entrada = datetime.strptime(hora_entrada_str, "%Y-%m-%d %H:%M:%S")
        ahora = datetime.now()
        minutos_totales = max(1, (ahora - entrada).total_seconds() / 60)
        
        tarifas = self.tarifa_model.obtener_tarifa()
        horas_completas = int(minutos_totales // 60)
        minutos_restantes = minutos_totales % 60
        fracciones = math.ceil(minutos_restantes / 15) if minutos_restantes > 0 else 0

        total = (horas_completas * tarifas["hora"]) + (fracciones * tarifas["fraccion"])
        return {
            "minutos": round(minutos_totales, 1),
            "total_bruto": total,
            "hora_salida": ahora.strftime("%Y-%m-%d %H:%M:%S")
        }

    def marcar_salida(self, vehiculo_id: int, hora_salida: str):
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE vehiculos SET hora_salida = ?, estado = 'FINALIZADO' WHERE id = ?", (hora_salida, vehiculo_id))
        conn.commit()
        conn.close()