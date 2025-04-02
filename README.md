# How this works

### Extract FB session cookies using EditThisCookie Chrome extension
- convert cookies to Netscape and save in txt file (cookies.txt)
### Create & activate the virtual environment in your project folder
- run: `python3 -m venv myenv`
- run: `source myenv/bin/activate`
### Install yt-dlp inside the virtual environment

### Test video download
- run: `yt-dlp --cookies cookies.txt "your_facebook_video_url"`