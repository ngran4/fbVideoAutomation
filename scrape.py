import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# set up webdriver
driver_path = "./chromedriver"
service = Service(driver_path) 
driver = webdriver.Chrome(service=service)

# Load the Facebook login page
driver.get("https://www.facebook.com")

# Load cookies from the exported file
with open("cookies.txt", "r") as f:
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


# Scroll down to load dynamic content
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)  # Wait for additional content to load

# get page source after JS has executed
html = driver.page_source

# parse the html with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Find all divs with the specific class containing <a> tags
divs = soup.find_all("div", class_="xrvj5dj x5yr21d xh8yej3")

# find <a> tag within the div and extract and print the href attribute 
for div in divs:
  a_tag = div.find("a", href=True)
  if a_tag:
    video_url = a_tag['href']
    print(f"Video URL found: {video_url}")

# close browser
driver.quit()







# import requests
# from bs4 import BeautifulSoup

# # set url of fb page
# url = "https://www.facebook.com/groups/133404231436028/media/videos"

# # load cookies from text file
# cookies = {}
# with open("cookies.txt", "r") as f:
#     for line in f:
#         if line.startswith(".facebook.com"):
#             parts = line.strip().split("\t")
#             if len(parts) >= 7:
#                 name, value = parts[5], parts[6]
#                 cookies[name] = value

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
# }
# res = requests.get(url, headers=headers, cookies=cookies)

# if res.status_code == 200:
#     # if response is successful, parse the html
#     soup = BeautifulSoup(res.text, "html.parser")

#     # # Print the HTML content for debugging
#     # print(soup.prettify()[:15000]) # debugging

#     # Find all <div> tags with specific classes
#     divs = soup.find_all("div", class_="xrvj5dj x5yr21d xh8yej3")

#     for div in divs:
#         # Find <a> tag within the div
#         a_tag = div.find("a", href=True)
#         if a_tag:
#             # Extract the href attribute + print
#             video_url = a_tag('href')
#             print(f"video url found: {video_url}")


#     # limit the number of videos to download
#     max_videos = 5
#     count = 0



#     # find all <a> tags that might contain video URLs
#     video_urls = soup.find_all("a", href=True)
#     for video_url in video_urls:
#         href = video_url['href']
#         if '/videos/' in href:
#             if count >= max_videos:
#                 break
#             print(f"Video URL found: {href}")
#             count += 1

#     if count == 0:
#         print("No video URLs found on page")

# else:
#     print(f"Failed to fetch page. Status code: {res.status_code}")