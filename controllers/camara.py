import re
import cv2
import easyocr

class CamaraController:
    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=False)

    def leer_placa_desde_celular(self, url_camara: str) -> str:
        """
        url_camara ejemplo con app IP Webcam: 'http://192.168.1.50:8080/video'
        """
        cap = cv2.VideoCapture(url_camara)
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return ""

        resultados = self.reader.readtext(frame, detail=0)
        for texto in resultados:
            limpio = re.sub(r'[^A-Z0-9]', '', texto.upper())
            
            if re.match(r'^[A-Z]{3}[0-9]{2,3}[A-Z0-9]?$', limpio):
                return limpio
        return ""