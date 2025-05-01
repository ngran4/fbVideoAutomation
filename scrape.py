import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os

cookies_path = os.path.expanduser("~/secure_folder/cookies.txt")

# set up webdriver
driver_path = "./chromedriver"
service = Service(driver_path) 
driver = webdriver.Chrome(service=service)

# Load the Facebook login page
driver.get("https://www.facebook.com")

# Load cookies from the exported file
with open(cookies_path, "r") as f:
    cookies = json.load(f)
    for cookie in cookies:
        # Fix invalid "sameSite" values
        if "sameSite" in cookie:
            if cookie["sameSite"] not in ["Strict", "Lax", "None"]:
                cookie["sameSite"] = "Lax"  # Default to "Lax" if invalid

        # Add the cookie to the browser
        driver.add_cookie(cookie)

# Refresh the page to apply cookies
driver.refresh()

# set url of fb page
url = "https://www.facebook.com/groups/133404231436028/media/videos"

# load page, wait for load 
driver.get(url)

try:
  WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.xrvj5dj.x5yr21d.xh8yej3"))
  )
  print("Page content loaded successfully")
except Exception as e:
  print(f"error waiting for page content: {e}")
  driver.quit()
  exit()


# # Scroll down to load dynamic content
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# time.sleep(5)  # Wait for additional content to load

# # get page source after JS has executed
# html = driver.page_source

# # parse the html with BeautifulSoup
# soup = BeautifulSoup(html, "html.parser")

# # Find all divs with the specific class containing <a> tags
# divs = soup.find_all("div", class_="xrvj5dj x5yr21d xh8yej3")

# # find <a> tag within the div and extract and print the href attribute 
# for div in divs:
#   a_tag = div.find("a", href=True)
#   if a_tag:
#     video_url = a_tag['href']
#     print(f"Video URL found: {video_url}")

# scroll down to load all videos
video_urls = set() # use a set to avoid duplicates!!
scroll_pause_time = 5 # time to wait after each scroll
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
  # scroll down to the bottom of the page
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  time.sleep(scroll_pause_time)

  # get the page souce and pase it with BeautifulSoup
  html = driver.page_source
  soup = BeautifulSoup(html, "html.parser")

  # find all video urls on the page
  divs = soup.find_all("div", class_="xrvj5dj x5yr21d xh8yej3")
  for div in divs:
    a_tag = div.find("a", href=True)
    if a_tag:
       video_url = a_tag['href']
       video_urls.add(video_url) # add to the set

  #check if we hit end of page
  new_height = driver.execute_script("return document.body.scrollHeight")
  if new_height == last_height:
     break
  last_height = new_height

print("End of page reached")
  
      

# close browser
driver.quit()
