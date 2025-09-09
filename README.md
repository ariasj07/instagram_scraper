# Instagram Scraper
**Instagram Scraper** is a Python Script to get all the images from a profile
> This project is going to be upgraded and new features will be added soon

### ¿How does it work?
The script directly makes a POST to the API, to the profile you indicate, if the profile is private, it will only work if **you follow the profile** otherwise, it won't work

### ¿How to use it?
You need to follow a few steps
- Go to Instagram
- Open "Storage" in the web console (Usually by Pressing F12)
- Go to the Cookies Section, select the one that refers to instagram.com
- Get the "csrftoken" and the "sessionid"
**Those tokens are eventually going to expire** so, sometimes depending on your browser, and activity it'll tell you when they are going to expire. (Usually in about 1-2 hours)
<img width="1024" height="493" alt="imagen" src="https://github.com/user-attachments/assets/8c92c258-4310-4212-bd7b-af492079153a" />

Once you have them, create an instance of the class, it needs 3 arguments 

<img width="394" height="243" alt="imagen" src="https://github.com/user-attachments/assets/2dc93593-0453-490d-950f-89ec904f054e" />

> ```count``` parameter it's not longer required
As you can see, you need to put these values, and the username to fetch posts

- sessionid: Your cookie
- csrftoken: Your cookie
- user_name: The profile you want to download all the images (if private, you **must** follow it)


Lastly call the method

```python
scraper.get_all_images() # Return an array with al the images link 
scraper.download_all_images() # it'll create a folder with the username and whithin, all the photos
```

And it will save all the photos, if a post is a carrusel of photos, all the photos are going to be downloaded also.

Things to consider:

Currently, I'm working in the option to also download the videos, since it doesn't have it yet, when there's a video, is going to save the thumbnail of the video
