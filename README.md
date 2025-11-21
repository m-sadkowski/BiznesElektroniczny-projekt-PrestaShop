# Klon sklepu bikepart.pl - Projekt Biznes Elektroniczny 2025

## Opis projektu

Projekt zrealizowany w ramach przedmiotu **"Biznes elektroniczny"** na **Politechnice Gdańskiej**. Jego celem było stworzenie w pełni funkcjonalnego klona sklepu internetowego bikepart.pl przy użyciu platformy e-commerce **PrestaShop**.

Główne założenia projektu obejmowały:

  * Analizę i odtworzenie kluczowych funkcjonalności oryginalnego sklepu.
  * Implementację procesów biznesowych, takich jak zarządzanie produktami, zamówieniami i klientami.
  * Zastosowanie wiedzy z zakresu marketingu internetowego i strategii e-biznesu zdobytej na zajęciach.
  * Wdrożenie platformy z użyciem konteneryzacji, zgodnie z efektami uczenia się przedmiotu.

---

##  Wykorzystane technologie

* **Platforma e-commerce:** PrestaShop
* **System do zarządzania kompozycją kontenerów:** Docker

---

## Uruchomienie projektu

Aby uruchomić projekt lokalnie, wykonaj poniższe kroki.

### Wymagania wstępne

### Instalacja

1.  **Sklonuj repozytorium:**

    ```bash
    git clone https://github.com/m-sadkowski/BiznesElektroniczny-projekt-PrestaShop.git
    cd BiznesElektroniczny-projekt-PrestaShop
    ```

2.  **Uruchomienie środowiska sklepu za pomocą Docker**

    Wymagane: Instalacja Docker https://docker.com

  * Wejdź do folderu **Config** i uruchom instalację kontenerów

    ```bash
    cd Config
    docker-compose up -d # -d powoduje działanie w tle
    ```
  
  * Po uruchomieniu kontenerów wejdź na **localhost:8080** i przejdź przez proces instalacyjny Prestashop w następujący sposób:
    - Wybierz język instalacji: **Polski**
    - Zaakceptuj licencję oraz wprowadź dane sklepu i administratora
    - **UWAGA!** Nie należy tworzyć domyślnych produktów ani nie włączać SSL
    - W ustawieniach bazy danych wpisz:
      * adres: db
      * uzytkownik: prestashop_user
      * hasło: user123
    - Kliknij "Przetestuj połączenie z bazą danych"
    - Zakończ instalację

  * Po instalacji Prestashop usunąć folder install

    ```bash
    docker-compose exec prestashop rm -rf /var/www/html/install
    ```

  * Sprawdź nazwę folderu admina - będzie to admin+coś, np. admin7971fvqjg

    ```bash
    docker-compose exec prestashop ls /var/www/html
    ```

  * Przejdź do panelu administracyjnego: **localhost:8080/admin**

  * Wejdź w Design -> Theme & Logo

  * Wybierz motyw **BE**

  Docker - przydatne komendy

    ```bash
    # Zatrzymanie kontenerów
    docker-compose stop
    # Ponowne uruchomienie zatrzymanych kontenerów
    docker-compose start
    # Zatrzymanie i usunięcie kontenerów
    docker-compose down
    # Zatrzymanie, usunięcie kontenerów ORAZ wolumenów (usuwa dane sklepu - foldery w kontenerze)
    docker-compose down -v
    ```

---

## ‍Zespół

Projekt został zrealizowany w ramach pracy zespołowej, zgodnie z założeniami przedmiotu. Skład zespołu:

  * **Michał Sadkowski**
  * **Michał Matysiak**
  * **Dawid Wesołowski**
  * **Ostap Lozovyy**