"""Consumo de API externa de clima.

Se utiliza la librería oficial 'requests' para realizar solicitudes HTTP y
procesar respuestas JSON. La clave de API (si se usa OpenWeatherMap) se
obtiene desde variables de entorno para evitar su exposición en el código.
"""
import os
import requests
from SEGURIDAD.validaciones import validar_ciudad, sanitizar_texto


class ClimaService:
    def __init__(self):
        self.openweather_key = os.getenv("OPENWEATHER_API_KEY", "").strip()
        self.timeout = 10

    def obtener_clima(self, ciudad):
        """Obtiene el clima actual de una ciudad.

        Retorna un diccionario con datos normalizados o lanza ValueError/Exception.
        """
        ok, msg = validar_ciudad(ciudad)
        if not ok:
            raise ValueError(msg)
        ciudad = sanitizar_texto(ciudad, 80)

        # Si hay clave de API, se usa OpenWeatherMap (servicio que requiere key).
        if self.openweather_key:
            return self._clima_openweather(ciudad)
        # Alternativa sin clave: Open-Meteo + geocodificación (sin API key).
        return self._clima_openmeteo(ciudad)

    def _clima_openweather(self, ciudad):
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": ciudad,
            "appid": self.openweather_key,
            "units": "metric",
            "lang": "es",
        }
        try:
            resp = requests.get(url, params=params, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Error al consultar OpenWeatherMap: {e}")

        return {
            "fuente": "OpenWeatherMap",
            "ciudad": data.get("name", ciudad),
            "pais": data.get("sys", {}).get("country", ""),
            "temperatura": data.get("main", {}).get("temp"),
            "sensacion": data.get("main", {}).get("feels_like"),
            "humedad": data.get("main", {}).get("humidity"),
            "descripcion": data.get("weather", [{}])[0].get("description", ""),
            "viento": data.get("wind", {}).get("speed"),
        }

    def _clima_openmeteo(self, ciudad):
        # 1) Geocodificación (sin API key)
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        try:
            geo_resp = requests.get(geo_url, params={"name": ciudad, "count": 1, "language": "es"}, timeout=self.timeout)
            geo_resp.raise_for_status()
            geo_data = geo_resp.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Error en geocodificación: {e}")

        resultados = geo_data.get("results") or []
        if not resultados:
            raise ValueError(f"No se encontró la ciudad '{ciudad}'.")
        lugar = resultados[0]
        lat = lugar["latitude"]
        lon = lugar["longitude"]
        nombre = lugar.get("name", ciudad)
        pais = lugar.get("country", "")

        # 2) Clima actual
        weather_url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
        }
        try:
            w_resp = requests.get(weather_url, params=params, timeout=self.timeout)
            w_resp.raise_for_status()
            w_data = w_resp.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Error al consultar Open-Meteo: {e}")

        current = w_data.get("current_weather", {})
        return {
            "fuente": "Open-Meteo",
            "ciudad": nombre,
            "pais": pais,
            "temperatura": current.get("temperature"),
            "sensacion": None,
            "humedad": None,
            "descripcion": f"Código clima: {current.get('weathercode')}",
            "viento": current.get("windspeed"),
        }
