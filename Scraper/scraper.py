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

# LIMIT PRODUKTÓW
TARGET_PRODUCT_COUNT = 696969 

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

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

def download_image(img_url, product_ref):
    """Pobiera zdjęcie i zapisuje je lokalnie"""
    if not img_url or not img_url.startswith('http'):
        return ""
    
    try:
        filename = f"{product_ref}_{random.randint(1000,9999)}.jpg"
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

    def traverse_list(ul_element, current_path):
        for li in ul_element.find_all('li', recursive=False):
            a_tag = li.find('a', recursive=False)
            if not a_tag: continue
            
            name = clean_text(a_tag.text)
            href = a_tag.get('href')
            
            if "2-glowna" in href:
                nested_ul = li.find('ul', recursive=False)
                if nested_ul:
                    traverse_list(nested_ul, current_path)
                continue

            safe_name = re.sub(r'[\\/*?:"<>|]', "", name).strip()
            new_path = os.path.join(current_path, safe_name)
            
            categories_to_scan.append({
                'name': name,
                'url': href,
                'folder_path': new_path
            })
            
            nested_ul = li.find('ul', recursive=False)
            if nested_ul:
                traverse_list(nested_ul, new_path)

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
        
        # 3. Cena
        price_tag = soup.select_one('.current-price-value')
        price = float(price_tag['content']) if price_tag else 0.0
        
        # 4. Opis
        desc_div = soup.select_one('.product-description')
        description = ""
        if desc_div:
            for br in desc_div.find_all("br"):
                br.replace_with("\n")
            for p in desc_div.find_all("p"):
                p.insert_after("\n")
            
            raw_text = desc_div.get_text()
            
            lines = [line.strip() for line in raw_text.split('\n')]
            description = "\n".join([l for l in lines if l])

        # 5. Zdjęcia
        images = []
        cover_img = soup.select_one('.product-cover img')
        if cover_img:
            src = cover_img.get('data-image-large-src') or cover_img.get('src')
            images.append(src)
            
        thumbs = soup.select('.product-images li img')
        for thumb in thumbs:
            src = thumb.get('data-image-large-src') or thumb.get('data-src')
            if src and src not in images:
                images.append(src)
                
        final_images_urls = images[:2]
        while len(final_images_urls) < 2 and len(final_images_urls) > 0:
            final_images_urls.append(final_images_urls[0]) 
            
        local_images = []
        for i, img_url in enumerate(final_images_urls):
            filename = download_image(img_url, f"{reference}_{i}")
            if filename:
                local_images.append(filename)

        # 6. Atrybuty
        attributes = {}
        dts = soup.select('.data-sheet dt')
        dds = soup.select('.data-sheet dd')
        for dt, dd in zip(dts, dds):
            attributes[clean_text(dt.text)] = clean_text(dd.text)

        # 7. Ilość
        quantity = random.randint(0, 10)

        # 8. Dostępność
        is_active = 0 if random.random() < 0.15 else 1

        return {
            "name": name,
            "category": category_name,
            "reference": reference,
            "price": price,
            "description": description,
            "attributes": attributes,
            "images": local_images,
            "quantity": quantity,
            "active": is_active
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
    
    random.shuffle(categories_structure)
    
    products_counter = 0
    
    for cat in categories_structure:
        if products_counter >= TARGET_PRODUCT_COUNT:
            break
            
        if not os.path.exists(cat['folder_path']):
            os.makedirs(cat['folder_path'])
            gitkeep_path = os.path.join(cat['folder_path'], '.gitkeep')
            with open(gitkeep_path, 'w', encoding='utf-8') as f:
                pass
            
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
                    products_counter += 1
                    status = "AKTYWNY" if product_data['active'] == 1 else "NIEAKTYWNY"
                    print(f"✅ [{products_counter}] {product_data['name'][:30]}... (Stan: {product_data['quantity']}, {status})")
                
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