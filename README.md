# API de Tipo de Cambio Oficial - Venezuela (Estratek Cloud)

Esta API expone el tipo de cambio oficial publicado por el BCV, así como tasas internacionales de referencia para EUR, CNY, RUB y TRY, usando fuentes públicas y de costo cero.

## 📌 Descripción

- Scrapea el tipo de cambio USD/VEF oficial publicado en [tcambio.app](https://www.tcambio.app/).
- Devuelve la fecha valor, el valor oficial USD/VEF, un timestamp de consulta (GMT-4) y tasas aproximadas de otras monedas calculadas con [exchangerate.host](https://exchangerate.host/).
- Soporta despliegue local o en AWS (Lightsail).

---

## 🚀 Cómo instalar y correr localmente

1. Clona el repositorio y entra al directorio del proyecto:
   ```bash
   git clone https://github.com/[TU_USUARIO]/tipo-cambio.git
   cd tipo-cambio
   ```
2. Crea un entorno virtual (Python 3.11 recomendado) e instálalo:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
   Lanza el servidor Flask:

   ```bash
   python bcv-hoy.py
   ```

El API quedará disponible en http://127.0.0.1:5077/bcv-hoy

🧾 Ejemplo de uso
```bash
curl http://127.0.0.1:5077/bcv-hoy
```

Ejemplo de respuesta
```json
{
  "fecha_valor": "2025-08-08",
  "tipos_cambio": [
    {
      "codigo": "USD",
      "descripcion": "Dólar estadounidense",
      "valor": 130.07
    }
  ],
  "timestamp": "2025-08-08 02:28:54 -0400",
  "tasas_calculadas": [
    {
      "codigo": "EUR",
      "descripcion": "Euro",
      "valor": 140.422411
    },
    {
      "codigo": "CNY",
      "descripcion": "Yuan chino",
      "valor": 17.958333
    },
    {
      "codigo": "RUB",
      "descripcion": "Rublo ruso",
      "valor": 1.455934
    },
    {
      "codigo": "TRY",
      "descripcion": "Lira turca",
      "valor": 4.342345
    }
  ]
}
```

⚠️ Nota sobre tasas internacionales (tasas_calculadas)
Las tasas calculadas de EUR, CNY, RUB y TRY se obtienen usando la API pública exchangerate.host.
Esta solución es de costo cero y generalmente confiable, pero no garantiza la disponibilidad de todos los símbolos o tasas actualizadas en todo momento.

Si alguna tasa aparece como null en la respuesta JSON:

Probablemente la tasa no está disponible en exchangerate.host para el símbolo consultado, o hay un problema temporal de red.

Puedes verificar manualmente en:
https://api.exchangerate.host/latest?base=EUR&symbols=USD
(Cambia EUR por el código que necesites.)


##### ¿Cómo mejorar o mantener este cálculo en el futuro?

Si necesitas mayor confiabilidad o monedas adicionales, puedes cambiar el método interno _get_tasa_internacional en el código.

Puedes alternar con otros proveedores como Open Exchange Rates, Fixer.io o APIs oficiales de bancos centrales.

Si cambian los endpoints, revisa la documentación oficial de exchangerate.host o de tu nuevo proveedor.

##### ¿Por qué se usan tasas inversas?

La API da la tasa de la moneda base respecto a USD (ej: EUR/USD), y el valor en Bs se calcula como (1 / tasa) * USD_BCV para mantener la lógica "cuántos Bs por unidad de la moneda extranjera".

##### Advertencia:
Esta API debe ser considerada solo como referencial y para propósitos informativos, no como fuente oficial para operaciones financieras críticas.


👤 Autor
Omar Arias

https://omararias.com

Estratek Cloud