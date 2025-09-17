"""Herramientas para descargar publicaciones de un perfil de Instagram."""

import json
import os

import requests


class InstagramScraper:
    """Cliente ligero para recuperar y descargar publicaciones de Instagram.

    Args:
        sessionid: Valor de la cookie `sessionid` obtenido tras iniciar sesión en la web.
        csrftoken: Valor de la cookie `csrftoken` asociada a la sesión iniciada.
        user_name: Nombre de usuario del perfil que quieres clonar (sin `@`).

    Attributes:
        doc_id: Identificador del documento GraphQL utilizado por la API privada.
        session: Sesión reutilizable de ``requests`` para mantener las cookies.
        all_images_obtained: Lista acumulada de enlaces a imágenes y vídeos.
    """

    def __init__(self, sessionid: str, csrftoken: str, user_name: str):
        self.doc_id = "32435654999367421"  # Este valor puede cambiar en el futuro
        self.session = requests.Session()
        self.base_url = "https://www.instagram.com/graphql/query"
        self.cookies = {
            "sessionid": sessionid,
            "csrftoken": csrftoken,
        }
        self.all_images_obtained: list[str] = []
        self.user_name = user_name
        self.count = 12
        self.variables = {
            "data": {
                "count": self.count,
                "include_reel_media_seen_timestamp": True,
                "include_relationship_info": True,
                "latest_besties_reel_media": True,
                "latest_reel_media": True,
            },
            "username": self.user_name,
            "__relay_internal__pv__PolarisIsLoggedInrelayprovider": True,
        }
        self.body = {
            "variables": json.dumps(self.variables),
            "doc_id": self.doc_id,
        }
        self.headers = {
            "X-CSRFToken": self.cookies["csrftoken"],
        }

    def get_all_media_links(self) -> list[str]:
        """Recupera las URLs de todas las publicaciones accesibles del perfil.

        Returns:
            list[str]: enlaces de imagen o vídeo listos para descargar.
        """

        while True:
            res = self.session.post(
                self.base_url, cookies=self.cookies, headers=self.headers, data=self.body
            )
            content = res.json()
            posts = content["data"]["xdt_api__v1__feed__user_timeline_graphql_connection"]["edges"]
            for post in posts:
                try:
                    img = post["node"]
                    if img["carousel_media"]:
                        for c in img["carousel_media"]:
                            url = c["image_versions2"]["candidates"][0]["url"]
                            self.all_images_obtained.append(url)
                    elif img["video_versions"]:
                        url = img["video_versions"][0]["url"]
                    else:
                        url = img["image_versions2"]["candidates"][0]["url"]
                    self.all_images_obtained.append(url)
                except Exception as exc:  # pragma: no cover - bloque defensivo
                    print(exc)
            if content["data"]["xdt_api__v1__feed__user_timeline_graphql_connection"]["page_info"]["has_next_page"]:
                self.variables["after"] = content["data"]["xdt_api__v1__feed__user_timeline_graphql_connection"]["page_info"]["end_cursor"]
                self.body["variables"] = json.dumps(self.variables)
            else:
                print(f"Found: {len(self.all_images_obtained)}")
                return self.all_images_obtained

    def download_all_media_links(self) -> None:
        """Descarga todos los enlaces almacenados en ``all_images_obtained``."""

        for x, post in enumerate(self.all_images_obtained):
            path_to_save = f"{self.user_name}/media"
            if os.path.exists(path_to_save):
                pass
            else:
                os.makedirs(path_to_save)
            format_file = requests.get(post).headers["content-type"]
            match format_file:
                case "image/jpeg":
                    with open(f"{path_to_save}/{x}.png", "wb") as f:
                        f.write(requests.get(post).content)
                case "video/mp4":
                    with open(f"{path_to_save}/{x}.mp4", "wb") as f:
                        f.write(requests.get(post).content)
                case _:
                    print(f"The format was not recognized: {format_file}")


if __name__ == "__main__":
    scraper = InstagramScraper(
        sessionid="YOURSESSIONID",
        csrftoken="YOURTOKEN",
        user_name="profile_to_scrape",
    )
    scraper.get_all_media_links()  # <- Obtiene todos los enlaces
    scraper.download_all_media_links()  # <- Descarga todo el contenido
