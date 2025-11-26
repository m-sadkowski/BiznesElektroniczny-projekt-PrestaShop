#!/bin/bash

# --- KONFIGURACJA ---
DB_SERVICE="db"
DB_USER="prestashop_user"
DB_PASSWD="user123"
DB_NAME="prestashop"
PS_SERVICE="prestashop"

# Ścieżka do pliku zrzutu
DUMP_FILE="./export/prestashop_dump.sql"

# Sprawdzenie czy plik dumpa istnieje
if [ ! -f "$DUMP_FILE" ]; then
    echo "BŁĄD: Nie znaleziono pliku $DUMP_FILE"
    exit 1
fi

# Wgrywanie zrzutu SQL
echo "Importowanie danych z $DUMP_FILE..."
cat "$DUMP_FILE" | docker compose exec -T $DB_SERVICE mysql -u$DB_USER -p$DB_PASSWD $DB_NAME

if [ $? -eq 0 ]; then
    echo "Sukces: Baza danych została przywrócona."
else
    echo "BŁĄD: Wystąpił problem przy imporcie SQL."
    exit 1
fi

# Czyszczenie cache PrestaShop
docker compose exec -T $PS_SERVICE rm -rf /var/www/html/var/cache/prod /var/www/html/var/cache/dev &>/dev/null

echo "PRZYWRACANIE ZAKOŃCZONE POMYŚLNIE."
