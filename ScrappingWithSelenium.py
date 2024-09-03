from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
from urllib.parse import urljoin

# Path to your ChromeDriver executable
path = r"C:\Users\Dell\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service = Service(path)

# Start a new browser session
driver = webdriver.Chrome(service=service)

# URL of the page containing the image
url = r"https://www.jstor.org/stable/community.13895027?searchText=egypt&searchUri=%2Faction%2FdoBasicSearch%3FQuery%3Degypt%26image_search_referrer%3Dhomepage%26so%3Drel%26searchkey%3D1725199797186%26doi%3D10.2307%252Fcommunity.13895027&ab_segments=0%2Fbasic_image_search%2Fcontrol&refreqid=fastly-default%3A4bb7e01f7a0540169c5ff17dc80295db&searchkey=1725199797186"
driver.get(url)

# Locate the image element by its relative src path
image_element = driver.find_element(By.XPATH, "//img[contains(@src, '/api/cached/thumbnails/')]")

# Get the relative src of the image
relative_src = image_element.get_attribute("src")

# Construct the absolute URL for the image
absolute_url = urljoin(driver.current_url, relative_src)

# Download the image with headers to mimic a browser request
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
response = requests.get(absolute_url, headers=headers)

# Check if the response is OK and content type is an image
if response.status_code == 200 and 'image' in response.headers['Content-Type']:
    # Save the image to your local machine
    with open("image.jpg", "wb") as file:
        file.write(response.content)
    print("Image downloaded successfully.")
else:
    print("Failed to download image. Status Code:", response.status_code)
    print("Content-Type:", response.headers.get('Content-Type'))

# Close the browser
driver.quit()
