from datetime import date
import json
from pydoc import html
import time
import requests
import os
from urllib.parse import urlparse ### url parser to get the filename and extention from the url 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#  Chrome parameters
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

service = Service("chromedriver.exe")  
driver = webdriver.Chrome(service=service, options=chrome_options)

# download images function
def download_image(i):

    try:
        image = driver.find_element(By.CSS_SELECTOR, 'picture img')

        ## create a folder images if have not
        os.makedirs("images", exist_ok=True)


        img_url = image.get_attribute("src")
        path = urlparse(img_url).path
        ext = os.path.splitext(path)[1]
        if not ext:
            ext = ".jpg"

        response = requests.get(img_url)
        file_name = f"image_{i}{ext}"
        with open(f"images/{f"{date.today()}_{file_name}" }", "wb") as f:
            f.write(response.content)


        data["image"] = f"{date.today()}_{file_name}" 

    except:
        print("Image not found.")
        data["image"] = ""

    
# function to generate data
def generate_data(url):

    driver.get(url)

    wait = WebDriverWait(driver, 15)

    # wait since get data
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

    time.sleep(3)  # let page downloaded

    
    # Title
    element = driver.find_element(
        By.XPATH,
        '//div[contains(@class,"absolute") and contains(@class,"bottom-0") and contains(@class,"flex-col")]')
    
    
        #.text → texte visible seulement
        #get_attribute("innerHTML") → contenu HTML interne
        #get_attribute("outerHTML") → balise complète


    ### .text doesnt work because the title is hidden by CSS, so we use get_attribute("innerHTML") to get the content of the element, which includes the title even if it's not visible.
    h1 = element.find_element(By.XPATH, ".//h1")
    data["title"] = h1.get_attribute("innerHTML").strip()  ## split function to remove extra spaces and newlines


    # description
    try:
        p = element.find_element(By.XPATH, ".//p")
        html = p.get_attribute("innerHTML")
        soup = BeautifulSoup(html, "html.parser") 
        ### car p.text donne valeur vide , on utilise BeautifulSoup pour parser le HTML et extraire le texte 
        ###visible, en supprimant les balises HTML et les espaces inutiles.
        data["description"] = soup.get_text(strip=True)


    except:
        data["description"] = ""



    # Image
    download_image(i)


    # Ingredients

    data["ingredients"] = []

    ### XPath → plus flexible si tu veux filtrer par texte ou structure 
    ### mieux que CSS selector pour les éléments dynamiques ou complexes (taillwind, classes générées, etc.)
    ingredients_div = driver.find_element(
        By.XPATH,
        "//div[contains(@class,'ingredient-list') and contains(@class,'lg:overflow-y-auto')]"
    )

    ingredients = ingredients_div.find_elements(By.TAG_NAME, "li")


    for ing in ingredients:
        text = ing.text.strip()  #.strip() → remove leading/trailing whitespace
        if text :
            data["ingredients"].append(text)





    #timing
    timing_div = driver.find_element(By.ID, "ingredients")
    data["timing"] = timing_div.find_elements(By.TAG_NAME, "span")[2].get_attribute("innerHTML")  #.strip() → remove leading/trailing whitespace


    # Instructions
    data["instructions"] = []
    instructions_div = driver.find_element(By.ID, "steps")
    steps = instructions_div.find_elements(By.XPATH, ".//p")

    for step in steps:
        text = step.text.strip()
        if text and len(text) > 20:
            data["instructions"].append(text)


    ### Owner ID and source if you want to keep them in json file
    data["owner_id"] = "69a21003640c4e467216377b"
    data["source"] = url



    return data
42


### read links.json file
with open("links.json", "r", encoding="utf-8") as f:
    urls = json.load(f)


all_recipes = []

for i, url in enumerate(urls[101:300], start=1):

    recipe_data = {}
    print(f"number {i}     : Scraping {url}")

    data = {}  # important : reset data à chaque loop (data pour stocker les infos de generate data)

    recipe_data = generate_data(url)

    all_recipes.append(recipe_data)

    time.sleep(2)  # éviter blocage



#  JSON save

file_path = "recipes.json"

# 1️⃣ check file
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data_loaded = json.load(f)  # load data
            # Si le fichier existant est un dict, transformer en liste
            if isinstance(data_loaded, dict):
                data_loaded = [data_loaded]
        except json.JSONDecodeError:
            data_loaded = []  

else:
    data_loaded = []

# 2️⃣ add data
data_loaded.append(all_recipes)

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data_loaded, f, ensure_ascii=False, indent=4)

print("✅ JSON file created successfully!")

driver.quit()