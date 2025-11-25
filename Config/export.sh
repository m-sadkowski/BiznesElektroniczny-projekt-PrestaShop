#!/bin/bash

# --- KONFIGURACJA ---
DB_USER="prestashop_user"
DB_PASSWD="user123"
DB_NAME="prestashop"
DB_SERVICE="db" 
DB_PREFIX="ps_"

EXPORT_DIR="./export"
FILENAME="prestashop_dump.sql"
FULL_PATH="${EXPORT_DIR}/${FILENAME}"

IGNORE_TABLES_SUFFIXES=(
    "connections"
    "connections_source"
    "guest"
    "log"
    "statssearch"
    "pagenotfound"
    "date_range"
)

IGNORE_STRING=""
for SUFFIX in "${IGNORE_TABLES_SUFFIXES[@]}"; do
    TABLE="${DB_PREFIX}${SUFFIX}"
    IGNORE_STRING+=" --ignore-table=${DB_NAME}.${TABLE}"
done

# Sprawdzenie i utworzenie folderu docelowego
if [ ! -d "$EXPORT_DIR" ]; then
    mkdir -p "$EXPORT_DIR"
    echo "Utworzono folder eksportu: $EXPORT_DIR"
fi

echo "Rozpoczynam eksport do pliku $FULL_PATH..."

# Wykonanie zrzutu z pominięciem wybranych tabel
docker compose exec -T $DB_SERVICE mysqldump \
  -u $DB_USER \
  -p$DB_PASSWD \
  $IGNORE_STRING \
  $DB_NAME \
  > "$FULL_PATH"

if [ $? -eq 0 ]; then
    echo "Eksport zakończony pomyślnie do pliku $FULL_PATH."
else
    echo "Błąd podczas eksportu."
    exit 1
fi