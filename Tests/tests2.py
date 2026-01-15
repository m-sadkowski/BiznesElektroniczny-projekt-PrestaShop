import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker

# --- KONFIGURACJA ---
URL = "https://localhost:19777/"
faker = Faker("pl_PL")

chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()
wait = WebDriverWait(driver, 15)

# --- FUNKCJE POMOCNICZE ---

def safe_click(element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", element)

def clear_and_type(element, text):
    safe_click(element)
    element.send_keys(Keys.CONTROL + "a")
    element.send_keys(Keys.BACK_SPACE)
    element.send_keys(str(text))

def add_unique_products(category_url, count):
    print(f"\n--- Kategoria: {category_url} (Cel: {count} różnych) ---")
    driver.get(category_url)
    
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-miniature")))
        # Pobieramy wszystkie linki z kategorii
        products = driver.find_elements(By.CSS_SELECTOR, ".product-miniature .thumbnail.product-thumbnail")
        links = list(set([p.get_attribute("href") for p in products])) # Unikalne linki
        random.shuffle(links) # Mieszamy kolejność
    except:
        print("Błąd pobierania listy produktów.")
        return 0

    added = 0
    for link in links:
        if added >= count: break
        try:
            driver.get(link)
            add_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".add-to-cart")))
            
            if not add_btn.is_enabled():
                print("Produkt niedostępny.")
                continue

            # Losowa ilość 1-3
            qty_input = wait.until(EC.element_to_be_clickable((By.ID, "quantity_wanted")))
            clear_and_type(qty_input, random.randint(1, 3))
            
            safe_click(add_btn)
            time.sleep(1) # Czekamy na przetworzenie
            
            print(f" -> Dodano produkt: {link}")
            added += 1
        except Exception as e:
            print(f"Błąd dodawania: {e}")
            continue
            
    return added

# --- GŁÓWNY TEST ---

try:
    start_time = time.time()
    print("=== START TESTU ===")

    print("\n1. Dodanie do koszyka 10 produktów (w różnych ilościach) z dwóch różnych kategorii")
    cat1 = URL + "index.php?id_category=8&controller=category" 
    cat2 = URL + "index.php?id_category=362&controller=category"

    add_unique_products(cat1, 5)
    add_unique_products(cat2, 5)

    print("\nPOMYŚLNIE DODANO")
    print("\n2. Wyszukanie produktu po nazwie...")
    driver.get(URL)
    
    search_input = wait.until(EC.element_to_be_clickable((By.NAME, "s")))
    clear_and_type(search_input, "Honda") 
    search_input.send_keys(Keys.ENTER)
    
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-miniature")))
    
    results_elements = driver.find_elements(By.CSS_SELECTOR, ".product-miniature .thumbnail.product-thumbnail")
    
    links_list = [elem.get_attribute("href") for elem in results_elements]
    
    if not links_list:
        raise Exception("Brak wyników wyszukiwania!")

    random_url = random.choice(links_list)
    print(f"Wybrano produkt: {random_url}")
    driver.get(random_url)
    
    add_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".add-to-cart")))
    safe_click(add_btn)
    time.sleep(2)
    
    print("\nPOMYŚLNIE DODANO")

    print("\n3. Usunięcie z koszyka 3 produktów")
    driver.get(URL + "index.php?controller=cart")
    for i in range(3):
        try:
            delete_buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "remove-from-cart")))
            if delete_buttons:
                safe_click(delete_buttons[0])
                print(f"Usunięto {i+1}")
                time.sleep(2.5)
            else:
                break
        except:
            break

    print("\nPOMYŚLNIE USUNIĘTO")
    print("\n4. Wykonanie zamówienia zawartości koszyka")
    driver.get(URL + "index.php?controller=order")
    
    try:
        wait.until(EC.visibility_of_element_located((By.NAME, "firstname")))
        try:
            gender_radio = driver.find_element(By.CSS_SELECTOR, "input[name='id_gender'][value='1']")
            driver.execute_script("arguments[0].click();", gender_radio)
            print(" -> Wybrano płeć: Pan")
        except Exception as e:
            print(f" -> Nie udało się zaznaczyć płci (może już zaznaczona?): {e}")

        driver.find_element(By.NAME, "firstname").send_keys(faker.first_name())
        driver.find_element(By.NAME, "lastname").send_keys(faker.last_name())

        print("\n5. Rejestracja nowego konta")
        driver.find_element(By.NAME, "email").send_keys(f"user_{random.randint(1000,9999)}@test.com")
        driver.find_element(By.NAME, "password").send_keys("Haslo1234!")
        print("chuj")
        driver.execute_script("document.querySelector('input[name=\"customer_privacy\"]').click()")
    #    driver.execute_script("document.querySelector('input[name=\"psgdpr\"]').click()")
        safe_click(driver.find_element(By.NAME, "continue"))
        print("\nPOMYŚLNIE ZAREJESTROWANO")
    except:
        print("Pominięto rejestrację.")

    try:
        wait.until(EC.visibility_of_element_located((By.NAME, "address1")))
        driver.find_element(By.NAME, "address1").send_keys(faker.street_address())
        driver.find_element(By.NAME, "postcode").send_keys("00-001")
        driver.find_element(By.NAME, "city").send_keys(faker.city())
        safe_click(driver.find_element(By.NAME, "confirm-addresses"))
    except:
        pass
    
    print("\n6. Wybór jednego z dwóch przewoźników")
    
    wait.until(EC.element_to_be_clickable((By.NAME, "confirmDeliveryOption")))
    
    delivery_radios = driver.find_elements(By.CSS_SELECTOR, ".delivery-option input[type='radio']")
    
    if len(delivery_radios) >= 2:
        choice = random.randint(0, 1) 
        print(f"Znaleziono {len(delivery_radios)} przewoźników. Wybieram opcję nr: {choice+1}")
        safe_click(delivery_radios[choice])
    elif len(delivery_radios) == 1:
        print("Tylko jeden przewoźnik dostępny - wybieram go.")
        safe_click(delivery_radios[0])
    else:
        print("UWAGA: Nie znaleziono opcji dostawy! Klikam Dalej domyślnie.")

    safe_click(wait.until(EC.element_to_be_clickable((By.NAME, "confirmDeliveryOption"))))

    print("\nPOMYŚLNIE WYBRANO PRZEWOŹNIKA")
    print("\n7. Wybór metody płatności: przy odbiorze")

    payment_opts = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[name='payment-option']")))
    
    cod_found = False
    for opt in payment_opts:
        if "cash" in opt.get_attribute("data-module-name") or "odbior" in opt.get_attribute("id"):
             safe_click(opt)
             cod_found = True
             break
    
    if not cod_found: safe_click(payment_opts[0])

    print("\nPOMYŚLNIE WYBRANO METODĘ PŁATNOŚCI")

    safe_click(driver.find_element(By.ID, "conditions_to_approve[terms-and-conditions]"))
    safe_click(driver.find_element(By.ID, "payment-confirmation").find_element(By.TAG_NAME, "button"))
    print("\nPOMYŚLNIE WYKONANO ZAMÓWIENIE")
    
    print("\n8. Zatwierdzenie zamówienia")
    wait.until(EC.presence_of_element_located((By.ID, "content-hook_order_confirmation")))
    print("\nPOMYŚLNIE ZATWIERDZONO")
    
    print("\n9. Sprawdzenie statusu zamówienia")
    driver.get(URL + "index.php?controller=history")
    status = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr:first-child .label-pill"))).text
    print(f"POMYŚLNIE SPRAWDZONO, STATUS: {status}")

    print("\n10. Pobranie faktury VAT")
    try:
        pdf_link = driver.find_element(By.CSS_SELECTOR, "tbody tr:first-child a[href*='pdf-invoice']")
        print(f"FAKTURA URL: {pdf_link.get_attribute('href')}")
    except:
        print("OBECNIE BRAK FAKTURY VAT.")

    print(f"\n=== SUKCES! Czas: {time.time() - start_time:.2f}s ===")

except Exception as e:
    print(f"\n!!! BŁĄD: {e}")
finally:
    # driver.quit()
    pass