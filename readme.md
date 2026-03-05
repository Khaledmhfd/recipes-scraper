# 🍲 Recipes Scraper

## 📖 Project Description

Recipes Scraper is a Python-based web scraping project designed to extract recipe links and detailed recipe information from a cooking website.

The project works in two stages:

1. **Link Scraping Stage**  
   Collects all recipe URLs and stores them in `links.json`.

2. **Data Scraping Stage**  
   Visits each recipe URL and extracts:
   - Title
   - Description
   - Ingredients
   - instructions
   - Image download
   - Recipe link

All recipes link is saved in structured JSON format (filename "link.json").
All extracted data json is saved in structured JSON format (filename "recipes.json").
All images is saved in Image folder.

## 🏗 Architecture

The project is modular:
- links_scraper.py handles URL extraction   (URL variable change)
- recipe_scraper.py handles data extraction
- JSON is used as a lightweight storage layer

## 🛠 Tech Stack

- Python
- Selenium / BeautifulSoup
- Requests
- JSON
- webdriver (i'm used chrome driver. dont' forget to put it ine same folder)

## ▶ Usage

1. Install dependencies:

#```bash
python -m pip install -r requirements.txt

2. Run links

python scraper/links_scraper.py
python scraper/recipe_scraper.py

## ⚠ Ethical Notice

This project is for educational purposes only and respects responsible scraping practices.