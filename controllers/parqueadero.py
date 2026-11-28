from models.vehiculo import Vehiculo
from models.tarifa import Tarifa
from models.descuento import Descuento
from models.pago import Pago

class ParqueaderoController:
    def __init__(self):
        self.vehiculo_model = Vehiculo()
        self.tarifa_model = Tarifa()
        self.descuento_model = Descuento()
        self.pago_model = Pago()

    def ingresar_vehiculo(self, placa: str, tipo: str):
        if not placa.strip():
            return False, "La placa no puede estar vacía."
        self.vehiculo_model.registrar_entrada(placa, tipo)
        return True, f"Vehículo {placa.upper()} ingresado."

    def listar_vehiculos(self):
        return self.vehiculo_model.obtener_activos()

    def preliquidar(self, hora_entrada: str, codigo_cupon: str = ""):
        calculo = self.vehiculo_model.calcular_cobro(hora_entrada)
        porcentaje = self.descuento_model.validar_codigo(codigo_cupon) if codigo_cupon else 0.0
        valor_descuento = calculo["total_bruto"] * (porcentaje / 100)
        total_final = max(0.0, calculo["total_bruto"] - valor_descuento)
        
        calculo["porcentaje"] = porcentaje
        calculo["descuento"] = valor_descuento
        calculo["total_final"] = total_final
        return calculo

    def procesar_pago(self, vehiculo_id: int, datos_cobro: dict, metodo: str):
        self.pago_model.registrar_pago(
            vehiculo_id,
            datos_cobro["total_bruto"],
            datos_cobro["descuento"],
            datos_cobro["total_final"],
            metodo
        )
        self.vehiculo_model.marcar_salida(vehiculo_id, datos_cobro["hora_salida"])