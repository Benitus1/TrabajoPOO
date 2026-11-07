"""Consumo de API externa de tipo de cambio / indicadores económicos.

Fuente: mindicador.cl (sin API key). Se valida el código del indicador
para evitar inyección en la URL.
"""
import requests
from SEGURIDAD.validaciones import validar_codigo_moneda, sanitizar_texto


INDICADORES_PERMITIDOS = {
    "dolar": "Dólar (CLP)",
    "euro": "Euro (CLP)",
    "uf": "Unidad de Fomento (CLP)",
    "utm": "UTM (CLP)",
    "bitcoin": "Bitcoin (CLP)",
}


class IndicadoresService:
    def __init__(self):
        self.base_url = "https://mindicador.cl/api"
        self.timeout = 10

    def listar_indicadores(self):
        try:
            resp = requests.get(self.base_url, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Error al consultar mindicador.cl: {e}")
        # Devolver solo indicadores conocidos con su valor actual
        resultado = {}
        for codigo, nombre in INDICADORES_PERMITIDOS.items():
            info = data.get(codigo)
            if info:
                resultado[codigo] = {
                    "nombre": nombre,
                    "valor": info.get("valor"),
                    "fecha": info.get("fecha"),
                }
        return resultado

    def obtener_indicador(self, codigo):
        codigo = sanitizar_texto(codigo, 20).lower()
        if codigo not in INDICADORES_PERMITIDOS:
            raise ValueError(
                f"Indicador no permitido. Opciones: {', '.join(INDICADORES_PERMITIDOS.keys())}"
            )
        url = f"{self.base_url}/{codigo}"
        try:
            resp = requests.get(url, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Error al consultar indicador '{codigo}': {e}")

        serie = data.get("serie", [])
        ultimo = serie[0] if serie else {}
        return {
            "codigo": codigo,
            "nombre": INDICADORES_PERMITIDOS[codigo],
            "valor": ultimo.get("valor", data.get("valor")),
            "fecha": ultimo.get("fecha", data.get("fecha")),
        }

    def convertir(self, monto, moneda_origen, moneda_destino):
        """Conversión simple usando indicadores en CLP."""
        moneda_origen = moneda_origen.upper()
        moneda_destino = moneda_destino.upper()
        # Solo se soporta conversión hacia/desde CLP con indicadores disponibles.
        if moneda_origen == "CLP" and moneda_destino in ("USD", "EUR"):
            ind = "dolar" if moneda_destino == "USD" else "euro"
            info = self.obtener_indicador(ind)
            valor = info["valor"]
            return monto / valor if valor else None, info
        if moneda_destino == "CLP" and moneda_origen in ("USD", "EUR"):
            ind = "dolar" if moneda_origen == "USD" else "euro"
            info = self.obtener_indicador(ind)
            valor = info["valor"]
            return monto * valor if valor else None, info
        raise ValueError("Conversión no soportada. Use CLP <-> USD o CLP <-> EUR.")
