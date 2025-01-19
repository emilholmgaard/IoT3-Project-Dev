# Nginx SSL Konfiguration

## Generering af SSL-certifikat

1. Opret en mappe til at gemme SSL-certifikaterne, hvis den ikke allerede findes:

    ```bash
    sudo mkdir -p /etc/nginx/ssl
    ```

2. Brug OpenSSL til at generere et selvsigneret certifikat og en privat nøgle:

    ```bash
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt
    ```

## Nginx Konfiguration

1. Åbn din Nginx-konfigurationsfil, som findes i `nginx/src/nginx_config`:

    ```bash
    sudo nano /nginx/src/nginx_config
    ```

2. Tilføj følgende SSL-konfiguration:

    ```nginx
    server {
        listen 443 ssl;
        server_name localhost;

        ssl_certificate /etc/nginx/ssl/nginx.crt;
        ssl_certificate_key /etc/nginx/ssl/nginx.key;

        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        gzip on;
        gzip_types text/plain text/css application/javascript application/json application/xml application/xml+rss text/javascript;
        gzip_min_length 1000;

        location / {
            root /var/www/webapp-pi0/dist;
            index index.html index.htm;
        }

        location ~* \.(jpg|jpeg|png|gif|css|js|woff|woff2|ttf|eot|svg|ico|otf|json)$ {
            expires 30d;
            add_header Cache-Control "public, no-transform";
        }

        error_page 404 /404.html;
        error_page 500 502 503 504 /50x.html;

        location = /50x.html {
            root /var/www/html;
        }
    }
    ```

3. **Bemærk**: Sørg for, at din webapp er placeret i `/var/www/webapp-pi0/dist`, da dette er den angivne `root`-sti.

## Genstart Nginx

For at anvende ændringerne skal du genstarte Nginx:

```bash
sudo systemctl restart nginx
