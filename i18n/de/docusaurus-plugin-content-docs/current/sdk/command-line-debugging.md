---
title: "Netzwerkstörungen mit dem Outline SDK aus der Ferne charakterisieren und umgehen"
sidebar_label: "Netzwerkstörungen mit dem Outline SDK aus der Ferne charakterisieren und umgehen"
---

In dieser Anleitung wird gezeigt, wie Sie mit den Befehlszeilentools des Outline SDK Netzwerkstörungen aus der Ferne erkennen und umgehen können. Sie erfahren, wie Sie mit den Tools des SDK Netzwerkstörungen messen, Umgehungsstrategien testen und die Ergebnisse analysieren. In diesem Leitfaden geht es hauptsächlich um die Tools `resolve`, `fetch` und `http2transport`.

## Erste Schritte mit den Outline SDK-Tools

Sie können die Outline SDK-Tools direkt über die Befehlszeile verwenden.

### DNS auflösen

Mit dem Tool `resolve` können Sie DNS-Lookups mit einem bestimmten Resolver durchführen.

So lösen Sie den A-Eintrag einer Domain auf:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type A 1.2.3.4.nip.io
```

So lösen Sie einen CNAME-Eintrag auf:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type CNAME www.google.com
```

### Webseite abrufen

Mit dem Tool `fetch` können Sie den Inhalt einer Webseite abrufen.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest https://example.com
```

Außerdem kann die Verbindung so erzwungen werden, QUIC zu verwenden.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -proto=h3 https://www.youtube.com
```

### Lokalen Proxy verwenden

Das `http2transport`-Tool erstellt einen lokalen Proxy, über den Ihr Traffic geleitet wird.
So starten Sie einen lokalen Proxy mit einem Shadowsocks-Transport:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/http2transport@latest -localAddr 127.0.0.1:8080 -transport "ss://{your_shadowsocks_credentials}"
```

Sie können diesen Proxy dann mit anderen Tools wie curl verwenden:

```sh
curl -p -x http://127.0.0.1:8080 https://ipinfo.io
```

## Strategien zur Umgehung angeben

Mit dem Outline SDK können verschiedene Umgehungsstrategien angegeben werden, die kombiniert werden können, um verschiedene Formen von Netzwerkstörungen zu umgehen. Die Spezifikation für diese Strategien finden Sie in der [Go-Dokumentation](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl).

### Zusammensetzbare Strategien

Diese Strategien können kombiniert werden, um robustere Umgehungstechniken zu entwickeln.

* **DNS-over-HTTPS mit TLS-Fragmentierung**: `doh:name=cloudflare-dns.com&address=cloudflare.net:443 | tlsfrag:1`

* **SOCKS5-over-TLS mit Domain Fronting**: `tls:sni=decoy.example.com&certname=[HOST] | socks5:[HOST]:[PORT]`

* **Multi-Hop-Routing mit Shadowsocks**: `ss://[USERINFO1]@[HOST1]:[PORT1] | ss://[USERINFO2]@[HOST2]:[PORT2] | ss://[USERINFO3]@[HOST3]:[PORT3]`

## Remotezugriff und ‑messung

Mit Remote-Proxys können Sie Netzwerkstörungen in verschiedenen Regionen messen. Sie können Remote-Proxys finden oder erstellen, um eine Verbindung herzustellen.

### Optionen für den Remote-Zugriff

Mit dem Tool `fetch` können Sie Verbindungen auf verschiedene Arten remote testen.

#### Outline-Server

Stellen Sie eine Remote-Verbindung zu einem Standard-Outline-Server mit einem Shadowsocks-Transport her.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "ss://{remote_shadowsocks_credentials}" https://ipinfo.io | jq
```

#### SOCKS5 über SSH

Erstellen Sie einen SOCKS5-Proxy über einen SSH-Tunnel.

```sh
ssh -D 127.0.0.1:1080 -C -N $USER@$HOST:$PORT
```

Verbindung zu diesem Tunnel mit „fetch“ herstellen

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "socks5://localhost:1080" https://ipinfo.io | jq
```

## Fallstudie: YouTube-Sperrung im Iran umgehen

Hier ist ein praktisches Beispiel für das Erkennen und Umgehen von Netzwerkstörungen.

### Blockierung erkennen

Wenn versucht wird, die YouTube-Startseite über einen iranischen Proxy abzurufen, tritt ein Zeitüberschreitungsfehler auf, was auf eine Blockierung hindeutet.

```sh
export TRANSPORT="ss://{remote_shadowsocks_credentials}"
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)" https://www.youtube.com
```

Dieser Befehl schlägt mit einem Zeitüberschreitungsfehler fehl.

### Umgehen mit TLS-Fragmentierung

Durch Hinzufügen der TLS-Fragmentierung zur Übertragung können wir diese Blockierung umgehen.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)|tlsfrag:1" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Mit diesem Befehl wird der Titel der YouTube-Startseite abgerufen, nämlich `<title>YouTube</title>`.

### Umgehen mit TLS-Fragmentierung und DNS-over-HTTPS

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|tlsfrag:1|doh:name=cloudflare-dns.com&address=www.cloudflare.net" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Dadurch wird auch `<title>YouTube</title>` zurückgegeben.

### Umgehen mit einem Outline-Server

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|ss://<your_shadowsocks_credentials>" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Auch hier wird `<title>YouTube</title>` zurückgegeben.

## Weitere Analysen und Ressourcen

Wenn Sie sich mit anderen Nutzern austauschen oder Fragen stellen möchten, besuchen Sie das [Outline SDK-Forum](https://github.com/OutlineFoundation/outline-sdk/discussions).
