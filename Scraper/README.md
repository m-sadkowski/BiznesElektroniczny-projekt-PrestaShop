# Scraper

## Opis

Folder **Scraper** zawiera narzędzie napisane w Pythonie, którego zadaniem jest pobieranie danych o produktach ze sklepu bikepart.pl i zapisywanie wyników w folderze `ScraperResults`.

W folderze zawarty jest również folder `importer` zawierający skrypty importujące zescrapowane produkty do Prestashop poprzez REST API.

**UWAGA!** ScraperResults zawiera już zescrapowane dane!

W skrypcie `scraper.py` można edytować docelową ilość scrapowanych produktów poprzez zmianę wartości zmiennej *TARGET_PRODUCT_COUNT*.

---

## Uruchomienie

Aby uruchomić scraper, należy:

1. Zainstalować zależności z pliku `requirements.txt`:
```bash
pip install -r requirements.txt
```
2. Odpalić scraper:
```bash
python scraper.py
```
3. Pójść po herbatę i poczekać aż skrypt się w pełni wykona (może to trwać bardzo długo!)
