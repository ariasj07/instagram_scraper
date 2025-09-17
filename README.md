# Instagram Scraper

Instagram Scraper es un script en Python que automatiza la obtención y descarga de todas las publicaciones disponibles en un perfil de Instagram al que tengas acceso. Utiliza la API privada que alimenta la web de Instagram, por lo que resulta ideal para crear copias de seguridad personales o para analizar contenido sin depender de herramientas de terceros.

## Características principales
- Extrae todos los enlaces de imágenes y vídeos publicados en el perfil indicado.
- Detecta automáticamente carruseles y descarga cada elemento por separado.
- Guarda los archivos en una estructura de carpetas sencilla (`<usuario>/media`).
- Funciona con perfiles públicos y privados (siempre que sigas al perfil privado y tus cookies sean válidas).

## Requisitos previos
- Python 3.10 o superior.
- `pip` para instalar dependencias.
- La biblioteca [`requests`](https://requests.readthedocs.io/) instalada en tu entorno.
- Una cuenta de Instagram con la que puedas iniciar sesión en la versión web para obtener las cookies `sessionid` y `csrftoken`.

## Instalación rápida
```bash
# Clona el repositorio
git clone https://github.com/<tu-usuario>/instagram_scraper.git
cd instagram_scraper

# (Opcional) crea y activa un entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows usa: .venv\Scripts\activate

# Instala la dependencia necesaria
pip install requests
```

## Configuración de credenciales
El script requiere dos cookies válidas para autenticarte frente a Instagram:

- **`sessionid`**: identifica tu sesión iniciada.
- **`csrftoken`**: token asociado a tu sesión para proteger peticiones.

Puedes obtener estos valores desde las herramientas de desarrollador de tu navegador (pestaña *Application* o *Storage* → *Cookies* → `https://www.instagram.com`). Consulta la [guía detallada](docs/guia_de_uso.md#2-obtener-las-cookies-necesarias) para ver el proceso paso a paso.

> ⚠️ Las cookies expiran con el tiempo. Si recibes errores de autenticación, repite el proceso y reemplaza los valores.

## Ejemplo mínimo de uso
```python
from instagram import InstagramScraper

scraper = InstagramScraper(
    sessionid="TU_SESSION_ID",
    csrftoken="TU_CSRF_TOKEN",
    user_name="usuario_a_descargar"
)

# Recupera todos los enlaces disponibles en la cronología
links = scraper.get_all_media_links()
print(f"Se encontraron {len(links)} elementos")

# Descarga cada archivo en <usuario>/media
scraper.download_all_media_links()
```

Si prefieres no exponer las cookies en el código, puedes almacenarlas en variables de entorno y leerlas con `os.getenv` antes de instanciar la clase.

## Estructura de salida
Por defecto, los archivos descargados se guardan en la ruta `<usuario>/media`. Las imágenes se exportan con extensión `.png` y los vídeos con extensión `.mp4`. Si Instagram devuelve un formato desconocido, el script mostrará un mensaje indicando que el tipo de contenido no fue reconocido.

## Documentación adicional
- [Guía de uso paso a paso](docs/guia_de_uso.md)
- [Referencia de la clase `InstagramScraper`](docs/api_reference.md)

## Limitaciones y aviso legal
- Instagram puede modificar la API privada en cualquier momento, lo que dejaría de funcionar el `doc_id` utilizado internamente.
- El uso de este proyecto debe respetar los términos de servicio de Instagram y la legislación vigente sobre protección de datos y derechos de autor.
- Descarga únicamente contenido para el que tengas permiso expreso.

## Contribuciones y soporte
Las contribuciones son bienvenidas mediante *pull requests*. Si encuentras un error o necesitas una mejora, abre un *issue* describiendo los detalles del problema y los pasos para reproducirlo. Para dudas rápidas consulta primero la documentación incluida en la carpeta [`docs`](docs/).
