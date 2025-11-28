from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
import time
import random
import string
import traceback # Do wyświetlania pełnych błędów

# ─────────────────────────────────────────────
# KONFIGURACJA
# ─────────────────────────────────────────────
BASE_URL = "http://localhost:8080/" 

def random_email():
    return "test_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + "@mail.com"




def get_driver():
    options = FirefoxOptions()
    options.accept_insecure_certs = True # Firefox obsługuje to natywnie bardzo dobrze
    driver = webdriver.Firefox(options=options)
    return driver


def test_registration():
    driver = get_driver()
    
    print("--- START TESTU ---")

    try:
        driver.maximize_window()
        
        # Sprawdź czy na pewno masz taki URL (login vs logowanie)
        target_url = BASE_URL + "login?create_account=1"
        print(f"1. Otwieram stronę: {target_url}")
        driver.get(target_url)

        # ─────────────────────────────────────────────────────────────
        # PAUZA RATUNKOWA
        # Jeśli widzisz ekran błędu SSL ("Połączenie nie jest prywatne"),
        # kliknij w przeglądarce ręcznie, a potem wciśnij ENTER w konsoli.
        # ─────────────────────────────────────────────────────────────
        print("\n!!! SPÓJRZ NA PRZEGLĄDARKĘ !!!")
        print("Jeśli widzisz błąd certyfikatu - przeklikaj go ręcznie.")
        print("Jeśli strona się załadowała - po prostu wciśnij ENTER w tej konsoli, aby kontynuować...")
        input("Naciśnij ENTER aby kontynuować test >> ")
        # ─────────────────────────────────────────────────────────────

        wait = WebDriverWait(driver, 10)
        
        print("2. Szukam przycisku wyboru płci...")
        wait.until(EC.element_to_be_clickable((By.ID, "field-id_gender-1"))).click()

        print("3. Wypełniam formularz...")
        firstname = "Michal"
        lastname = "Matysiak"
        email = random_email() 

        driver.find_element(By.ID, "field-firstname").send_keys(firstname)
        driver.find_element(By.ID, "field-lastname").send_keys(lastname)
        driver.find_element(By.ID, "field-email").send_keys(email)
        driver.find_element(By.ID, "field-password").send_keys("Haslo123")
        
        print("4. Zaznaczam zgody...")
        driver.find_element(By.NAME, "customer_privacy").click()
        driver.find_element(By.NAME, "psgdpr").click()
        
        print("5. Klikam Zapisz...")
        driver.find_element(By.CLASS_NAME, "form-control-submit").click()
        
        print("6. Weryfikuję zalogowanie...")
        user_info = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "user-info")))
        
        assert (firstname + " " + lastname) in user_info.text
        print(f"\n✅ SUKCES! Konto założone: {email}")

    except Exception as e:
        print("\n❌ WYSTĄPIŁ BŁĄD!")
        print("Oto co poszło nie tak (pokaż mi to):")
        print("-" * 30)
        traceback.print_exc() # Wypisuje dokładną przyczynę błędu
        print("-" * 30)
        
    # Usunąłem driver.quit(), żebyś mógł zobaczyć stan przeglądarki po błędzie

if __name__ == "__main__":
    test_registration()