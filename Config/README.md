# Config

Ten folder zawiera pliki konfiguracyjne niezbędne do uruchomienia środowiska Docker oraz skrypty automatyzujące procesy backupu i przywracania sklepu PrestaShop.

## Zawartość katalogu

* Pliki służące do odpalenia środowiska Docker oraz wygenerowania samodzielnie podpisanych certyfikatów SSL, takie jak `docker-compose.yml`, `Dockerfile`, `prestashop_ssl.conf`

* Folder **`export/`**
  Katalog przeznaczony do przechowywania eksportu ustawień sklepu.
  * `prestashop_dump.sql`: Aktualny zrzut bazy danych (struktura + dane)

---

## Skrypty automatyzacji

W folderze znajdują się skrypty ułatwiające zarządzanie stanem sklepu.

### 1. Eksport ustawień (`export.sh`)
Skrypt wykonuje zrzut bazy danych (dump) do pliku `export/prestashop_dump.sql`.

**Uruchomienie:**
```bash
./export.sh
```

### 2. Przywracanie ustawień (`restore.sh`)
Skrypt służy do przywracania ustawień sklepu z pliku `export/prestashop_dump.sql`.

**Uruchomienie:**
```bash
./restore.sh
```