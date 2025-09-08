import os.path
import requests
import json


class InstagramScraper:
    def __init__(self, sessionid: str, csrftoken: str, user_name: str):
        self.doc_id = "32435654999367421"
        self.session = requests.Session()
        self.base_url = "https://www.instagram.com/graphql/query"
        self.cookies = {
            "sessionid": sessionid,
            "csrftoken": csrftoken
        }
        self.all_images_obtained = []
        self.user_name = user_name
        self.count = 12
        self.variables = {
            "data": {
                    "count": self.count, "include_reel_media_seen_timestamp": True, "include_relationship_info": True,
                    "latest_besties_reel_media": True, "latest_reel_media": True
                    },
            "username": self.user_name,
            "__relay_internal__pv__PolarisIsLoggedInrelayprovider": True
        }
        self.body = {
            "variables": json.dumps(self.variables),
            "doc_id": self.doc_id
        }
        self.headers = {
           "X-CSRFToken": self.cookies["csrftoken"],
        }

    def get_all_images_link(self):
        while True:
            res = self.session.post(self.base_url, cookies=self.cookies, headers=self.headers, data=self.body)
            content = res.json()
            posts = content["data"]["xdt_api__v1__feed__user_timeline_graphql_connection"]["edges"]
            for post in posts:
                try:
                    img = post["node"]
                    if img["carousel_media"]:
                        for c in img["carousel_media"]:
                            url = c["image_versions2"]["candidates"][0]["url"]
                            self.all_images_obtained.append(url)
                    else:
                        url = img["image_versions2"]["candidates"][0]["url"]
                    self.all_images_obtained.append(url)
                except Exception as e:
                    print(e)
            if content["data"]["xdt_api__v1__feed__user_timeline_graphql_connection"]["page_info"]["has_next_page"]:
                self.variables["after"] = content["data"]["xdt_api__v1__feed__user_timeline_graphql_connection"]["page_info"]["end_cursor"]
                self.body["variables"] = json.dumps(self.variables)
            else:
                print(f"Found: {len(self.all_images_obtained)}")
                return self.all_images_obtained

    def download_all_images_link(self):
        for x, post in enumerate(self.all_images_obtained):
            path_to_save = f"{self.user_name}/photos"
            if os.path.exists(path_to_save):
                pass
            else:
                os.makedirs(path_to_save)
            with open(os.path.join(f"{path_to_save}", f"{x}.png"), "wb") as file:
                file.write(requests.get(post).content)


