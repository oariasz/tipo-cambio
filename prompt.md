# Prompt Configurable para ChatGPT 4.1: API de Tipo de Cambio BCV

---

## VARIABLES CONFIGURABLES

- **PROYECTO_NOMBRE:** bcv_hoy  
- **ARCHIVO_MAIN:** bcv_hoy.py  
- **NOMBRE_API:** bcv_hoy  
- **ENDPOINT:** /bcv_hoy  
- **SUBDOMINIO_API:** api.estratekdata.com  
- **PYTHON_VERSION:** 3.11  
- **USUARIO_GITHUB:** oariasz  
- **AUTOR:** Omar Arias  
- **LICENCIA:** Apache-2.0  
- **README_FILENAME:** README.md  
- **LICENSE_FILENAME:** LICENSE.txt  

---

## PROMPT

Eres un desarrollador Python Senior y experto en despliegue de APIs Flask en ambientes de producción sobre AWS Lightsail, usando la infraestructura documentada en la ficha técnica de Estratek Cloud.  
Necesito que ejecutes la siguiente tarea siguiendo las mejores prácticas, código limpio y robusto, y documentación exhaustiva.  
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
    },
    {
      "codigo": "CNY",
      "descripcion": "Yuan chino",
      "valor": 17.85065631
    },
    {
      "codigo": "TRY",
      "descripcion": "Lira turca",
      "valor": 3.15372584
    },
    {
      "codigo": "RUB",
      "descripcion": "Rublo ruso",
      "valor": 1.60178988
    },
    {
      "codigo": "USD",
      "descripcion": "Dólar estadounidense",
      "valor": 128.24090000
    }
    // ...etc.
  ]
}

```
---

### Especificaciones adicionales:

- Las monedas que debe leer están en una imagen adjunta (si falta alguna, ajusta el código para que soporte todos los publicados en esa sección).

- El código debe estar en el archivo principal [ARCHIVO_MAIN] dentro del directorio del proyecto llamado [PROYECTO_NOMBRE]. Usar clases y las mejores prácticas Python.

- El scraping debe simular el user-agent de Chrome (evitar ser bloqueado como bot).

- No debe haber ciclos intensivos ni patrones de ataque, solo una consulta simple por request.

- El scraping puede convertir el HTML a markdown si es útil para el parsing, pero no es obligatorio.

- Esta API será llamada por un workflow en n8n.

- Quiero instrucciones exhaustivas para el deployment en [SUBDOMINIO_API][ENDPOINT] siguiendo los scripts y procedimientos de la ficha técnica de Estratek Cloud.

- Incluye instrucciones para crear el repositorio en GitHub (usuario: [USUARIO_GITHUB]), un [README_FILENAME] explicativo y un [LICENSE_FILENAME] con la licencia [LICENCIA].

- Todo código debe ser probado localmente en Mac antes de deployment.

## MACRO PASOS DETALLADOS

Cada macro paso debe ser respondido con instrucciones exhaustivas, comandos concretos, recomendaciones, validaciones y buenas prácticas.
No avances al siguiente hasta que indique "SIGUIENTE PASO".

1. Creación de Ambiente
    - Indica cómo crear el directorio [PROYECTO_NOMBRE] en local (ejemplo: /Users/<usuario>/dev/Flask/[PROYECTO_NOMBRE]).

    - Instrucciones para crear un entorno virtual en Python [PYTHON_VERSION].

    - Instalación de dependencias necesarias (Flask, requests, beautifulsoup4, etc.).

    - Ejemplo de requirements.txt.

    - Recomendaciones sobre manejo de .env (si aplica).

2. Publicación en GitHub
    - Indica cómo inicializar el repositorio local.

    - Buenas prácticas para .gitignore (por ejemplo: venv, .env).

    - Enlace con GitHub (usuario [USUARIO_GITHUB]), creación de repo remoto y primer push.

    - Proteger credenciales y no subir archivos sensibles.

3. Código y Estructura del Proyecto
    - Presenta la estructura recomendada del directorio y archivos principales, por ejemplo:

        css
        Copiar
        Editar
        [PROYECTO_NOMBRE]/
        ├── [ARCHIVO_MAIN]
        ├── requirements.txt
        ├── .gitignore
        ├── [README_FILENAME]
        └── [LICENSE_FILENAME]

    - Incluye el código de [ARCHIVO_MAIN]: todo en clases, con comentarios breves y siguiendo mejores prácticas.

    - Explica los métodos principales (por ejemplo: método para scraping, método para formateo de respuesta JSON).

    - Ejemplo de uso/curl.

4. Pruebas Locales en Mac

    - Cómo activar el entorno y lanzar el servidor Flask localmente.

    - Comprobar endpoint y ejemplo de respuesta.

    - Debugging básico si ocurre error.

    - Prueba del scraping en diferentes días (si es posible).

5. Deployment en el servidor
Instrucciones para transferir el directorio al servidor etk-web de acuerdo a la ficha técnica (vía scp).
    - Acceso por SSH, creación/activación del virtualenv.
    - Instalación de dependencias en el servidor.
    - Uso del script de deployment etk_deploy.sh para publicar en [SUBDOMINIO_API    ENDPOINT].
    - Validaciones post-deployment (logs, acceso vía HTTPS, revisión en Apache).
    - Reglas de backup y validación de sintaxis antes de reiniciar servicios.    
    
6. Documentación y Licenciamiento
    - Crear un [README_FILENAME] con:
    - Descripción de la API.
    - Cómo instalar y correr localmente.
    - Ejemplo de request/response.
    - Endpoint publicado.
    - Autor: [AUTOR]
    - Dependencias.
    - Ejemplos de uso (curl, Python requests).

    - Crear un [LICENSE_FILENAME] con la licencia [LICENCIA] (formato oficial Apache-2.0).

### REQUISITOS ADICIONALES

- No realizar ningún cambio que ponga en riesgo la disponibilidad de los sitios omararias.com o estratekdata.com.
- Todo deployment debe seguir el flujo de backup, validación de sintaxis, y logs según la ficha técnica.
- Comenta brevemente las funciones y las partes críticas del código.

