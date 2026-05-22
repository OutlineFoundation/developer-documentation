# Shadowsocks-over-WebSockets behind HTTPs website

This documentation is an extension of the existing WebSockets documentation. It
adds a lot of additional information and components to enhance the setup, user
experience, and obfuscation (via a bogus website).

## Prerequisites

- a Linux server
  - Operating System:
    - Debian Linux

      Note: In this document, [Ubuntu](https://ubuntu.com/) is being used.
  - Platform:
    - any 64-bit system

      Note: In this document, a [Raspberry Pi](https://www.raspberrypi.com/)
            is used as the server (ARM64/AArch64).

- a non-_root_ user that has _sudo_ privileges

## Step 1: Setup Website Domain and DNS

### Get a domain name

Get a domain name from a domain registrar.

Note: In this document, the domain `fake-website.com` will be used as the
      example domain that you purchase from a domain registrar for your bogus
      website.

#### Configure DNS Settings

**If your server has a static IP, then:**

Create an `A` record in your DNS settings to point `fake-website.com` to your
static IP address
```text
fake-website.com    A    XXX.XXX.XXX.XXX
```
where `XXX.XXX.XXX.XXX` is replaced by the server's IP address.

**Otherwise, if your server is in a network where the external IP address is
dynamic (occasionally  changes), like your home, then:**

Get a **Dynamic DNS (DDNS)** hostname from a DDNS provider such as
[No-IP](https://www.noip.com/) or [DuckDNS](https://www.duckdns.org/).

Note: Dynamic DNS (DDNS) maps a frequently changing (dynamic) IP address to a
      fixed hostname, allowing consistent remote access. By using a DDNS
      provider and a client (router or software), the system automatically
      updates DNS records, ensuring the hostname always points to the current IP
      address for services like home servers.

Note: in this document, No-IP is used as the DDNS provider, and the domain
      `your.ddns-hostname.com` will be used as the example DDNS domain that you
      obtain from this DDNS provider.

A DDNS client will be configured later in this document.

... and setup DNS settings for your DDNS hostname:

Create a `CNAME` record in your DNS settings to point `fake-website.com` to
`your.ddns-hostname.com`:
```text
fake-website.com    CNAME    your.ddns-hostname.com
```

Note: This will allow your _dynamic_ IP address to always point to your domain
      name.

## Step 2: Initial Linux Server Setup

SSH into your server.

### Step 2.1: Install OS Packages

Configure **APT package manager**:

Edit or create this file: `/etc/apt/apt.conf.d/10sandbox`
```shell
sudo nano /etc/apt/apt.conf.d/10sandbox
```
place this into the file:
```text
APT::Sandbox::User "root";
```
Note: `APT::Sandbox::User "root";` is a configuration directive used in
      Debian-based systems (like Ubuntu or Termux) to define which user account
      the **APT package manager** should use when performing sandboxed
      operations.

Update operating system (OS) and install packages:
```shell
sudo apt-get update
sudo apt-get dist-upgrade
sudo apt-get install -y telnet \
                        wget \
                        curl \
                        netcat \
                        nmap \
                        yq \
                        qrencode \
                        nginx libnginx-mod-stream \
                        certbot python3-certbot-nginx
sudo apt-get clean
```

### Step 2.2: _[optional]_ Install & Configure DDNS DUC

If you setup a DDNS hostname then you will need to setup a **Dynamic Update Client
(DUC)** to keep the hostname constantly up-to-date with your changing IP address.

The following steps show how to setup a No-IP DUC.

Download and Unpack DUC Binaries:
```shell
sudo mkdir -p /opt/noip-duc
cd /opt/noip-duc/
sudo wget https://dmej8g5cpdyqd.cloudfront.net/downloads/noip-duc_3.3.0.tar.gz
sudo tar xzf noip-duc_3.3.0.tar.gz
```

Note: At the time of writing, the latest version of the No-IP DUC was `3.3.0`.

Install DUC OS Package:
```shell
cd /opt/noip-duc/noip-duc_3.3.0/binaries/      
```
in this directory there are a few options (files):
```text
noip-duc_3.3.0_amd64.deb
noip-duc_3.3.0_arm64.deb
noip-duc_3.3.0_armhf.deb
noip-duc_3.3.0_x86_64-musl.gz
```
choose the correct option for the server's platform

Note: In this example, the server is a **Raspberry Pi** and we will choose `noip-duc_3.3.0_arm64.deb`
```shell
sudo apt-get install ./noip-duc_3.3.0_arm64.deb      
```

Setup a _systemd_ service for the DUC:

create a symlink for the service
```shell
sudo ln -s /opt/noip-duc/noip-duc_3.3.0/debian/service /etc/systemd/system/noip-duc.service
```

edit or create this file: `/etc/default/noip-duc`
```shell
sudo nano /etc/default/noip-duc
```
place this into the file:
```text
## File: /etc/default/noip-duc
NOIP_USERNAME=your-noip-ddns-key-username
NOIP_PASSWORD=your-noip-ddns-key-password
NOIP_HOSTNAMES=your.ddns-hostname.com
```
replace the values with your appropriate settings

Note: The username and password are not your No-IP credentials, they are a
      specific DDNS key (username and password pair) that you generate for your
      DDNS hostname in order for the DUC to authenticate properly, located in
      your account at: https://my.noip.com/ddns-keys

Enable the DUC service:
```shell
sudo systemctl daemon-reload
sudo systemctl enable noip-duc
sudo systemctl start noip-duc
sudo systemctl status noip-duc
```

Reboot server:
```shell
sudo reboot
```

## Step 3: Setup Firewall

Ensure that your server is reachable at port `80` and `443` on the firewall in
front of your server.

If your server is setup at home then go to your router's port forwarding
settings and allow port `80` and `443` traffic to forward to your home server.

## Step 4: Install & Configure Outline Shadowsocks Server

SSH into your server.

Download and unpack the Outline Shadowsocks server binaries.
```shell
sudo mkdir -p /opt/outline/bin
cd /opt/outline/bin/
sudo wget https://github.com/OutlineFoundation/tunnel-server/releases/download/v1.9.2/outline-ss-server_1.9.2_linux_arm64.tar.gz
sudo tar xzf outline-ss-server_1.9.2_linux_arm64.tar.gz
```

Note: At the time of writing, the latest version of the Outline Shadowsocks
      server was `1.9.2`.

Note: In the above `wget` command, the _arm64_ package was used because we are
      on a **Raspberry Pi** system. Replace this URL to the appropriate platform
      you are using from: https://github.com/OutlineFoundation/tunnel-server/releases

Configure Outline Shadowsocks server:

create directory:
```shell
sudo mkdir -p /opt/outline/config
```

create this file: `/opt/outline/config/server.yaml`
```shell
sudo nano /opt/outline/config/server.yaml
```
place this into the file:
```yaml
---
web:
  servers:
    - id: "outline-ss-server"
      listen:
        - "127.0.0.1:4444"
services:
  - listeners:
      - type: "websocket-stream"
        web_server: "outline-ss-server"
        path: "/9d4cd779f1c7c31867dc/tcp"
      - type: "websocket-packet"
        web_server: "outline-ss-server"
        path: "/9d4cd779f1c7c31867dc/udp"
    keys:
      - id: "client-1"
        cipher: "chacha20-ietf-poly1305"
        secret: "1fda6bc8e698ade456e9"
```

Note: In the above YAML, the following attributes are important to understand:

`web.servers[0].listen[0]` - port is set to `4444` but can be changed to
whatever you desire

`services[0].listeners[*].path` - these paths are secret, change them to
anything that is long and difficult to guess, keep it secret

`services[0].keys[0].secret` - this is the secret for your first initial client,
change this to anything that is 20 characters long, keep it secret

Setup a systemd service for the Outline Shadowsocks server:

create directory:
```shell
sudo mkdir -p /opt/outline/debian
```

create this file: `/opt/outline/debian/outline-ss-server.service`
```shell
sudo nano /opt/outline/debian/outline-ss-server.service
```
place this into the file:
```text
[Unit]
Description=Outline Shadowsocks Server
After=network.target auditd.service

[Service]
ExecStart=/opt/outline/bin/outline-ss-server --config /opt/outline/config/server.yaml --replay_history 10000
Restart=on-failure
Type=simple

[Install]
WantedBy=multi-user.target
```

create a symlink for the service:
```shell
sudo ln -s /opt/outline/debian/outline-ss-server.service /etc/systemd/system/outline-ss-server.service
```

enable the Outline Shadowsocks server service:
```shell
sudo systemctl daemon-reload
sudo systemctl enable outline-ss-server
sudo systemctl start outline-ss-server
sudo systemctl status outline-ss-server
```

Reboot server:
```shell
sudo reboot
```

## Step 5: Configure Outline Shadowsocks Client

SSH into your server.

Configure initial Outline Shadowsocks client:

create directory:
```shell
sudo mkdir -p /opt/outline/config/clients
```

create this file: `/opt/outline/config/clients/client-1.yaml`
```shell
sudo nano /opt/outline/config/clients/client-1.yaml
```
place this into the file:
```yaml
---
transport:
  $type: "tcpudp"

  tcp:
    $type: "shadowsocks"
    endpoint:
      $type: "websocket"
      url: "wss://fake-website.com/9d4cd779f1c7c31867dc/tcp"
    cipher: "chacha20-ietf-poly1305"
    secret: "1fda6bc8e698ade456e9"

  udp:
    $type: "shadowsocks"
    endpoint:
      $type: "websocket"
      url: "wss://fake-website.com/9d4cd779f1c7c31867dc/udp"
    cipher: "chacha20-ietf-poly1305"
    secret: "1fda6bc8e698ade456e9"
```

Note: In the above YAML, the following attributes are important to understand:

`transport.tcp.endpoint.url` - the path in this URL, after `fake-website.com`
must match the server config (above) listener of type "websocket-stream"

`transport.udp.endpoint.url` - the path in this URL, after `fake-website.com`
must match the server config (above) listener of type "websocket-packet"

`transport.tcp.secret` - this secret must match the server config (above)
key with id "client-1"

`transport.udp.secret` - this secret must match the server config (above)
key with id "client-1"

Note: Replace `fake-website.com` in all of the above with the domain name that
      you purchased.

### Step 5.1: _[Optional]_ Create Outline Shadowsocks Client Management Script

Add the following script to make managing Outline Shadowsocks clients easier.

Edit create this file: `/opt/outline/bin/outline-ss-clients`
```shell
sudo nano /opt/outline/bin/outline-ss-clients
```
place this into the file:
```shell
#!/bin/bash

OUTLINE_HOME="/opt/outline"
OUTLINE_CONFIG_HOME="${OUTLINE_HOME}/config"
OUTLINE_SERVER_CONFIG="${OUTLINE_CONFIG_HOME}/server.yaml"
OUTLINE_CLIENT_CONFIG_HOME="${OUTLINE_CONFIG_HOME}/clients"

OUTLINE_HOSTNAME="$(grep -l outline-ss-server /etc/nginx/sites-enabled/* | xargs grep server_name | head -1 | awk '{print $2}' | tr -d ';')"

KEY_CIPHER="chacha20-ietf-poly1305"
KEY_SECRET_LENGTH=20

function display_usage() {
  cat <<EOF
Manage Outline Shadowsocks clients

Usage: $(basename "${0}") <command>

Commands:
  list                    List all clients added
  add                     Add client
  remove <client-name>    Remove client
  qrcode <client-name>    Generate QR code for client access key
EOF
}

COMMAND="${1}"
shift
case "${COMMAND}" in
  "list"|"add"|"remove"|"qrcode")
    # all good
    ;;
  *)
    display_usage >&2
    exit 1
    ;;
esac

function list() {
  echo "Client List"
  echo "-----------"
  yq -r '.services[0].keys[].id' ${OUTLINE_SERVER_CONFIG}
  return 0
}

function add() {
  read -p "Enter a name for the client: " client_id
  if [[ ! "${client_id}" =~ ^[a-z][0-9a-z-]+[0-9a-z]$ ]] ; then
    echo "Client name must be at least 3 characters in length, and can contain only alphanumeric and hyphen characters"
    exit 1
  fi

  yq --exit-status --yaml-output '.services[0].keys[] | select(.id == "'${client_id}'")' ${OUTLINE_SERVER_CONFIG} > /dev/null 2>&1
  if (( ${?} == 0 )) ; then
    echo "Client \"${client_id}\" already exists"
    exit 1
  fi

  key_secret="$(cat /dev/urandom | tr -dc 'a-f0-9' | head -c ${KEY_SECRET_LENGTH})"
  transport_tcp_endpoint_url="$(yq -r '.services[0].listeners[] | select(.type == "websocket-stream") | .path' ${OUTLINE_SERVER_CONFIG})"
  transport_udp_endpoint_url="$(yq -r '.services[0].listeners[] | select(.type == "websocket-packet") | .path' ${OUTLINE_SERVER_CONFIG})"

  yq --yaml-output '.services[0].keys +=
[
  {
    "id": "'${client_id}'",
    "cipher": "'${KEY_CIPHER}'",
    "secret": "'"${key_secret}"'"
  }
]
' ${OUTLINE_SERVER_CONFIG} > ${OUTLINE_SERVER_CONFIG}.tmp
  mv ${OUTLINE_SERVER_CONFIG}.tmp ${OUTLINE_SERVER_CONFIG}
  echo "Updated server config with new client access key"

  cat <<EOF > "${OUTLINE_CLIENT_CONFIG_HOME}/${client_id}.yaml"
---
transport:
  \$type: "tcpudp"

  tcp:
    \$type: "shadowsocks"
    endpoint:
      \$type: "websocket"
      url: "wss://${OUTLINE_HOSTNAME}${transport_tcp_endpoint_url}"
    cipher: "chacha20-ietf-poly1305"
    secret: "${key_secret}"

  udp:
    \$type: "shadowsocks"
    endpoint:
      \$type: "websocket"
      url: "wss://${OUTLINE_HOSTNAME}${transport_udp_endpoint_url}"
    cipher: "chacha20-ietf-poly1305"
    secret: "${key_secret}"
EOF
  echo "Created new client config file"

  echo "Client config file: ${OUTLINE_CLIENT_CONFIG_HOME}/${client_id}.yaml"
  client_config_uri="${OUTLINE_HOSTNAME}/clients/${client_id}.yaml"
  client_config_url="https://${client_config_uri}"
  client_access_key="ssconf://${client_config_uri}"
  echo "Client config URL: ${client_config_url}"
  echo "Client access key: ${client_access_key}"

  systemctl restart outline-ss-server
  echo "Restarted Outline Shadowsocks server"

  return 0
}

function remove() {
  local client_id="${1}"

  read -p "Do you really want to remove client \"${client_id}\"? [Y/n]" confirm_remove
  if [[ "${confirm_remove}" != "Y" ]] ; then
    echo "Aborting operation"
    exit 1
  fi

  yq --exit-status --yaml-output '.services[0].keys[] | select(.id == "'${client_id}'")' ${OUTLINE_SERVER_CONFIG} > /dev/null 2>&1
  if (( ${?} != 0 )) ; then
    echo "Client \"${client_id}\" does not exist"
    exit 1
  fi

  yq --yaml-output 'del(.services[0].keys[] | select(.id == "'${client_id}'"))' ${OUTLINE_SERVER_CONFIG} > ${OUTLINE_SERVER_CONFIG}.tmp
  mv ${OUTLINE_SERVER_CONFIG}.tmp ${OUTLINE_SERVER_CONFIG}
  echo "Updated server config by removing client access key"

  echo "Client config file: ${OUTLINE_CLIENT_CONFIG_HOME}/${client_id}.yaml"
  rm "${OUTLINE_CLIENT_CONFIG_HOME}/${client_id}.yaml" > /dev/null 2>&1 || true
  echo "Removed client config file"

  systemctl restart outline-ss-server
  echo "Restarted Outline Shadowsocks server"

  return 0
}

function qrcode() {
  local client_id="${1}"

  yq --exit-status --yaml-output '.services[0].keys[] | select(.id == "'${client_id}'")' ${OUTLINE_SERVER_CONFIG} > /dev/null 2>&1
  if (( ${?} != 0 )) ; then
    echo "Client \"${client_id}\" does not exist"
    exit 1
  fi

  client_config_uri="${OUTLINE_HOSTNAME}/clients/${client_id}.yaml"
  client_access_key="ssconf://${client_config_uri}"
  qrencode -t "ANSIUTF8" "${client_access_key}"

  return 0
}

case "${COMMAND}" in
  "add"|"list")
    if (( ${#} != 0 )) ; then
      display_usage >&2
      exit 1
    fi
    "${COMMAND}"
    ;;
  "remove"|"qrcode")
    if (( ${#} != 1 )) ; then
      display_usage >&2
      exit 1
    fi
    "${COMMAND}" "${1}"
    ;;
  *)
    display_usage >&2
    exit 1
    ;;
esac
```

Using the client manager script:

Warning: Do not use this script until you have completed the [Step 6: Setup Bogus (Fake) Website](#abc) section.

**List existing clients**
```shell
cd /opt/outline/bin/
sudo ./outline-ss-clients list
```

**Add new client**
```shell
cd /opt/outline/bin/
sudo ./outline-ss-clients add
```

**Display QR code for existing client**
```shell
cd /opt/outline/bin/
sudo ./outline-ss-clients qrcode client-id
```
Note: Replace `client-id` with correct client id.

A QR code will be generated in the terminal, and you can scan this with a mobile
device that has the Outline client app installed by opening the camera app and
pointing it at the QR code.

Example QR code generated for `ssconf://fake-website.com/clients/client-1.yaml`:
```text
█████████████████████████████████████
█████████████████████████████████████
████ ▄▄▄▄▄ █▀ █▀▀▄█▀▄▀ ▄▄█ ▄▄▄▄▄ ████
████ █   █ █▀ ▄ █▀ ▄▄▀█ ▄█ █   █ ████
████ █▄▄▄█ █▀█ █▄█▀▀  ▄▄▀█ █▄▄▄█ ████
████▄▄▄▄▄▄▄█▄█▄█ █ █▄█▄█ █▄▄▄▄▄▄▄████
████  ▄  ▀▄   ▄█▄ ▄▄▀ ▀▀▀ ▀ ▀ ▀ ▀████
████▄ █▄▀ ▄█  ▀ ▄▄▄▄ ███▀██▄█ ▄█▀████
████▄▀▀▄██▄██▄▀▄ ▄ ██  ▀  ▀▀▀▀  ▀████
█████▀▀▄  ▄▄  ▀█▄█▄▄▄▄██▄█▄▄ ▀▄█▀████
████ █   █▄  █  ▄ █▄ ▄▀ ▀█▀▀▀▀▄▄▀████
████ █▀█▄█▄█▄█ ███  ▀▄▄▀▄█▀▀▀█▄█▀████
████▄██▄▄▄▄█  ▀ ▄▄▀▄  ▀▀ ▄▄▄ ▄ ▄▀████
████ ▄▄▄▄▄ █▄▀▀█▀█▀▄▀█▀  █▄█ █▄█▀████
████ █   █ █ ▄ ▀▄ ██▀ ▀█ ▄▄▄▄▀ ▀ ████
████ █▄▄▄█ █ ▄ █▀▄▄  █▄█▀▄▄ ▄▄▄ █████
████▄▄▄▄▄▄▄█▄██▄█▄▄▄█▄█▄███▄██▄██████
█████████████████████████████████████
█████████████████████████████████████
```

**Remove existing client**
```shell
cd /opt/outline/bin/
sudo ./outline-ss-clients remove client-id
```
Note: Replace `client-id` with correct client id.

## Step 6: Setup Bogus (Fake) Website

SSH into your server.

_nginx_ was installed, previously, in the [Step 2.1: Install OS Packages](#step-21-install-os-packages) section.

create some fake website content

Note: For simplicity we are creating a very basic "Hello, World!" index file but
      it is better to create a proper-looking, albeit fake, website.

add fake website content:

create directory:
```shell
sudo mkdir -p /var/www/fake-website.com
```

edit or create this file: `/var/www/fake-website.com/index.html`
```shell
sudo nano /var/www/fake-website.com/index.html
```
place this into the file:
```text
Hello, World!
```

if you have proper website content then place it in this directory:
`/var/www/fake-website.com`

configure the website to be served by nginx web server:

create this file: `/etc/nginx/sites-available/fake-website.com.conf`
```shell
sudo nano /etc/nginx/sites-available/fake-website.com.conf
```
place this into the file:
```text
server {
  server_name fake-website.com;

  listen 80;
  listen [::]:80;

  root  /var/www/fake-website.com;
  index index.html;

  location / {
    try_files $uri $uri/ =404;
  }
}
```

enable the newly created website in nginx:
```shell
cd /etc/nginx/sites-enabled/
sudo ln -s ../sites-available/fake-website.com.conf fake-website.com.conf
```

get a free HTTPs (TLS/SSL) certificate via certbot:

certbot was installed, previously, in the [Step 2.1: Install OS Packages](#step-21-install-os-packages) section

run certbot for nginx to get a certificate that is automatically renewed:  
```shell
sudo certbot --nginx --agree-tos
```
follow the instructions in the terminal to complete the certificate request

verify the certbot auto-renewal service is running:
```shell
sudo systemctl status certbot.timer
```

finalize the website configuration in nginx:

create this file: `/etc/nginx/sites-available/fake-website.com.conf`
```shell
sudo nano /etc/nginx/sites-available/fake-website.com.conf
```
place this into the file:
```text
upstream outline-ss-server {
  # this port must match Outline Shadowsocks server config
  server localhost:4444;
}

server {
  server_name fake-website.com;

  listen [::]:443 ssl ipv6only=on;
  listen 443 ssl;

  ssl_certificate     /etc/letsencrypt/live/fake-website.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/fake-website.com/privkey.pem;
  include             /etc/letsencrypt/options-ssl-nginx.conf;
  ssl_dhparam         /etc/letsencrypt/ssl-dhparams.pem;

  root  /var/www/fake-website.com;
  index index.html;

  location / {
    try_files $uri $uri/ =404;
  }

  # this path must match Outline Shadowsocks server config
  # for listener of type "websocket-stream"
  location /9d4cd779f1c7c31867dc/tcp {
    proxy_pass http://outline-ss-server;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
  }

  # this path must match Outline Shadowsocks server config
  # for listener of type "websocket-packet"
  location /9d4cd779f1c7c31867dc/udp {
    proxy_pass http://outline-ss-server;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
  }
}

server {
  server_name fake-website.com;

  listen 80;
  listen [::]:80;

  if ($host = fake-website.com) {
    return 301 https://$host$request_uri;
  }

  return 404;
}
```

Note: if you changed the Outline Shadowsock server port to something other than
      `4444` then make sure to update the port in this config file (see commented sections) 

Note: if you changed the Outline Shadowsock server listeners paths to something
      new then make sure it matches in this config file (see commented sections)

create a symlink for the Outline client configs:
```shell
sudo ln -s /opt/outline/config/clients /var/www/fake-website.com/clients
```

Reboot server:
```shell
sudo reboot
```

after the server finishes rebooting, ensure all services are running correctly:
```shell
sudo systemctl status
```

verify your website is reachable:

in a browser, go to: http://fake-website.com/

the browser should have been redirected from HTTP to HTTPs: https://fake-website.com/ 

verify that you can see your website:

if you used the simple "Hello, World!" setup then that is what you should
see in the browser

Note: Replace `fake-website.com` in all of the above with the domain name that
      you purchased.

## Step 7: Managing Outline Shadowsocks Clients

In general, when you open an Outline client app, it asks you for an access key.
Access keys must be entered in this format:

`ssconf://fake-website.com/clients/client-id.yaml`
Note: Replace `client-id` with correct client id.

If you want to avoid using this tedious URL then you can use a QR code instead,
using the Outline Client manager script (above).

Note: Replace `fake-website.com` in all of the above with the domain name that
you purchased.

## Step 8: _[optional]_ Configure Scheduled Server Restart

- SSH into your machine
  > ℹ️ **Note:**
    in this document, the commands listed assume you are using a non-_root_ user
    on the system that has _sudo_ privileges

- it is good practice to reboot your server at least once a week to give it
  refresh

- setup a scheduled task in crontab
  ```shell
  crontab -e
  ```
  place this into the file:
  ```text
  # m h  dom mon dow   command
    0 2  *   *   0     sudo reboot
  ```
  in this cron schedule the server will reboot every Sunday at 02:00
