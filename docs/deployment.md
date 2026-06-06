# Idle Forest Linux Deployment

This is the current lightweight deployment path for a small test server.
It targets Ubuntu 24.04 LTS, about 10-20 players, and the current Python
stdlib server with SQLite persistence.

## Server Size

- 2 CPU cores
- 2 GB RAM
- 40 GB system disk
- 200 Mbps public bandwidth

## Install Packages

```bash
sudo apt update
sudo apt install -y python3 python3-venv git nginx ufw
```

## Pull Code

```bash
cd /opt
sudo git clone https://github.com/bujarlati/Test.git idle-game
sudo chown -R $USER:$USER /opt/idle-game
cd /opt/idle-game
git checkout feature/idle-forest-polish
git pull
mkdir -p data
```

## Manual Smoke Test

```bash
python3 server.py --host 127.0.0.1 --port 8000
```

## Package Deploy

Release packages include `scripts/deploy_package.sh`. The script preserves `/opt/idle-game/data`, replaces the rest of the app, and restarts the `idle-game` systemd service.

For the first package that contains the script, upload the package to `/tmp`,
extract a temporary copy, and run the script from there:

```bash
mkdir -p /tmp/idle-game-release
rm -rf /tmp/idle-game-release/*
tar -xzf /tmp/idle_forest_release.tar.gz -C /tmp/idle-game-release
sudo bash /tmp/idle-game-release/scripts/deploy_package.sh /tmp/idle_forest_release.tar.gz
```

After that, future package updates only need:

```bash
sudo /opt/idle-game/scripts/deploy_package.sh /tmp/idle_forest_release.tar.gz
```

The optional arguments are target directory and service name:

```bash
sudo /opt/idle-game/scripts/deploy_package.sh /tmp/idle_forest_release.zip /opt/idle-game idle-game
```

## systemd Service

Create the service:

```bash
sudo nano /etc/systemd/system/idle-game.service
```

Paste:

```ini
[Unit]
Description=Idle Game Server
After=network.target

[Service]
WorkingDirectory=/opt/idle-game
ExecStart=/usr/bin/python3 /opt/idle-game/server.py --host 127.0.0.1 --port 8000
Restart=always
RestartSec=3
User=root
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

Enable it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable idle-game
sudo systemctl start idle-game
sudo systemctl status idle-game
```

## Nginx Reverse Proxy

Create the site:

```bash
sudo nano /etc/nginx/sites-available/idle-game
```

Paste, replacing `SERVER_NAME` with a domain or public IP:

```nginx
server {
    listen 80;
    server_name SERVER_NAME;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable it:

```bash
sudo ln -s /etc/nginx/sites-available/idle-game /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 80
sudo ufw enable
```

## Optional HTTPS

After pointing a domain at the server:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx
```

## Important Data

Back up this file regularly:

```bash
/opt/idle-game/data/idle_forest.db
```
