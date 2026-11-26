import flet as ft
from controllers.parqueadero import ParqueaderoController
from controllers.camara import CamaraController
from views.app import iniciar_interfaz

def main(page: ft.Page):
    ctrl = ParqueaderoController()
    camara_ctrl = CamaraController()
    iniciar_interfaz(page, ctrl, camara_ctrl)

if __name__ == "__main__":
    ft.app(target=main)