# Referencia de la clase `InstagramScraper`

La clase `InstagramScraper` encapsula toda la lógica necesaria para conectarse a Instagram, recuperar las publicaciones disponibles de un perfil y descargar los archivos asociados. A continuación se documentan sus argumentos, atributos y métodos públicos.

## Inicialización
```python
InstagramScraper(sessionid: str, csrftoken: str, user_name: str)
```

| Parámetro   | Tipo | Descripción |
| ----------- | ---- | ----------- |
| `sessionid` | `str` | Valor de la cookie `sessionid` obtenida de tu sesión web autenticada. |
| `csrftoken` | `str` | Valor de la cookie `csrftoken` asociada a tu sesión. |
| `user_name` | `str` | Nombre de usuario del perfil que deseas clonar (sin el símbolo `@`). |

Durante la inicialización se crea una sesión de `requests` reutilizable y se preparan los parámetros necesarios para invocar el endpoint GraphQL privado de Instagram.

### Atributos relevantes
- `doc_id` (`str`): identificador del documento GraphQL utilizado internamente. Si Instagram cambia su API privada este valor puede quedar obsoleto. Puedes sustituirlo manualmente si obtienes uno actualizado.
- `all_images_obtained` (`list[str]`): colección de enlaces recopilados hasta el momento. Se llena al ejecutar `get_all_media_links()`.
- `count` (`int`): número de elementos solicitados por petición. Instagram impone límites, por lo que valores más altos no garantizan más resultados.

## Métodos públicos
### `get_all_media_links() -> list[str]`
Envía solicitudes consecutivas al endpoint privado de Instagram hasta agotar las publicaciones disponibles del perfil. Durante el proceso detecta si un elemento es un carrusel o un vídeo y extrae cada URL individual.

- **Retorno**: una lista con todos los enlaces recopilados en el orden en que Instagram los devuelve (habitualmente de más reciente a más antiguo).
- **Uso típico**:
  ```python
  enlaces = scraper.get_all_media_links()
  for url in enlaces:
      print(url)
  ```
- **Errores**: si la sesión expira o la cuenta pierde acceso al perfil, Instagram devolverá una respuesta de error. En ese caso se imprimirá la excepción capturada y el método terminará devolviendo los enlaces reunidos hasta ese momento.

### `download_all_media_links() -> None`
Recorre la lista interna de enlaces y descarga cada archivo. Para cada elemento:

1. Crea la carpeta `<usuario>/media` en caso de que no exista.
2. Detecta el tipo de contenido a partir de la cabecera `Content-Type`.
3. Guarda las imágenes como `.png` y los vídeos como `.mp4`.
4. Muestra un aviso si encuentra un formato no reconocido.

> **Importante**: este método asume que previamente se ha ejecutado `get_all_media_links()`. Si la lista está vacía no se descargará nada.

## Personalización
- **Cambiar el tamaño de la paginación**: modifica el valor de `self.count` tras crear la instancia para ajustar cuántos elementos se solicitan por petición.
- **Actualizar el `doc_id`**: si Instagram deja de responder, inspecciona las peticiones de la versión web y reemplaza el valor de `self.doc_id` por el más reciente.
- **Descargar en otra ruta**: puedes editar el atributo `path_to_save` dentro de `download_all_media_links()` o adaptar el método para recibir una ruta personalizada.

## Flujo recomendado
1. Instancia la clase con cookies válidas.
2. Ejecuta `get_all_media_links()` para poblar la lista interna de URLs.
3. Llama a `download_all_media_links()` para guardar los archivos.
4. Repite el proceso cada vez que necesites una copia actualizada (recuerda renovar las cookies si expiran).

Esta referencia cubre la API actual del proyecto. Cualquier cambio o método adicional debería documentarse aquí para mantener la consistencia con el código.
