---
title: "Deploy with Automatic HTTPS Using Caddy"
sidebar_label: "HTTPS with Caddy"
---

In diesem Leitfaden erfahren Sie, wie Sie mit [Caddy](https://caddyserver.com/), einem leistungsstarken und nutzerfreundlichen Webserver, Ihre Outline-Serverkonfiguration optimieren. Dank [automatischem HTTPS](https://caddyserver.com/docs/automatic-https) und flexiblen Konfigurationsmöglichkeiten ist Caddy eine sehr gute Wahl für Ihren Outline-Server, insbesondere, wenn Sie das WebSocket-Übertragungsprotokoll verwenden.

## Was ist Caddy? {#what_is_caddy}

Caddy ist ein Open-Source-Webserver, der für seine Nutzerfreundlichkeit, die automatische Umleitung auf HTTPS („Automatisches HTTPS“) und die Unterstützung verschiedener Protokolle bekannt ist. Er vereinfacht die Webserver-Konfiguration und bietet Funktionen wie:

- **Automatisches HTTPS:** Caddy erhält und erneuert TLS-Zertifikate automatisch und sorgt so für sichere Verbindungen.

- **Unterstützung von HTTP/3:** Caddy unterstützt das neueste HTTP/3-Protokoll für schnelleren und effizienteren Web-Traffic.

- **Plug‑ins:** Caddy lässt sich mit Plug‑ins um verschiedene Funktionen erweitern, darunter Reverse-Proxyvorgänge und Load Balancing.

## Schritt 1: Voraussetzungen {#step_1_prerequisites}

- Laden Sie [`xcaddy`](https://github.com/caddyserver/xcaddy) herunter und führen Sie die Installation durch.

## Schritt 2: Domain konfigurieren {#step_2_configure_your_domain}

Bevor Sie Caddy starten, vergewissern Sie sich, dass Ihr Domainname richtig konfiguriert ist und auf die IP‑Adresse Ihres Servers verweist.

- **A‑/AAAA-Einträge festlegen:** Melden Sie sich bei Ihrem DNS-Anbieter an und legen Sie die A‑ und AAAA-Einträge für Ihre Domain so fest, dass sie jeweils auf die IPv4- bzw. auf die IPv6-Adressen Ihres Servers verweisen.

- **DNS-Einträge prüfen:** Prüfen Sie, ob die DNS-Einträge für die maßgebliche Domain festgelegt sind:

```sh
curl "https://cloudflare-dns.com/dns-query?name=<DOMAIN_NAME>&type=A" \
  -H "accept: application/dns-json"
```

## Schritt 3: Benutzerdefinierten Caddy-Build erstellen und ausführen {#build-and-run}

Mit `xcaddy` können Sie ein benutzerdefiniertes `caddy`-Binärprogramm erstellen, das das Kernmodul des Outline-Servers sowie weitere benötigte Server-Erweiterungsmodule enthält.

```sh
xcaddy build \
  # The example uses a YAML config, so include a YAML config adapter module.
  --with github.com/iamd3vil/caddy_yaml_adapter \
  # The Outline core server module.
  --with github.com/OutlineFoundation/outline-ss-server/outlinecaddy
```

## Schritt 4: Caddy-Server konfigurieren und mit Outline ausführen {#step_4_configure_and_run_the_caddy_server_with_outline}

Erstellen Sie eine neue `config.yaml`-Datei mit der folgenden Konfiguration:

```yaml
apps:
  http:
    servers:
      server1:
        listen:
          - ":443"
        routes:
          - match:
            - host:
              - <DOMAIN_NAME>
            - path:
              - /<TCP_PATH>
            handle:
            - handler: websocket2layer4
              type: stream
              connection_handler: ss1
          - match:
            - host:
              - <DOMAIN_NAME>
            - path:
              - /<UDP_PATH>
            handle:
              - handler: websocket2layer4
                type: packet
                connection_handler: ss1
  outline:
    shadowsocks:
      replay_history: 10000
    connection_handlers:
      - name: ss1
        handle:
          handler: shadowsocks
          keys:
            - id: user-1
              cipher: chacha20-ietf-poly1305
              secret: <SHADOWSOCKS_SECRET>
```

Diese Konfiguration stellt eine Shadowsocks‑over-WebSockets-Strategie dar, mit einem Webserver, der Port `443` überwacht und getarnten Shadowsocks-Traffic über TCP und UDP auf den Pfaden `TCP_PATH` und `UDP_PATH` akzeptiert.

Führen Sie den Caddy-Server mit Outline als Erweiterung mit der erstellten Konfiguration aus:

```sh
caddy run --config config.yaml --adapter yaml --watch
```

Weitere Beispielkonfigurationen [finden Sie hier](https://github.com/OutlineFoundation/outline-ss-server/tree/master/outlinecaddy/examples).

## Schritt 5: Dynamischen Zugriffsschlüssel erstellen {#step_5_create_a_dynamic_access_key}

Generieren Sie eine YAML-Datei mit dem Client-Zugriffsschlüssel für Ihre Nutzer. Verwenden Sie dazu das Format für die [erweiterte Konfiguration](../management/config) und die WebSocket-Endpunkte, die Sie zuvor auf Serverseite konfiguriert haben:

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN_NAME>/<TCP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>

  udp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN_NAME>/<UDP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>
```

Nachdem Sie die YAML-Datei mit dem dynamischen Zugriffsschlüssel erstellt haben, müssen Sie diese Ihren Nutzern zukommen lassen. Sie können die Datei auf einem statischen Webhosting-Dienst hosten oder dynamisch generieren. Weitere Informationen zur Verwendung von [dynamischen Zugriffsschlüsseln](../management/dynamic-access-keys)

## Schritt 6: Mit dem Outline-Client verbinden {#step_6_connect_with_the_outline_client}

Fügen Sie in einer der offiziellen [Outline-Client](../../download-links)-Anwendungen (ab Version 1.15.0) den gerade erstellten dynamischen Zugriffsschlüssel für den Server hinzu. Klicken Sie auf **Verbinden**, um mit der Shadowsocks‑over-WebSocket-Konfiguration eine Tunnelverbindung zu Ihrem Server herzustellen.

Vergewissern Sie sich mit einem Tool wie [IPInfo](https://ipinfo.io), dass Sie über Ihren Outline-Server mit dem Internet verbunden sind.
