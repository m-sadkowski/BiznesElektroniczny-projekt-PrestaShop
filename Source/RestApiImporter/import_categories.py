import requests
import os
from pathlib import Path
import xml.etree.ElementTree as ET
import re
import json

# --- KONFIGURACJA ---
PS_SHOP_URL = "http://localhost:8080/"
PS_WS_AUTH_KEY = "KLUCZ_API"    # UZUPEŁNIĆ WŁASNYM KODEM API
LANGUAGE_ID = "1"
DEFAULT_ID_PARENT = "2"

ROOT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'ScraperResults')
CATEGORIES_DIR = os.path.join(ROOT_DIR, "categories")
CATEGORY_MAP_PATH = os.path.join(os.path.dirname(__file__), "category_id_map.json")

category_map = {}

def get_blank_xml_schema(resource):
    """Pobiera pusty schemat XML dla danego zasobu."""
    url = f"{PS_SHOP_URL}api/{resource}?schema=blank&ws_key={PS_WS_AUTH_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Błąd pobierania schematu dla {resource}: {e}")
        print(f"Treść odpowiedzi: {getattr(response, 'text', 'Brak treści')}")
        return None

def create_prestashop_category(parent_id, category_name):
    """Tworzy kategorię w PrestaShop i zwraca jej nowe ID."""
    
    # Pobieramy pusty schemat
    blank_xml = get_blank_xml_schema('categories')
    if not blank_xml:
        return None
    
    # Parsowanie XML
    root = ET.fromstring(blank_xml)
    category_node = root.find('category')
    
    for element in category_node:
        if element.tag in ['id', 'position', 'date_add', 'date_upd']:
            category_node.remove(element)

    # UZUPEŁNIENIE DANYCH KATEGORII

    # Nazwa
    name_node = category_node.find('name')
    if name_node is not None:
        lang_node = name_node.find(f"language[@id='{LANGUAGE_ID}']")
        if lang_node is not None:
            lang_node.text = category_name
        else:
            new_lang_node = ET.Element('language', attrib={'id': LANGUAGE_ID})
            new_lang_node.text = category_name
            name_node.append(new_lang_node)
    
    # Aktywna
    active_node = category_node.find('active')
    if active_node is not None:
        active_node.text = '1'
    
    # ID Rodzica
    id_parent_node = category_node.find('id_parent')
    if id_parent_node is not None:
        id_parent_node.text = str(parent_id)
        id_parent_node.set('{http://www.w3.org/1999/xlink}href', f"{PS_SHOP_URL}api/categories/{parent_id}")
    
    # Czy jest to zwykła kategoria (nie jest rootem)
    is_root_category_node = category_node.find('is_root_category')
    if is_root_category_node is not None:
        is_root_category_node.text = '0'

    # ID domyślnego sklepu (zakładamy 1)
    id_shop_default_node = category_node.find('id_shop_default')
    if id_shop_default_node is not None:
        id_shop_default_node.text = '1'

    # Link rewrite (przyjazny adres URL)
    link_rewrite_text = re.sub(r'[^\w\s-]', '', category_name.lower())
    link_rewrite_text = re.sub(r'[-\s]+', '-', link_rewrite_text).strip('-')

    link_rewrite_node = category_node.find('link_rewrite')
    if link_rewrite_node is not None:
        lang_node = link_rewrite_node.find(f"language[@id='{LANGUAGE_ID}']")
        if lang_node is not None:
            lang_node.text = link_rewrite_text
        else:
            new_lang_node = ET.Element('language', attrib={'id': LANGUAGE_ID})
            new_lang_node.text = link_rewrite_text
            link_rewrite_node.append(new_lang_node)

    # Opis i Meta
    for field in ['description', 'meta_title', 'meta_description']:
        field_node = category_node.find(field)
        if field_node is not None:
            lang_node = field_node.find(f"language[@id='{LANGUAGE_ID}']")
            if lang_node is not None:
                if lang_node.text is None:
                    lang_node.text = ""
    

    # Przygotowanie XML do wysłania
    xml_data = ET.tostring(root, encoding='utf-8', xml_declaration=True).decode('utf-8')
    
    # Usuwamy deklarację namespace z <prestashop>
    xml_data = xml_data.replace('ns0:', '', 1) 
    
    # Wysłanie żądania POST
    post_url = f"{PS_SHOP_URL}api/categories?ws_key={PS_WS_AUTH_KEY}"
    headers = {'Content-Type': 'text/xml; charset=utf-8'}
    
    try:
        response = requests.post(post_url, data=xml_data.encode('utf-8'), headers=headers, timeout=20)
        response.raise_for_status()
        
        # Parsowanie odpowiedzi w celu uzyskania ID nowej kategorii
        response_root = ET.fromstring(response.content)
        new_id = response_root.find('category/id').text
        return new_id
        
    except requests.exceptions.HTTPError as err:
        print(f"Błąd HTTP {err.response.status_code} dla kategorii '{category_name}':")
        print(f"Treść odpowiedzi (Error): {err.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Błąd połączenia przy dodawaniu kategorii '{category_name}': {e}")
        return None

def recursive_category_import(current_path: Path, prestashop_parent_id):
    """Rekurencyjnie przechodzi przez foldery, tworzy kategorie i aktualizuje mapowanie ID."""
    
    if not current_path.is_dir() or current_path.name == 'images':
        return

    # Nazwa kategorii to nazwa folderu z ScraperResults/categories
    category_name = current_path.name
    
    # Pomijamy folder główny "categories", który nie jest kategorią do dodania
    if category_name == 'categories':
        print(f"Rozpoczynam import kategorii od: {current_path.resolve()}")
        for child in sorted(current_path.iterdir()):
            if child.is_dir():
                recursive_category_import(child, prestashop_parent_id)
        return

    # DODAWANIE KATEGORII
    
    # Sprawdzamy czy kategoria już istnieje
    if category_name in category_map:
        new_category_id = category_map[category_name]
        print(f"Kategoria '{category_name}' już istnieje w mapie (ID: {new_category_id}). Pomijam tworzenie.")
    else:
        # Dodaj kategorię do PrestaShop
        print(f"⚙️ Dodaję kategorię: '{category_name}' (Parent ID: {prestashop_parent_id})")
        new_category_id = create_prestashop_category(prestashop_parent_id, category_name)
        
        if new_category_id:
            category_map[category_name] = new_category_id
            print(f"Utworzono kategorię '{category_name}' z ID: {new_category_id}")
        else:
            print(f"Nie udało się utworzyć kategorii '{category_name}'. Przerywam import podkategorii.")
            return

    # REKURENCJA DLA PODKATEGORII

    for child in sorted(current_path.iterdir()):
        if child.is_dir():
            recursive_category_import(child, new_category_id)
            
    print(f"Kategorie dla folderu '{category_name}' ukończone.")
    print("---")

def run_category_importer():
    """Główna funkcja uruchamiająca import kategorii."""
    print("--- IMPORT KATEGORII ---")
    
    try:
        initial_parent_id = int(DEFAULT_ID_PARENT)
    except ValueError:
        print(f"BŁĄD: DEFAULT_ID_PARENT ({DEFAULT_ID_PARENT}) musi być liczbą całkowitą.")
        return

    categories_path = Path(CATEGORIES_DIR)
    if not categories_path.exists():
        print(f"BŁĄD: Nie znaleziono katalogu ScraperResults/categories pod ścieżką: {CATEGORIES_DIR}")
        return

    recursive_category_import(categories_path, initial_parent_id)

    # Zapisujemy słownik kategorii w formacie JSON
    print(f"\nZapisuję mapowanie ID kategorii do pliku: {CATEGORY_MAP_PATH}")
    with open(CATEGORY_MAP_PATH, 'w', encoding='utf-8') as f:
        json.dump(category_map, f, ensure_ascii=False, indent=4)
    
    print("\n==================================")
    print("ZAKOŃCZONO IMPORT KATEGORII.")
    print("==================================")

if __name__ == "__main__":
    run_category_importer()