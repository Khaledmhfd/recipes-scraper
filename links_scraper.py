import json
import time
## download chromedriver from https://chromedriver.chromium.org/downloads and put it in the same folder as this script
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#  URL search page
url = "https://cookpad.com/fr/recherche/algerienne"

#  Chrome parameters
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

service = Service("chromedriver.exe") 
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(url)

wait = WebDriverWait(driver, 15)

time.sleep(3) 


## ul list containing recipes
list_recipes = wait.until(EC.presence_of_element_located((By.XPATH, "//ul[contains(@id,'search-recipes-list')]"))) ## attendre que la liste des recettes soit présente


target_count = 1500
recipes_count = 400
scroll_pause = 2  # temps d'attente entre les scrolls

while True:
    # récupérer tous les li actuellement chargés
    recipes = list_recipes.find_elements(By.TAG_NAME, "li")
    
    if len(recipes) >= target_count:
        break  # on a assez de recettes
    
    #print(driver.execute_script("return arguments[0].scrollHeight > arguments[0].clientHeight;", list_recipes))
    # >>>> return boolean to know if scrolable (ul)

    #driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", list_recipes)
        # défiler jusqu'en bas du conteneur (list_recipes)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # attendre que les nouvelles recettes chargent
    time.sleep(scroll_pause)



recipes_links = []
def get_recipe_links():
    for recipe in recipes:

        try:
            link_elt = recipe.find_element(
                By.XPATH,'.//a[@class="block-link__main"]')
            #le . au début de .//a[...] → ça signifie “chercher dans ce <li> uniquement”
            if link_elt:
                href = link_elt.get_attribute("href")
                recipes_links.append(href)
        except:
            #print('result not found')  # au cas où le <a> n'apparaît pas
            pass

    return len(recipes_links)


print(f"Found {get_recipe_links()} recipe links.")

if len(recipes_links) < recipes_count:
    print(f"Only found {len(recipes_links)} links, trying to scroll more...")
else :
    with open('links.json', "w", encoding="utf-8") as f:
        json.dump(recipes_links, f, ensure_ascii=False, indent=4)
        print("✅ JSON file created successfully!")

driver.quit()