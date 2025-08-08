import requests
from flask import Flask, Response
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime, timezone, timedelta
import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class BsScraper:
    URL_BCV = "https://www.bcv.org.ve/seccionportal/tipo-de-cambio-oficial-del-bcv"
    URL_TCAMBIO = "https://www.tcambio.app/"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    DESCRIPCIONES = {
        "EUR": "Euro",
        "CNY": "Yuan chino",
        "TRY": "Lira turca",
        "RUB": "Rublo ruso",
        "USD": "Dólar estadounidense",
    }

    def _get_tasa_internacional(self, codigo_moneda, usd_ves):
        """
        Obtiene la tasa oficial de la moneda contra USD desde exchangerate.host,
        y calcula el valor aproximado en VES usando el USD de tcambio.app.

        # ALERTA de Mantenimiento:
        # Si alguna tasa retorna 'None' (null en JSON), probablemente es porque exchangerate.host
        # no tiene ese símbolo, la tasa está desactualizada o hay error de red.
        # Para agregar nuevas monedas o cambiar de proveedor:
        # - Verifica la documentación oficial de exchangerate.host: https://exchangerate.host/#/#docs
        # - Si necesitas mayor confiabilidad, puedes alternar con otros proveedores como:
        #   Open Exchange Rates, Fixer.io, o APIs oficiales de bancos centrales.
        # - Si cambian los símbolos o endpoints, ajusta la URL de la request aquí.
        # - Si deseas cambiar la fuente, puedes implementar aquí el nuevo fetch.
        """
        
        try:
            url = f"https://api.exchangerate.host/latest?base={codigo_moneda}&symbols=USD"
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            rate = r.json()["rates"]["USD"]
            if rate and usd_ves:
                valor_bcv = round((1 / rate) * usd_ves, 6)
            else:
                valor_bcv = None
        except Exception as ex:
            print(f"[ERROR] {codigo_moneda}: {ex}")
            valor_bcv = None
        return valor_bcv

    def fetchBCV(self):
        """Scrapea la web oficial del BCV para obtener los tipos de cambio."""
        headers = {"User-Agent": self.USER_AGENT}
        resp = requests.get(self.URL_BCV, headers=headers, timeout=15, verify=False)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        tipos_cambio = []
        ids = ["euro", "yuan", "lira", "rublo", "dolar"]
        codigos = ["EUR", "CNY", "TRY", "RUB", "USD"]

        for i, div_id in enumerate(ids):
            div = soup.find("div", id=div_id)
            if not div:
                continue
            span = div.find("span")
            codigo = span.text.strip() if span else codigos[i]
            codigo = codigo.replace(" ", "").upper()
            descripcion = self.DESCRIPCIONES.get(codigo, codigo)
            valor_tag = div.find("strong")
            if not valor_tag:
                continue
            valor_str = valor_tag.text.strip().replace(".", "").replace(",", ".")
            try:
                valor = float(valor_str)
            except Exception:
                valor = None

            tipos_cambio.append({
                "codigo": codigo,
                "descripcion": descripcion,
                "valor": valor
            })

        # Buscar la fecha valor
        fecha_valor = None
        fecha_div = soup.find(string=re.compile("Fecha Valor"))
        if fecha_div:
            m = re.search(r"(\d{2})\s*(?:de)?\s*([A-Za-záéíóú]+)\s*(\d{4})", fecha_div)
            if m:
                day, month_name, year = m.groups()
                month_map = {
                    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
                    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
                    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
                }
                month = month_map.get(month_name.lower()[:len(month_name.lower())-1] if month_name.lower().endswith('.') else month_name.lower(), "01")
                fecha_valor = f"{year}-{month}-{day}"
        if not fecha_valor:
            fecha_span = soup.find("span", class_="date-display-single")
            if fecha_span and fecha_span.has_attr("content"):
                fecha_valor = fecha_span["content"][:10]
            else:
                fecha_valor = datetime.now().strftime("%Y-%m-%d")

        return {
            "fecha_valor": fecha_valor,
            "tipos_cambio": tipos_cambio
        }
    
    def fetchTCambio(self):
        """
        Scrapea tcambio.app para obtener USD oficial BCV,
        fecha valor, timestamp y tasas internacionales convertidas con exchangerate.host.
        """
        headers = {"User-Agent": self.USER_AGENT}
        resp = requests.get(self.URL_TCAMBIO, headers=headers, timeout=15, verify=False)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # --- Buscar valor USD en el bloque principal ---
        usd_valor = None
        usd_box = soup.find(string=re.compile(r"Bs\.S\s*\d+[\.,]\d+", re.I))
        if usd_box:
            match = re.search(r"Bs\.S\s*([0-9]+[\.,][0-9]+)", usd_box)
            if match:
                valor_str = match.group(1).replace(",", ".")
                try:
                    usd_valor = float(valor_str)
                except Exception:
                    usd_valor = None

        tasas = []
        if usd_valor:
            tasas.append({
                "codigo": "USD",
                "descripcion": self.DESCRIPCIONES["USD"],
                "valor": usd_valor
            })

        # --- Buscar la fecha valor publicada (Ej: 'Ultima actualización 08/08/2025') ---
        fecha_valor = None
        fecha_box = soup.find(string=re.compile(r"Ultima actualización", re.I))
        if fecha_box:
            match = re.search(r"(\d{2})/(\d{2})/(\d{4})", fecha_box)
            if match:
                dia, mes, anio = match.groups()
                fecha_valor = f"{anio}-{mes}-{dia}"
        if not fecha_valor:
            fecha_valor = datetime.now(timezone(timedelta(hours=-4))).strftime("%Y-%m-%d")

        # --- Timestamp de consulta (GMT-4) ---
        now_gmt4 = datetime.now(timezone(timedelta(hours=-4)))
        timestamp = now_gmt4.strftime("%Y-%m-%d %H:%M:%S %z")

        # --- Tasas internacionales (EUR, CNY, RUB, TRY) ---
        conversiones = [
            ("EUR", "Euro"),
            ("CNY", "Yuan chino"),
            ("RUB", "Rublo ruso"),
            ("TRY", "Lira turca"),
        ]
        tasas_calculadas = []
        for codigo, descripcion in conversiones:
            valor_bcv = self._get_tasa_internacional(codigo, usd_valor)
            tasas_calculadas.append({
                "codigo": codigo,
                "descripcion": descripcion,
                "valor": valor_bcv
            })

        return {
            "fecha_valor": fecha_valor,
            "tipos_cambio": tasas,
            "timestamp": timestamp,
            "tasas_calculadas": tasas_calculadas
        }

# --- FLASK API ---
app = Flask(__name__)

@app.route("/bcv-hoy", methods=["GET"])
def bcv_hoy():
    scraper = BsScraper()
    try:
        response = scraper.fetchTCambio()
        return Response(
            json.dumps(response, ensure_ascii=False),
            mimetype="application/json"
        )
    except Exception as e:
        return Response(
            json.dumps({"error": str(e)}, ensure_ascii=False),
            mimetype="application/json",
            status=500
        )

if __name__ == "__main__":
    app.run(debug=True, port=5077)