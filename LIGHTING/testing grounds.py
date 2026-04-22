from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
import re
import openpyxl
import json

ua = UserAgent()

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument(f'user-agent={ua.random}')

# Initialize the Chrome webdriver
driver = webdriver.Chrome(options=chrome_options)

# def get_links(url):
#     try:
#         driver.get(url)
#         time.sleep(2)  # Wait for the page to load

#         soup = BeautifulSoup(driver.page_source, 'html.parser')
        
#         if 'mouser' in url:
#             datasheet_link = get_mouser_links(soup)
#         else:
#             website_link_element = soup.find('a', attrs={'title': 'View product details'})
#             datasheet_url_pattern = re.compile(r'"datasheetUrl":"(.*?)"')

#             datasheet_url_match = datasheet_url_pattern.search(str(soup))
#             datasheet_link = datasheet_url_match.group(1) if datasheet_url_match else None

#         return datasheet_link
#     except Exception as e:
#         print(f"Error while processing {url}: {e}")
#         return None

def get_links(url):
    try:
        driver.get(url)
        time.sleep(2)  # Wait for the page to load

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        if 'mouser' in url:
            datasheet_links = get_mouser_links(soup)
        else:
            website_link_element = soup.find('a', attrs={'title': 'View product details'})
            datasheet_url_pattern = re.compile(r'"datasheetUrl":"(.*?)"')

            datasheet_url_match = datasheet_url_pattern.search(str(soup))
            datasheet_link = datasheet_url_match.group(1) if datasheet_url_match else None
            datasheet_links = [datasheet_link] if datasheet_link else []

        return datasheet_links
    except Exception as e:
        print(f"Error while processing {url}: {e}")
        return []




# def get_mouser_links(soup):
#     try:
#         datasheet_link = None
#         link_elements = soup.find_all('a', class_="datasheet")
#         if link_elements:
#             datasheet_link = link_elements[0]['href']
#     except Exception as e:
#         print(f"Error while processing Mouser page: {e}")
#     return datasheet_link

def get_mouser_links(soup):
    try:
        scripts = soup.find_all('script', {'type': 'text/javascript'})
        datasheet_url = None

        for script in scripts:
            if 'event_datasheet_url' in script.text:
                regex_pattern = r'"event_datasheet_url":"(.*?)"'
                match = re.search(regex_pattern, script.text)

                if match:
                    datasheet_url = match.group(1)
                    break

        return [datasheet_url] if datasheet_url else []
    except Exception as e:
        print(f"Error while processing Mouser link: {e}")
        return []










# Define a list of component URLs
component_urls = [
    'https://www.digikey.com/en/products/detail/alpha-omega-semiconductor-inc/AON6250/4764691?s=N4IgTCBcDaIIIHkByA2MBWADCAugXyA',
    'https://www.mouser.com/ProductDetail/Micro-Commercial-Components-MCC/SK3200B-LTP?qs=SdqRYZZ9IxCsmFkIfPAyXA%3D%3D',
    'https://www.mouser.com/ProductDetail/Micro-Commercial-Components-MCC/BAT46W-TP?qs=O1HRStiETCgnCTHJzjHgzw%3D%3D',
    'https://www.mouser.com/ProductDetail/Vishay-Siliconix/SI4062DY-T1-GE3?qs=c9a7l%2FSwUkK%2FCNXgTevY1A%3D%3D',
    'https://www.mouser.com/ProductDetail/onsemi-Fairchild/FDMC007N08LC?qs=V471yVjZJ9uldG84wopztw%3D%3D',
    'https://www.mouser.com/ProductDetail/onsemi/FDMS3D5N08LC?qs=PqoDHHvF649zqeuxDAua9A%3D%3D',
    'https://www.mouser.com/ProductDetail/ROHM-Semiconductor/RQ5P010SNTL?qs=5aG0NVq1C4zdLJGwiG26VA%3D%3D',
    'https://www.mouser.com/ProductDetail/onsemi-Fairchild/FDD390N15ALZ?qs=i%2FCc05vtxWTgn%2FcOxbx%252Bsg%3D%3D',
    'https://www.mouser.com/ProductDetail/KEMET/A750MV477M1VAAE018?qs=vmHwEFxEFR%252BNRdmMhxgAOA%3D%3D',
    'https://www.mouser.com/ProductDetail/Diodes-Incorporated/DMN15H310SE-13?qs=OVC8WVYZliTTc3Ktk26%252BOQ%3D%3D',
    'https://www.mouser.com/ProductDetail/United-Chemi-Con/EGPD101ELL221MK25H?qs=IYueExuAvkqGe5KVHaGgYg%3D%3D',
    'https://www.mouser.com/ProductDetail/United-Chemi-Con/EKYB630ELL561MK25S?qs=IYueExuAvkpt4K1pjkmWZQ%3D%3D'
]



# Define empty lists to store the links
website_links = []
datasheet_links = []

# for url in component_urls:
#     datasheet_link = get_links(url)
#     if datasheet_link:
#         website_links.append(url)
#         datasheet_links.append(datasheet_link)
#     else:
#         print(f"Skipping {url} due to an error")

for url in component_urls:
    datasheet_links_from_url = get_links(url)
    if datasheet_links_from_url:
        for datasheet_link in datasheet_links_from_url:
            website_links.append(url)
            datasheet_links.append(datasheet_link)
    else:
        print(f"Skipping {url} due to an error")


df = pd.DataFrame({'Website Link': website_links, 'Datasheet Link': datasheet_links})

with pd.ExcelWriter('component_links.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, index=False)

    # Add hyperlinks
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    for i, link in enumerate(datasheet_links, start=2):
        worksheet.cell(row=i, column=2).hyperlink = link

    writer.save()

with pd.ExcelWriter('component_links.xlsx') as writer:
    df.to_excel(writer, index=False)

# Close the webdriver after processing all URLs
driver.quit()