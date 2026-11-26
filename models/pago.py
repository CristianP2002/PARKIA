import io
import base64
from datetime import datetime
import qrcode
from models.database import Database

class Pago:
    def __init__(self):
        self.db = Database()

    def generar_qr_base64(self, placa: str, monto: float) -> str:
        datos_pago = f"PARKIA-PAY|PLACA:{placa}|TOTAL:${monto:.2f}|REF:{datetime.now().strftime('%H%M%S')}"
        qr = qrcode.make(datos_pago)
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def registrar_pago(self, vehiculo_id: int, bruto: float, descuento: float, final: float, metodo: str):
        conn = self.db.conectar()
        cursor = conn.cursor()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO pagos (vehiculo_id, monto_bruto, descuento_aplicado, monto_final, metodo_pago, fecha_pago)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (vehiculo_id, bruto, descuento, final, metodo, fecha))
        conn.commit()
        conn.close()