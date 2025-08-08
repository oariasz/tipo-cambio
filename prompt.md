# Prompt Configurable para ChatGPT 4.1: API de Tipo de Cambio BCV

---

## VARIABLES CONFIGURABLES

- **PROYECTO_NOMBRE:** tipo-cambio  
- **ARCHIVO_MAIN:** bcv-hoy.py  
- **NOMBRE_API:** bcv-hoy  
- **ENDPOINT:** /bcv-hoy  
- **SUBDOMINIO_API:** api.estratekdata.com  
- **PYTHON_VERSION:** 3.11  
- **USUARIO_GITHUB:** oariasz  
- **AUTOR:** Omar Arias  
- **LICENCIA:** Apache-2.0  
- **README_FILENAME:** README.md  
- **LICENSE_FILENAME:** LICENSE.txt  

---

## PROMPT

Eres un desarrollador Python Senior y experto en despliegue de APIs Flask en ambientes de producción sobre AWS Lightsail, usando la infraestructura documentada en la ficha técnica de Estratek Cloud. Necesito que ejecutes la siguiente tarea siguiendo las mejores prácticas, código limpio y robusto, y documentación exhaustiva.  
Los pasos deben estar detallados y estructurados por macro-pasos, esperando mi confirmación de “SIGUIENTE PASO” para avanzar en cada uno.

---

### TAREA PRINCIPAL

Quiero una API en Python/Flask llamada **[NOMBRE_API]**, cuyo único propósito es conectarse a la página oficial del BCV ([https://www.bcv.org.ve/seccionportal/tipo-de-cambio-oficial-del-bcv](https://www.bcv.org.ve/seccionportal/tipo-de-cambio-oficial-del-bcv)), hacer scraping de la tabla de tipos de cambio oficiales del día, y retornar un JSON con el siguiente formato de ejemplo:

```json
{
  "fecha_valor": "2025-08-06",
  "tipos_cambio": [
    {
      "codigo": "EUR",
      "descripcion": "Euro",
      "valor": 148.20416090
    }
    // ...etc.
  ]
}
