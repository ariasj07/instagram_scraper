# Instagram Scraper
**Instagram Scraper** is a Python Script to get all the images from a profile
> This project is going to be upgraded and new features will be added soon

### ¿How does it work?
The script directly makes a post to the profile you indicate, if the profile is private, it will only work if **you follow the profile** otherwise, it won't work

### ¿How to use it?
You need to follow a few steps
- Go to Instagram
- Open "Storage" in the web console (Pressing f12 usually)
- Go to Cookies, select the one who refers to instagram.com
- Get the "csrftoken" and the "sessionid"
**Those tokens eventually are going to expire** so, sometimes depending on your browser it'll tell you when are going to expire (usually in the next 1-2 hours)
<img width="1024" height="493" alt="imagen" src="https://github.com/user-attachments/assets/8c92c258-4310-4212-bd7b-af492079153a" />

Once you have them, create an instance of the class, it needs 4 arguments, one is not **mandatory**, since it has a default value
<img width="394" height="243" alt="imagen" src="https://github.com/user-attachments/assets/2dc93593-0453-490d-950f-89ec904f054e" />

As you can see, you need to put these values, and the username to fetch posts

- sessionid: Your cookie
- csrftoken: Your cookie
- user_name: The profile you want to download all the images (if private, you **must** follow it)
- count: The amount of posts you want to get, by default is **12**, you can put as much as you want
If the count is greater than the posted post, there will be **no problem**

Lastly call the method

```python
scraper.save_images()
```
