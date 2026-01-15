#!/bin/bash
set -e

TARGET_DOMAIN="$1"
DUMP_FILE="dump.sql"
DB_NAME="BE_197747"

if [ -z "$TARGET_DOMAIN" ]; then
    echo "Błąd: Nie podano adresu domeny!"
    exit 1
fi

if [ ! -f $DUMP_FILE ]; then
    echo "Błąd: Nie znaleziono pliku $DUMP_FILE!"
    exit 1
fi

CONTAINER=$(docker ps --filter "name=admin-mysql_db" --format "{{.Names}}" | head -n 1)

if [ -z "$CONTAINER" ]; then
    echo "Błąd: Kontener bazy danych (admin-mysql_db) nie działa!"
    exit 1
fi

docker exec "$CONTAINER" mysql -u root -pstudent -e "DROP DATABASE IF EXISTS $DB_NAME; CREATE DATABASE $DB_NAME;"
docker exec -i "$CONTAINER" mysql -u root -pstudent $DB_NAME < $DUMP_FILE
docker exec "$CONTAINER" mysql -u root -pstudent $DB_NAME -e "UPDATE ps_shop_url SET domain='$TARGET_DOMAIN', domain_ssl='$TARGET_DOMAIN', physical_uri='/';"
