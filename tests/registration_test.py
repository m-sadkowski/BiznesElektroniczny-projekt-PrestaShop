


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import random
import string


# ─────────────────────────────────────────────
# KONFIGURACJA
# ─────────────────────────────────────────────
BASE_URL = "http://localhost:8080/"      # ← TUTAJ WSTAW SWÓJ ADRES SKLEPU
PASSWORD = "Test1234!"

# Generowanie unikalnego maila
def random_email():
    return "test_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + "@mail.com"

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-web-security")

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver

# ─────────────────────────────────────────────
# TEST REJESTRACJI
# ─────────────────────────────────────────────
def test_registration():
    service = Service()
    driver = get_driver()

    driver.maximize_window()
    driver.get(BASE_URL + "login?create_account=1")

    driver.find_element(By.CLASS_NAME, "user-info").click()
    driver.find_element(By.CLASS_NAME, "no-account").click()
    driver.find_element(By.ID, "field-id_gender-1").click()

    firstname = "Michal"
    lastname = "Matysiak"
    email = "mmatysiak2004@gmail.com"

    driver.find_element(By.ID, "field-firstname").send_keys(firstname)
    driver.find_element(By.ID, "field-lastname").send_keys(lastname)
    driver.find_element(By.ID, "field-email").send_keys(email)
    driver.find_element(By.ID, "field-password").send_keys("Haslo123")
    driver.find_element(By.NAME, "customer_privacy").click()
    driver.find_element(By.NAME, "psgdpr").click()
    driver.find_element(By.CLASS_NAME, "form-control-submit").click()
    time.sleep(1)

    user_info = driver.find_element(By.CLASS_NAME, "user-info")
    assert (firstname + " " + lastname) in user_info.text

    print("Test D passed!")


    driver.quit()



# ─────────────────────────────────────────────
# URUCHAMIANIE
# ─────────────────────────────────────────────
if __name__ == "__main__":
    test_registration()