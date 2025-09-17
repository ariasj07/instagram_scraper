# Guía de uso paso a paso

Esta guía amplía la información del README y te acompaña desde la preparación del entorno hasta la descarga de los archivos. Está pensada para personas que no están familiarizadas con la API de Instagram pero necesitan automatizar la creación de copias de seguridad de un perfil.

## 1. Preparar el entorno de trabajo
1. Asegúrate de tener instalado **Python 3.10 o superior**. Puedes comprobarlo con:
   ```bash
   python --version
   ```
2. (Opcional) Crea un entorno virtual para aislar la instalación del proyecto:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows usa: .venv\Scripts\activate
   ```
3. Instala la dependencia necesaria:
   ```bash
   pip install requests
   ```

## 2. Obtener las cookies necesarias
El scraper se apoya en tu sesión de Instagram abierta en el navegador para acceder a la información del perfil. Necesitas copiar dos cookies: `sessionid` y `csrftoken`.

1. Abre [https://www.instagram.com](https://www.instagram.com) y asegúrate de que has iniciado sesión con la cuenta que tiene acceso al perfil que quieres descargar.
2. Abre las **herramientas de desarrollador** del navegador. En la mayoría de navegadores puedes hacerlo con `F12` o `Ctrl`+`Shift`+`I` (`Cmd`+`Option`+`I` en macOS).
3. Busca la sección de almacenamiento de cookies:
   - **Chrome / Edge**: pestaña *Application* → *Storage* → *Cookies* → `https://www.instagram.com`.
   - **Firefox**: pestaña *Storage* → *Cookies* → `https://www.instagram.com`.
4. Localiza las entradas llamadas `sessionid` y `csrftoken`. Copia los valores de cada una y guárdalos temporalmente en un lugar seguro.

> 💡 Mantén estas cadenas en privado. Dan acceso completo a tu sesión hasta que expiren o cierres sesión.

### Guardar las cookies como variables de entorno (opcional pero recomendado)
En lugar de pegarlas directamente en el código puedes almacenarlas como variables de entorno para reducir el riesgo de exposición:

```bash
export IG_SESSIONID="valor_de_tu_sessionid"
export IG_CSRFTOKEN="valor_de_tu_csrftoken"
```

En Windows PowerShell utiliza:

```powershell
setx IG_SESSIONID "valor_de_tu_sessionid"
setx IG_CSRFTOKEN "valor_de_tu_csrftoken"
```

Más tarde podrás leerlas en Python con `os.getenv("IG_SESSIONID")` y `os.getenv("IG_CSRFTOKEN")`.

## 3. Ejecutar el scraper
1. Crea un archivo `main.py` (o edita `instagram.py`) con el siguiente contenido:
   ```python
   import os
   from instagram import InstagramScraper

   scraper = InstagramScraper(
       sessionid=os.getenv("IG_SESSIONID"),
       csrftoken=os.getenv("IG_CSRFTOKEN"),
       user_name="usuario_a_descargar"
   )

   enlaces = scraper.get_all_media_links()
   print(f"Se recuperaron {len(enlaces)} elementos")

   scraper.download_all_media_links()
   print("Descarga finalizada")
   ```
2. Ejecuta el script:
   ```bash
   python main.py
   ```
3. Revisa la carpeta creada (`usuario_a_descargar/media`). Dentro encontrarás los archivos numerados en el orden en que fueron recuperados.

## 4. Renovar credenciales caducadas
Instagram invalida las cookies cada cierto tiempo, especialmente si detecta actividad sospechosa. Si ves errores de autenticación o la respuesta no contiene publicaciones:

- Repite el proceso del [apartado 2](#2-obtener-las-cookies-necesarias) para obtener cookies actualizadas.
- Comprueba que sigues teniendo acceso al perfil (en el caso de cuentas privadas).
- Si cambiaste la contraseña recientemente, inicia sesión de nuevo antes de extraer las nuevas cookies.

## 5. Buenas prácticas y recomendaciones
- Respeta los términos de uso de Instagram y solicita autorización antes de descargar contenido ajeno.
- Evita compartir las cookies con terceros. Considéralas equivalentes a una contraseña temporal.
- Para grandes volúmenes de contenido se recomienda realizar pausas manuales entre descargas para no saturar la API.
- Mantén la dependencia `requests` actualizada (`pip install --upgrade requests`) para recibir correcciones de seguridad.

Con estos pasos deberías poder clonar un perfil accesible y descargar todas sus publicaciones disponibles en formato imagen o vídeo.
