from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from faker import Faker


fake = Faker(locale="pl_PL")
BASE_URL = "https://bikepart.pl/pl/" 


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)


def pauza(komunikat="Sprawdź przeglądarkę"):
    """Zatrzymuje skrypt do momentu naciśnięcia ENTER."""
    print(f"\nPAUZA: {komunikat}")
    print("   (Przeglądarka jest otwarta. Możesz klikać i sprawdzać.)")
    input("    Naciśnij ENTER w tej konsoli, aby kontynuować test...\n")
    print("    Wznawiam działanie skryptu...\n")

def generate_safe_email():
    
    return f"test_{int(time.time())}_{random.randint(100,999)}@example.com"

def add_products_directly_from_category(category_url, count_needed):
    print(f"\n--- Wchodzę do kategorii: {category_url} ---")
    driver.get(category_url)
    
    
    
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "input-group-add-cart")))
        product_containers = driver.find_elements(By.CLASS_NAME, "input-group-add-cart")
    except:
        print(" ! Nie znaleziono produktów na liście.")
        return

    total_products = len(product_containers)
    print(f" -> Znaleziono {total_products} produktów na liście.")

    
    if total_products < count_needed:
        count_needed = total_products 
        

   
    random_indices = [1,2,3,4,5]

   
    print(f" -> Wylosowano produkty o indeksach: {random_indices}")

   
    added_counter = 0
    
    for index in random_indices:
        try:
            
            containers = driver.find_elements(By.CLASS_NAME, "input-group-add-cart")
            current_product = containers[index]
            
            
            qty_input = current_product.find_element(By.CSS_SELECTOR, "input.input-qty")
            
            
            random_qty = random.randint(1, 7)
            
            
            driver.execute_script("arguments[0].value = '';", qty_input) 
            qty_input.send_keys(str(random_qty))
            
            
            add_btn = current_product.find_element(By.CSS_SELECTOR, "button[data-button-action='add-to-cart']")
            
           
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_btn)
            time.sleep(0.5)
            
            
            driver.execute_script("arguments[0].click();", add_btn)
            print(f" -> Kliknięto produkt nr {index} (ilość: {random_qty}). Czekam na modal...")

            
            continue_btn = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.cart-content-btn button[data-dismiss='modal']")
            ))
            
            continue_btn.click()
            
            
            wait.until(EC.invisibility_of_element_located((By.ID, "blockcart-modal"))) 
           
            time.sleep(1.5) 
            
            added_counter += 1
            print(f" -> SUKCES: Dodano {added_counter}/{count_needed}")

        except Exception as e:
            print(f" ! Błąd przy produkcie indeks {index}: {e}")
            
            try:
                driver.find_element(By.CSS_SELECTOR, "button[data-dismiss='modal']").click()
                time.sleep(1)
            except:
                pass
            continue


def test_step_1_add_products():
    print("--- KROK 1: Dodawanie produktów z kategorii ---")
    
    cat1 = f"{BASE_URL}2616-motocykle-honda"
    cat2 = f"{BASE_URL}3212-cb500-hornet-2024-"
    
    add_products_directly_from_category(cat1, 5) 
    add_products_directly_from_category(cat2, 5)
    print("KROK 1 ZAKOŃCZONY.")

def test_step_2_search_and_add():
    print("--- KROK 2: Wyszukiwanie i dodanie losowego ---")
    search_box = driver.find_element(By.NAME, "s")
    search_box.clear()
    search_box.send_keys("honda")
    search_box.send_keys(Keys.RETURN)
    
    
    wait.until(EC.presence_of_element_located((By.ID, "products")))
    products = driver.find_elements(By.CSS_SELECTOR, ".product-miniature .thumbnail.product-thumbnail")
    
    if products:
        random_prod = random.choice(products)
        random_prod.click()
        
        
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-cart"))).click()
        
       
        continue_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".cart-content-btn .btn-secondary")))
        continue_btn.click()
        print("KROK 2 ZAKOŃCZONY.")
    else:
        print("Brak wyników wyszukiwania.")

def test_step_3_remove_from_cart():
    print("--- KROK 3: Usuwanie 3 produktów ---")
    driver.get(f"{BASE_URL}koszyk")
    
    for i in range(3):
        try:
            
            remove_buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "remove-from-cart")))
            if remove_buttons:
                remove_buttons[0].click()
                print(f" -> Usunięto produkt {i+1}")
                time.sleep(2) 
            else:
                break
        except Exception as e:
            print("Koniec usuwania lub błąd:", e)
            
    print("KROK 3 ZAKOŃCZONY.")

def test_step_4_to_6_checkout_process():
    print("--- KROK 4-6: Rejestracja i Dostawa ---")
    
    driver.get(f"{BASE_URL}zamowienie")
    
   
    try:
        firstname = fake.first_name()
        lastname = fake.last_name()
        
        wait.until(EC.element_to_be_clickable((By.NAME, "firstname"))).send_keys(firstname)
        driver.find_element(By.NAME, "lastname").send_keys(lastname)
        driver.find_element(By.NAME, "email").send_keys(generate_safe_email())
        driver.find_element(By.NAME, "password").send_keys("Test1234!")
        
       
        driver.find_element(By.NAME, "customer_privacy").click()
        driver.find_element(By.NAME, "psgdpr").click()
        
        driver.find_element(By.CSS_SELECTOR, "button[data-link-action='register-new-customer']").click()
        print(" -> Konto zarejestrowane.")
    except Exception as e:
        print("Możliwe, że jesteś już zalogowany lub formularz wygląda inaczej:", e)

    
    try:
        wait.until(EC.element_to_be_clickable((By.NAME, "address1"))).send_keys(fake.street_address())
        driver.find_element(By.NAME, "postcode").send_keys(fake.postcode())
        driver.find_element(By.NAME, "city").send_keys(fake.city())
        
       
        driver.find_element(By.NAME, "confirm-addresses").click()
        print(" -> Adres dodany.")
    except:
        print("Pominięto krok adresu (może już istnieje).")

    
    print(" -> Wybór przewoźnika...")
    
    wait.until(EC.presence_of_element_located((By.ID, "checkout-delivery-step")))
    
    
    delivery_options = driver.find_elements(By.CSS_SELECTOR, ".delivery-option input") 
    
    if len(delivery_options) >= 2:
        
        choice = random.choice([0, 1])
        
        driver.execute_script("arguments[0].click();", delivery_options[choice])
        print(f" -> Wybrano przewoźnika nr {choice+1}")
    else:
        driver.execute_script("arguments[0].click();", delivery_options[0])
        print(" -> Wybrano jedynego dostępnego przewoźnika.")

   
    wait.until(EC.element_to_be_clickable((By.NAME, "confirmDeliveryOption"))).click()
    print("KROK 4-6 ZAKOŃCZONY.")

   
    return 

   
    payment_options = driver.find_elements(By.CSS_SELECTOR, ".payment-options .payment-option")
    found_cod = False
    for option in payment_options:
        if "odbiorze" in option.text.lower() or "cash" in option.text.lower():
            option.find_element(By.CSS_SELECTOR, "input").click() # Klikamy radio
            found_cod = True
            break
    
    if not found_cod and len(payment_options) > 0:
        payment_options[0].find_element(By.CSS_SELECTOR, "input").click()

    
    driver.find_element(By.ID, "conditions_to_approve[terms-and-conditions]").click()
    
    # Przycisk "Złóż zamówienie"
    # driver.find_element(By.ID, "payment-confirmation").find_element(By.TAG_NAME, "button").click()


# --- URUCHOMIENIE TESTÓW ---
try:
    # Uruchamiamy funkcje jedna po drugiej, NIE czyszcząc ciasteczek między nimi,
    # aby zachować sesję i koszyk.
    
   
    test_step_1_add_products()
    pauza()
    test_step_2_search_and_add()
   # test_step_3_remove_from_cart()
    test_step_4_to_6_checkout_process()
    
    print("\n--- TEST ZAKOŃCZONY SUKCESEM (do etapu dostawy) ---")
    input("Naciśnij ENTER w konsoli, aby zamknąć przeglądarkę...")

except Exception as e:
    print(f"\n!!! BŁĄD PODCZAS TESTU: {e}")
    driver.save_screenshot("error.png")

finally:
    driver.quit()