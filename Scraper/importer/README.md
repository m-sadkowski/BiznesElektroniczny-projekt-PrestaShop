# REST API Importer do PrestaShop

Ten folder zawiera skrypty do importu danych do PrestaShop:

* `import_categories.py` – tworzenie kategorii i podkategorii
* `import_products.py` – import produktów

---

## Wymagania wstępne

1. W panelu administratora w sekcji **Configure** wejdź do **Advanced Parameters/Webservice**.
2. Kliknij **Dodaj nowy klucz API**.
3. Wygeneruj i skopiuj klucz API oraz nadaj mu wszystkie uprawnienia dla zasobów: **categories**, **images**, **products**, **stock_availables**
4. Włącz API PrestaShop i zapisz zmiany.
5. WAŻNE! W plikach **import_categories.py** oraz **import_products.py** uzupełnij wartość zmiennej *PS_WS_AUTH_KEY* o wartość wygenerowanego klucza API

---

## Kolejność uruchamiania

1. Zainstaluj wymagane biblioteki:
```bash
    pip install -r requirements.txt
```
2. Importuj kategorie:
```bash
    python import_categories.py
```

   * Skrypt powinien wygenerować plik `category_id_map.json` w tym folderze.
3. Importuj produkty:
```bash
    python import_products.py
```
