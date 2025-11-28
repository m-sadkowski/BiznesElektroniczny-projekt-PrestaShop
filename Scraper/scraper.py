import requests
from bs4 import BeautifulSoup
import json
import os
import random
import time
import re

# --- KONFIGURACJA ---
BASE_URL = "https://bikepart.pl"
SITEMAP_URL = "https://bikepart.pl/pl/mapa-strony"

ROOT_DIR = os.path.join(os.path.dirname(__file__), '..', 'ScraperResults')
IMAGES_DIR = os.path.join(ROOT_DIR, "images")
CATEGORIES_DIR = os.path.join(ROOT_DIR, "categories")

# DOCELOWA ILOŚĆ SCRAPOWANYCH PRODUKTÓW
TARGET_PRODUCT_COUNT = 696969 

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Aby uniknąć powtarzania zdjęć tych samych produktów (o tym samym reference)
PROCESSED_REFERENCES = set()
IMAGE_MAP = {}

def setup_directories():
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
    if not os.path.exists(CATEGORIES_DIR):
        os.makedirs(CATEGORIES_DIR)

def get_soup(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Błąd połączenia z {url}: {e}")
    return None

def clean_text(text):
    """Usuwa nadmiarowe spacje, entery i śmieci - DO NAZW I ATRYBUTÓW"""
    if not text: return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def download_image(img_url, product_ref, index):
    """Pobiera zdjęcie i zapisuje je lokalnie"""
    if not img_url or not img_url.startswith('http'):
        return ""
    
    try:
        filename = f"{product_ref}_{index}.jpg"
        filename = re.sub(r'[\\/*?:"<>|]', "", filename)
        filepath = os.path.join(IMAGES_DIR, filename)
        
        if os.path.exists(filepath):
            return filename

        img_data = requests.get(img_url, headers=HEADERS, timeout=10).content
        with open(filepath, 'wb') as handler:
            handler.write(img_data)
            
        return filename 
    except Exception as e:
        print(f"Błąd pobierania zdjęcia: {e}")
        return ""

def parse_sitemap_structure(soup):
    """Rekurencyjnie buduje strukturę kategorii."""
    categories_to_scan = []
    
    block_links = soup.select('.sitemap .block-links')
    target_ul = None
    
    for block in block_links:
        if 'Kategorie' in block.select_one('.block-title').text:
            target_ul = block.select_one('ul')
            break
            
    if not target_ul:
        print("Nie znaleziono drzewa kategorii w mapie strony.")
        return []

    def traverse_list(ul_element, current_path, is_excluded=False):
        for li in ul_element.find_all('li', recursive=False):
            a_tag = li.find('a', recursive=False)
            if not a_tag: continue
            
            name = clean_text(a_tag.text)
            href = a_tag.get('href')

            is_current_excluded = is_excluded or 'HondaImport' in name
            
            if "2-glowna" in href:
                nested_ul = li.find('ul', recursive=False)
                if nested_ul:
                    traverse_list(nested_ul, current_path, is_current_excluded)
                continue

            safe_name = re.sub(r'[\\/*?:"<>|]', "", name).strip()
            new_path = os.path.join(current_path, safe_name)

            if not os.path.exists(new_path):
                os.makedirs(new_path)
                gitkeep_path = os.path.join(new_path, '.gitkeep')
                with open(gitkeep_path, 'w', encoding='utf-8') as f:
                    pass

            nested_ul = li.find('ul', recursive=False)
            if nested_ul:
                traverse_list(nested_ul, new_path)
            
            if not nested_ul:
                if not is_current_excluded:
                    categories_to_scan.append({
                        'name': name,
                        'url': href,
                        'folder_path': new_path
                    })
            

    traverse_list(target_ul, CATEGORIES_DIR)
    return categories_to_scan

def scrape_product(url, category_name):
    soup = get_soup(url)
    if not soup: return None

    try:
        # 1. Nazwa
        name_tag = soup.select_one('h1.page-title span') or soup.select_one('h1.page-title')
        name = clean_text(name_tag.text) if name_tag else "Nieznany produkt"
        
        # 2. Referencja
        ref_tag = soup.select_one('.product-reference span')
        reference = clean_text(ref_tag.text) if ref_tag else f"GEN-{random.randint(10000,99999)}"

        # OBSŁUGA PRODUKTÓW PRZYPISANYCH DO WIELU KATEGORII
        is_duplicate = reference in PROCESSED_REFERENCES
        if is_duplicate:
            local_images = IMAGE_MAP.get(reference, [])
        else:
            local_images = []
        
        # 3. Cena
        price_tag = soup.select_one('.current-price-value')
        price = float(price_tag['content']) if price_tag else 0.0
        
        # 4. Opis krótki i długi
        desc_short_div = soup.select_one('div[id^="product-description-short-"]')
        description_short = ""
        if desc_short_div:
            description_short = desc_short_div.get_text('\n', strip=True)
            description_short = '\n'.join([line.strip() for line in description_short.split('\n') if line.strip()])

        desc_full_div = soup.select_one('.tab-pane#description .product-description .rte-content')
        description_full = ""
        if desc_full_div:
            for tag in desc_full_div.find_all(['b', 'strong']):
                tag.replace_with(tag.get_text())
                
            description_full = desc_full_div.get_text('\n', strip=True)
            description_full = '\n'.join([line.strip() for line in description_full.split('\n') if line.strip()])

        # 5. Zdjęcia
        if not is_duplicate or not IMAGE_MAP.get(reference):
            images_urls = []
            cover_img = soup.select_one('.product-cover img')
            if cover_img:

                src = cover_img.get('data-image-large-src') or cover_img.get('src')
                images_urls.append(src)
                
            thumbs = soup.select('.product-images li img')
            for thumb in thumbs:
                src = thumb.get('data-image-large-src') or thumb.get('data-src')
                if src and src not in images_urls:
                    images_urls.append(src)
            
            final_images_urls = images_urls[:2]
            
            while len(final_images_urls) < 2 and len(final_images_urls) > 0:
                final_images_urls.append(final_images_urls[0]) 
            
            local_images = []
            for i, img_url in enumerate(final_images_urls):
                filename = download_image(img_url, reference, i + 1)
                if filename:
                    local_images.append(filename)
            
            IMAGE_MAP[reference] = local_images
        else:
            local_images = IMAGE_MAP[reference]

        # 6. Atrybuty
        attributes = {}
        dts = soup.select('.data-sheet dt')
        dds = soup.select('.data-sheet dd')
        for dt, dd in zip(dts, dds):
            attributes[clean_text(dt.text)] = clean_text(dd.text)

        # 7. Ilość
        quantity = random.randint(0, 10)

        # 8. Czas realizacji zamówienia
        availability_tag = soup.select_one('#product-availability')
        availability_message = clean_text(availability_tag.text) if availability_tag else "Dostępny"

        return {
            "name": name,
            "category": category_name,
            "reference": reference,
            "price": price,
            "description_short": description_short,
            "description_full": description_full,
            "attributes": attributes,
            "order_processing_time": availability_message,
            "images": local_images,
            "quantity": quantity
        }

    except Exception as e:
        print(f"Błąd parsowania produktu {url}: {e}")
        return None

def run():
    setup_directories()
    
    print("Skanuję mapę strony i buduję strukturę folderów...")
    soup = get_soup(SITEMAP_URL)
    if not soup: return

    categories_structure = parse_sitemap_structure(soup)
    print(f"Znaleziono {len(categories_structure)} podkategorii.")
    
    products_counter = 0
    
    for cat in categories_structure:
        if products_counter >= TARGET_PRODUCT_COUNT:
            break

        print(f"Kategoria: {cat['name']}")
        
        category_products = []
        page = 1
        
        while True:
            list_url = f"{cat['url']}?page={page}"
            cat_soup = get_soup(list_url)
            if not cat_soup: break
            
            links = cat_soup.select('.product-miniature .product-title a')
            if not links: break 
            
            print(f"Strona {page}: znaleziono {len(links)} produktów...")
            
            for link in links:
                if products_counter >= TARGET_PRODUCT_COUNT:
                    break
                    
                href = link.get('href')
                product_data = scrape_product(href, cat['name'])
                
                if product_data:
                    category_products.append(product_data)
                    if product_data['reference'] not in PROCESSED_REFERENCES:
                        products_counter += 1
                        PROCESSED_REFERENCES.add(product_data['reference'])

                    print(f"✅ [{products_counter}] {product_data['name'][:30]}... (Stan: {product_data['quantity']})")
                
                # time.sleep(0.1)

            if not cat_soup.select_one('a.next'):
                break
            page += 1
            
            if products_counter >= TARGET_PRODUCT_COUNT:
                break
        
        if category_products:
            json_path = os.path.join(cat['folder_path'], "products.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(category_products, f, ensure_ascii=False, indent=4)

    print(f"\nZakończono! Pobrano {products_counter} produktów.")
    print(f"Wyniki w folderze: {ROOT_DIR}")

if __name__ == "__main__":
    run()