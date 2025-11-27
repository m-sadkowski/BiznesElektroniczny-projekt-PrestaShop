import requests
import os
from pathlib import Path
import xml.etree.ElementTree as ET
import json
import re
from typing import Dict, Any, List
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- KONFIGURACJA ---
PS_SHOP_URL = "https://localhost/"
PS_WS_AUTH_KEY = "KXB36FUS2ZYV13CX4T7CVFJA5BZUKX5U"   # UZUPEŁNIĆ WŁASNYM KLUCZEM API
LANGUAGE_ID = "1"
DEFAULT_CATEGORY_ID = "2"

ROOT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'ScraperResults')
CATEGORIES_DIR = os.path.join(ROOT_DIR, "categories")
IMAGES_DIR = os.path.join(ROOT_DIR, "images")

CATEGORY_MAP_PATH = os.path.join(os.path.dirname(__file__), "category_id_map.json")
CATEGORY_MAP: Dict[str, str] = {}

REFERENCE_ID_MAP: Dict[str, str] = {}

def load_category_map():
    """Ładuje mapowanie nazw kategorii na ID z pliku JSON."""
    global CATEGORY_MAP
    
    if not Path(CATEGORY_MAP_PATH).exists():
        print(f"BŁĄD: Nie znaleziono pliku mapowania: {CATEGORY_MAP_PATH}")
        print("Upewnij się, że importer kategorii został uruchomiony wcześniej.")
        return False
        
    try:
        with open(CATEGORY_MAP_PATH, 'r', encoding='utf-8') as f:
            CATEGORY_MAP = json.load(f)
            print(f"Ładowanie mapowania: {len(CATEGORY_MAP)} kategorii wczytanych.")
            return True
    except Exception as e:
        print(f"BŁĄD: Nie udało się wczytać mapowania kategorii: {e}")
        return False

def get_blank_xml_schema(resource: str) -> str | None:
    """Pobiera pusty schemat XML dla danego zasobu."""
    url = f"{PS_SHOP_URL}api/{resource}?schema=blank&ws_key={PS_WS_AUTH_KEY}"
    try:
        response = requests.get(url, timeout=10, verify=False)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Błąd pobierania schematu dla {resource}: {e}")
        print(f"Treść odpowiedzi: {getattr(response, 'text', 'Brak treści')}")
        return None

def find_category_id(category_name: str) -> str | None:
    """Zwraca ID kategorii na podstawie nazwy, używając mapy."""
    return CATEGORY_MAP.get(category_name, DEFAULT_CATEGORY_ID)

def find_product_by_reference(reference):
    """Wyszukuje ID produktu w Prestashop po numerze referencyjnym."""
    if reference in REFERENCE_ID_MAP:
        return REFERENCE_ID_MAP[reference]
    
    # Wyszukiwanie w Prestashop
    search_url = f"{PS_SHOP_URL}api/products?filter[reference]=[{reference}]&ws_key={PS_WS_AUTH_KEY}"
    try:
        response = requests.get(search_url, timeout=10, verify=False)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        product_node = root.find('products/product')
        
        if product_node is not None:
            product_id = product_node.get('id')
            if product_id:
                REFERENCE_ID_MAP[reference] = product_id
                return product_id  
    except requests.exceptions.RequestException as e:
        print(f"Błąd wyszukiwania produktu po referencji {reference}: {e}")

    return None

def fetch_current_categories(product_id: str) -> List[str]:
    """Pobiera listę ID kategorii, do których należy produkt."""
    categories_url = f"{PS_SHOP_URL}api/products/{product_id}?ws_key={PS_WS_AUTH_KEY}"
    try:
        response = requests.get(categories_url, timeout=10, verify=False)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        categories_node = root.find('product/associations/categories')
        
        current_ids = []
        if categories_node is not None:
            for cat_el in categories_node.findall('category'):
                id_el = cat_el.find('id')
                if id_el is not None:
                    current_ids.append(id_el.text)
        return current_ids
    except Exception as e:
        print(f"Błąd pobierania obecnych kategorii dla ID {product_id}: {e}")
        return []
    
def update_product_categories(product_id: str, current_ids: List[str], new_category_name: str) -> bool:
    """Dodaje nową kategorię do istniejącego produktu (nie usuwając starych)."""
    
    # 1. Znajdź ID nowej kategorii
    new_cat_id = find_category_id(new_category_name)
    if not new_cat_id:
        print(f"   [SKIP] Nie znaleziono ID dla kategorii: {new_category_name}")
        return False

    # 2. Sprawdź czy produkt już w niej jest (żeby nie dublować zapytań)
    if str(new_cat_id) in current_ids:
        print(f"   [OK] Produkt {product_id} już znajduje się w kategorii ID {new_cat_id}")
        return True

    print(f"   [UPDATE] Dodawanie kategorii ID {new_cat_id} do produktu {product_id}...")

    # 3. Pobierz PEŁNY XML produktu (jest wymagany do edycji)
    url = f"{PS_SHOP_URL}api/products/{product_id}?ws_key={PS_WS_AUTH_KEY}"
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        root = ET.fromstring(response.content)
    except Exception as e:
        print(f"   BŁĄD pobierania produktu XML: {e}")
        return False

    # 4. Znajdź węzeł asocjacji kategorii
    product_node = root.find('product')
    
    # PrestaShop API często zwraca pola read-only, które powodują błędy przy zapisie (PUT).
    # Usuwamy je dla bezpieczeństwa:
    for forbidden in ['manufacturer_name', 'quantity', 'quantity_all_versions']:
        node = product_node.find(forbidden)
        if node is not None:
            product_node.remove(node)

    associations_node = product_node.find('associations')
    if associations_node is None:
        associations_node = ET.SubElement(product_node, 'associations')
    
    categories_node = associations_node.find('categories')
    if categories_node is None:
        categories_node = ET.SubElement(associations_node, 'categories')

    # 5. Dodaj nową kategorię do XML
    new_cat_elem = ET.SubElement(categories_node, 'category')
    new_id_elem = ET.SubElement(new_cat_elem, 'id')
    new_id_elem.text = str(new_cat_id)

    # 6. Wyślij zaktualizowany XML (PUT)
    xml_data = ET.tostring(root, encoding='utf-8').decode('utf-8')
    # Usuwamy ewentualne namespace'y, które mogą przeszkadzać
    xml_data = xml_data.replace('ns0:', '').replace(':ns0', '')

    headers = {'Content-Type': 'text/xml; charset=utf-8'}
    try:
        put_response = requests.put(url, data=xml_data.encode('utf-8'), headers=headers, verify=False)
        put_response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as err:
        print(f"   BŁĄD ZAPISU (HTTP {err.response.status_code}): {err.response.text}")
        return False
    except Exception as e:
        print(f"   BŁĄD: {e}")
        return False

def create_product_xml(product_data: Dict[str, Any]) -> str | None:
    """Tworzy XML dla nowego produktu na podstawie danych z JSON."""
    blank_xml = get_blank_xml_schema('products')
    if not blank_xml: return None

    root = ET.fromstring(blank_xml)
    product_node = root.find('product')
    
    fields_to_remove = ['id', 'position_in_category', 'date_add', 'date_upd']
    for element in product_node:
        if element.tag in fields_to_remove:
            product_node.remove(element)

    # UZUPEŁNIANIE DANYCH PRODUKTU

    # Nazwa
    name_node = product_node.find('name')
    if name_node is not None:
        lang_node = name_node.find(f"language[@id='{LANGUAGE_ID}']")
        if lang_node is not None:
            lang_node.text = product_data.get('name', 'Brak nazwy')
        else:
            new_lang_node = ET.Element('language', attrib={'id': LANGUAGE_ID})
            new_lang_node.text = product_data.get('name', 'Brak nazwy')
            name_node.append(new_lang_node)
    
    # Aktywny
    active_node = product_node.find('active')
    if active_node is not None:
        active_node.text = '1'

    # Reference (Indeks)
    reference_node = product_node.find('reference')
    if reference_node is not None:
        reference_node.text = product_data.get('reference', 'N/A')

    # Cena netto
    price_node = product_node.find('price')
    if price_node is not None:
        price = round(product_data.get('price', 0.0) / 1.23, 6)
        price_node.text = str(price)

    # Podatek
    id_tax_rules_group_node = product_node.find('id_tax_rules_group')
    if id_tax_rules_group_node is not None:
        id_tax_rules_group_node.text = '1'

    # Domyślny sklep
    id_shop_default_node = product_node.find('id_shop_default')
    if id_shop_default_node is not None:
        id_shop_default_node.text = '1'

    # Opis produktu (krótki i pełny)
    desc_short_node = product_node.find('description_short')
    if desc_short_node is not None:
        lang_node = desc_short_node.find(f"language[@id='{LANGUAGE_ID}']")
        if lang_node is not None:
            short_html = product_data.get('description_short', '').replace("\n", "<br>")
            lang_node.text = short_html

    desc_full_node = product_node.find('description')
    if desc_full_node is not None:
        lang_node = desc_full_node.find(f"language[@id='{LANGUAGE_ID}']")
        if lang_node is not None:
            full_html = product_data.get('description_full', '').replace("\n", "<br>")
            lang_node.text = full_html

    # Czas realizacji zamówienia
    available_message_cdata = product_data.get('order_processing_time', '')
    delivery_in_stock_node = product_node.find('delivery_in_stock')
    if delivery_in_stock_node is not None:
        lang_node = delivery_in_stock_node.find(f"language[@id='{LANGUAGE_ID}']")
        if lang_node is not None:
            lang_node.text = available_message_cdata
        
    # Link rewrite
    link_rewrite_text = re.sub(r'[^\w\s-]', '', product_data.get('name', '').lower())
    link_rewrite_text = re.sub(r'[-\s]+', '-', link_rewrite_text).strip('-')

    link_rewrite_node = product_node.find('link_rewrite')
    if link_rewrite_node is not None:
        lang_node = link_rewrite_node.find(f"language[@id='{LANGUAGE_ID}']")
        if lang_node is not None:
            lang_node.text = link_rewrite_text
        else:
            new_lang_node = ET.Element('language', attrib={'id': LANGUAGE_ID})
            new_lang_node.text = link_rewrite_text
            link_rewrite_node.append(new_lang_node)
    
    # Kategoria domyślna
    id_category_default_node = product_node.find('id_category_default')
    if id_category_default_node is not None:
        id_category_default_node.text = DEFAULT_CATEGORY_ID

    # Lista wszystkich kategorii (węzeł <associations><categories>)
    categories_node = product_node.find('associations/categories')
    if categories_node is not None:
        categories_node[:] = []
        category_ids = [DEFAULT_CATEGORY_ID, find_category_id(product_data.get('category'))]

        for cat_id in set(category_ids):
            category_el = ET.SubElement(categories_node, 'category', {
                'xlink:href': f"{PS_SHOP_URL}/api/categories/{cat_id}"
            })
            id_el = ET.SubElement(category_el, 'id')
            id_el.text = str(cat_id)

    # Minimalna ilość
    minimal_quantity_node = product_node.find('minimal_quantity')
    if minimal_quantity_node is not None:
        minimal_quantity_node.text = '1'

    # Możliwość zamówienia
    available_for_order_node = product_node.find('available_for_order')
    if available_for_order_node is not None:
        available_for_order_node.text = '1'

    # Dodatkowe informacje o czasie realizacji zamówienia
    additional_delivery_times_node = product_node.find('additional_delivery_times')
    if additional_delivery_times_node is not None:
        additional_delivery_times_node.text = '2'

    # Pokazanie ceny
    show_price_node = product_node.find('show_price')
    if show_price_node is not None:
        show_price_node.text = '1'

    # Stan produktu
    state_node = product_node.find('state')
    if state_node is not None:
        state_node.text = '1'

    # Przygotowanie XML do wysłania
    xml_data = ET.tostring(root, encoding='utf-8', xml_declaration=True).decode('utf-8')
    
    # Usuwamy deklarację namespace z <prestashop>
    xml_data = xml_data.replace('ns0:', '', 1)   
    return xml_data

def update_product_stock(product_id: str, quantity: int) -> bool:
    """Aktualizuje stan magazynowy produktu."""

    # Pobieramy ID stock_availables
    stock_url = f"{PS_SHOP_URL}api/stock_availables/?filter[id_product]={product_id}&ws_key={PS_WS_AUTH_KEY}"
    try:
        response = requests.get(stock_url, timeout=10, verify=False)
        response.raise_for_status()
        stock_root = ET.fromstring(response.content)
    except Exception as e:
        print(f"Błąd pobierania stock_availables dla produktu ID {product_id}: {e}")
        return False
    
    stock_available_node = stock_root.find('stock_availables/stock_available')
    if stock_available_node is None:
        print(f"Nie znaleziono stock_available dla produktu ID {product_id}.")
        return False

    stock_id = stock_available_node.get('id')
        
    # Pobieramy stock_availables do aktualizacji
    stock_url = f"{PS_SHOP_URL}api/stock_availables/{stock_id}?ws_key={PS_WS_AUTH_KEY}"
    try:
        response = requests.get(stock_url, timeout=10, verify=False)
        response.raise_for_status()
        stock_root = ET.fromstring(response.content)
    except Exception as e:
        print(f"Błąd pobierania schematu stock_available ID {stock_id}: {e}")
        return False
        
    stock_available_node = stock_root.find('stock_available')
    
    if stock_available_node is None:
        print(f"Nie znaleziono węzła <stock_available> w schemacie dla ID {stock_id}.")
        return False
    
    # Aktualizujemy ilość
    quantity_node = stock_available_node.find('quantity')
    if quantity_node is not None:
        quantity_node.text = str(quantity)
    
    # Wysyłamy żądanie PUT
    xml_data = ET.tostring(stock_root, encoding='utf-8', xml_declaration=True).decode('utf-8')
    xml_data = xml_data.replace('ns0:', '', 1) 
    
    headers = {'Content-Type': 'text/xml; charset=utf-8'}
    
    try:
        response = requests.put(stock_url, data=xml_data.encode('utf-8'), headers=headers, timeout=20, verify=False)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Błąd aktualizacji stock_available ID {stock_id} (Qty: {quantity}): {e}")
        return False

def upload_product_images(product_id: str, image_files: List[str]) -> bool:
    """Wysyła pliki zdjęć do nowo utworzonego produktu."""

    if not image_files:
        return True

    success = True
    for image_filename in image_files:
        filepath = os.path.join(IMAGES_DIR, image_filename)
        if not os.path.exists(filepath):
            print(f"Plik zdjęcia nie istnieje: {filepath}")
            continue

        image_url = f"{PS_SHOP_URL}api/images/products/{product_id}?ws_key={PS_WS_AUTH_KEY}"
        
        try:
            with open(filepath, 'rb') as image_file:
                files = {'image': (image_filename, image_file)}
                response = requests.post(image_url, files=files, timeout=30, verify=False)
                response.raise_for_status()
                print(f"Dodano zdjęcie: {image_filename}")

        except requests.exceptions.RequestException as e:
            print(f"Błąd przesyłania zdjęcia {image_filename} dla produktu ID {product_id}: {e}")
            success = False         
    return success

def process_product_import(product_data: Dict[str, Any]):
    """Główna logika importu pojedynczego produktu."""
    
    reference = product_data.get('reference')
    product_name = product_data.get('name', 'N/A')

    existing_product_id = find_product_by_reference(reference)
    if existing_product_id:
        print(f"Duplikat (Ref: {reference}). Aktualizuję kategorię produktu ID: {existing_product_id}")
        
        # Pobieramy obecne kategorie
        current_categories = fetch_current_categories(existing_product_id)
        
        # Aktualizujemy (dodajemy) nową kategorię
        success = update_product_categories(existing_product_id, current_categories, product_data.get('category'))
        
        if success:
            print(f"Kategoria '{product_data.get('category')}' pomyślnie dodana.")
        else:
            print(f"Błąd dodawania kategorii.")
        return
    
    # Tworzymy XML produktu
    product_xml = create_product_xml(product_data)
    if not product_xml:
        print(f"Nie udało się wygenerować XML dla produktu: {product_name}")
        return
        
    # Wysłanie żądania POST
    post_url = f"{PS_SHOP_URL}api/products?ws_key={PS_WS_AUTH_KEY}"
    headers = {'Content-Type': 'text/xml; charset=utf-8'}
    
    try:
        response = requests.post(post_url, data=product_xml.encode('utf-8'), headers=headers, timeout=20, verify=False)
        response.raise_for_status()
        
        # Parsowanie odpowiedzi w celu uzyskania ID nowo utworzonego produktu
        response_root = ET.fromstring(response.content)
        new_product_id = response_root.find('product/id').text
        REFERENCE_ID_MAP[reference] = new_product_id
        print(f"Utworzono produkt '{product_name}' z ID: {new_product_id}")
        
    except requests.exceptions.HTTPError as err:
        print(f"Błąd HTTP {err.response.status_code} przy tworzeniu produktu '{product_name}':")
        print(f"Treść odpowiedzi (Error): {err.response.text}")
        return
    except requests.exceptions.RequestException as e:
        print(f"Błąd połączenia przy dodawaniu produktu '{product_name}': {e}")
        return
        
    # Aktualizacja stanu magazynowego
    quantity = product_data.get('quantity', 0)
    if update_product_stock(new_product_id, quantity):
        print(f"Zaktualizowano ilość: {quantity}")
        
    # Dodanie zdjęć
    image_files = product_data.get('images', [])
    upload_product_images(new_product_id, image_files)

def recursive_product_import(current_path: Path):
    """Rekurencyjnie przechodzi przez foldery w poszukiwaniu products.json i importuje produkty."""

    json_path = current_path / "products.json"
    
    if json_path.exists():
        print(f"\n📁 Kategoria: {current_path.name}")
        
        try:
            # Wczytujemy plik JSON
            with open(json_path, 'r', encoding='utf-8') as f:
                raw_json_text = f.read()
            
            products_list = json.loads(raw_json_text) 

            print(f"Znaleziono {len(products_list)} produktów do zaimportowania.")
            
            for i, product in enumerate(products_list):
                print(f"[{i+1}/{len(products_list)}] Importuję produkt: {product.get('name')}")
                process_product_import(product)
                
        except json.JSONDecodeError as e:
            print(f"BŁĄD JSON w pliku {json_path.name} (Linia: {e.lineno}, Kolumna: {e.colno}): {e.msg}")
        except Exception as e:
            print(f"Ogólny błąd przetwarzania pliku {json_path}: {e}")

    for child in sorted(current_path.iterdir()):
        if child.is_dir():
            recursive_product_import(child)

    print(f"Produkty dla folderu '{current_path.name}' ukończone.")
    print("---")

def run_product_importer():
    """Główna funkcja uruchamiająca import produktów."""
    print("--- IMPORT PRODUKTÓW ---")
    
    if not load_category_map():
        return

    categories_path = Path(CATEGORIES_DIR)
    if not categories_path.exists():
        print(f"BŁĄD: Nie znaleziono katalogu ScraperResults/categories pod ścieżką: {CATEGORIES_DIR}")
        return
    
    recursive_product_import(categories_path)
    
    print("\n==================================")
    print("ZAKOŃCZONO IMPORT PRODUKTÓW.")
    print("==================================")

if __name__ == "__main__":
    run_product_importer()