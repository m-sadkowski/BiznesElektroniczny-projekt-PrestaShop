#!/bin/bash
set -e

SERVER_IP=$(hostname -I | awk '{print $1}')
MY_PORT="19777"
FULL_DOMAIN="$SERVER_IP:$MY_PORT"

echo "Adres sklepu: $FULL_DOMAIN"
./load-db.sh "$FULL_DOMAIN"

docker stack deploy -c deploy.yml BE_197747 --with-registry-auth
