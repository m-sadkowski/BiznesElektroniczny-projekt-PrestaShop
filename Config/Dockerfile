FROM prestashop/prestashop:1.7.8 

# Zmienne środowiskowe dla OpenSSL
ENV DAYS=365 \
    COMMON_NAME=localhost \
    CERT_PATH=/etc/ssl/certs/server.crt \
    KEY_PATH=/etc/ssl/private/server.key

# Instalacja OpenSSL, włączenie modułów SSL i Rewrite
RUN apt-get update && \
    apt-get install -y openssl && \
    a2enmod ssl && a2enmod rewrite && \
    rm -rf /var/lib/apt/lists/*

# Generowanie samopodpisanego klucza i certyfikatu SSL
RUN openssl genrsa -out ${KEY_PATH} 2048 && \
    openssl req -new -x509 -sha256 -key ${KEY_PATH} -out ${CERT_PATH} -days ${DAYS} \
    -subj "/C=PL/ST=Pomerania/L=Gdansk/O=4D/CN=${COMMON_NAME}"

# Ustawienie uprawnień dla klucza prywatnego
RUN chmod 600 ${KEY_PATH}

# Kopiowanie pliku konfiguracyjnego
COPY prestashop_ssl.conf /etc/apache2/sites-available/prestashop_ssl.conf

# Aktywacja nowej konfiguracji VirtualHost
RUN a2ensite prestashop_ssl