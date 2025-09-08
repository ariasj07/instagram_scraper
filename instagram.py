import os.path
import requests
import json




class InstagramScraper:
    def __init__(self, sessionid: str, csrftoken: str, user_name: str, count: int = 12):
        self.doc_id = "32435654999367421"
        self.session = requests.Session()
        self.base_url = "https://www.instagram.com/graphql/query"
        self.cookies = {
            "sessionid": sessionid,
            "csrftoken": csrftoken
        }
        self.user_name = user_name
        self.count = count
        self.variables = {
            "data": {
                "count": self.count,
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

    def save_images(self):
        res = self.session.post(self.base_url, cookies=self.cookies, headers=self.headers, data=self.body)
        content = res.json()
        posts = content["data"]["xdt_api__v1__feed__user_timeline_graphql_connection"]["edges"]
        gotten_posts = []
        for post in posts:
            imgs = post["node"]["carousel_media"]
            for img in imgs:
                url = img["image_versions2"]["candidates"][0]["url"]
                gotten_posts.append(url)
        print(gotten_posts)
        for x, post in enumerate(gotten_posts):
            path_to_save = f"{self.user_name}/photos"
            if os.path.exists(path_to_save):
                pass
            else:
                os.makedirs(path_to_save)
            with open(os.path.join(f"{path_to_save}", f"{x}.png"), "wb") as file:
                file.write(requests.get(post).content)





