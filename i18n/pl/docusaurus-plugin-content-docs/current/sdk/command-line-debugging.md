---
title: "Command Line Debugging"
sidebar_label: "Command Line Debugging"
---

Ten przewodnik pokazuje, jak za pomocą narzędzi wiersza poleceń pakietu SDK Outline zrozumieć i obejść zakłócenia sieciowe z perspektywy zdalnej. Dowiesz się, jak używać narzędzi pakietu SDK do pomiaru zakłóceń w sieci, testowania strategii obchodzenia ograniczeń i analizowania wyników. W tym przewodniku skupimy się na narzędziach `resolve`, `fetch` i `http2transport`.

## Pierwsze kroki z narzędziami Outline SDK

Narzędzi Outline SDK możesz zacząć używać bezpośrednio z wiersza poleceń.

### Rozwiązywanie nazw DNS

Narzędzie `resolve` umożliwia przeprowadzanie wyszukiwań DNS za pomocą określonego resolvera.

Aby rozwiązać rekord A domeny:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type A 1.2.3.4.nip.io
```

Aby rozwiązać rekord CNAME:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type CNAME www.google.com
```

### Pobieranie strony internetowej

Narzędzie `fetch` może służyć do pobierania treści ze strony internetowej.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest https://example.com
```

Może też wymusić użycie protokołu QUIC.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -proto=h3 https://www.youtube.com
```

### Używanie lokalnego serwera proxy

Narzędzie `http2transport` tworzy lokalny serwer proxy, przez który kieruje ruch.
Aby uruchomić lokalny serwer proxy z transportem Shadowsocks:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/http2transport@latest -localAddr 127.0.0.1:8080 -transport "ss://{your_shadowsocks_credentials}"
```

Możesz następnie użyć tego serwera proxy z innymi narzędziami, takimi jak curl:

```sh
curl -p -x http://127.0.0.1:8080 https://ipinfo.io
```

## Określanie strategii omijania

Pakiet SDK Outline umożliwia określanie różnych strategii obchodzenia ograniczeń, które można łączyć, aby omijać różne formy zakłóceń sieci. Specyfikację tych strategii znajdziesz w [dokumentacji Go](https://pkg.go.dev/github.com/OutlineFoundation/outline-sdk/x@v0.0.3/configurl).

### Strategie kompozycyjne

Te strategie można łączyć, aby tworzyć bardziej zaawansowane techniki obchodzenia.

* **DNS-over-HTTPS z fragmentacją TLS**: `doh:name=cloudflare-dns.com&address=cloudflare.net:443 | tlsfrag:1`

* **SOCKS5-over-TLS z maskowaniem domeny:** `tls:sni=decoy.example.com&certname=[HOST] | socks5:[HOST]:[PORT]`

* **Routing wieloskoku z Shadowsocks:** `ss://[USERINFO1]@[HOST1]:[PORT1] | ss://[USERINFO2]@[HOST2]:[PORT2] | ss://[USERINFO3]@[HOST3]:[PORT3]`

## Dostęp zdalny i pomiar

Aby zmierzyć zakłócenia sieci w różnych regionach, możesz użyć zdalnych serwerów proxy. Możesz znaleźć lub utworzyć zdalne serwery proxy, z którymi chcesz się połączyć.

### Opcje dostępu zdalnego

Za pomocą narzędzia `fetch` możesz zdalnie testować połączenia na różne sposoby.

#### Serwer Outline

Połącz się zdalnie ze standardowym serwerem Outline za pomocą transportu Shadowsocks.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "ss://{remote_shadowsocks_credentials}" https://ipinfo.io | jq
```

#### SOCKS5 przez SSH

Utwórz serwer proxy SOCKS5 za pomocą tunelu SSH.

```sh
ssh -D 127.0.0.1:1080 -C -N $USER@$HOST:$PORT
```

Połącz się z tym tunelem za pomocą funkcji fetch.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "socks5://localhost:1080" https://ipinfo.io | jq
```

## Studium przypadku: omijanie blokady YouTube w Iranie

Oto praktyczny przykład wykrywania i omijania zakłóceń sieci.

### Wykrywanie bloku

Podczas próby pobrania strony głównej YouTube za pomocą irańskiego serwera proxy żądanie przekracza limit czasu, co wskazuje na blokadę.

```sh
export TRANSPORT="ss://{remote_shadowsocks_credentials}"
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)" https://www.youtube.com
```

To polecenie kończy się niepowodzeniem z powodu przekroczenia limitu czasu.

### Obejście z fragmentacją TLS

Dodając fragmentację TLS do transportu, możemy obejść tę blokadę.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)|tlsfrag:1" https://www.youtube.com | grep -oe '<title>.*</title>'
```

To polecenie pobiera tytuł strony głównej YouTube, czyli
`<title>YouTube</title>`.

### Omijanie z użyciem fragmentacji TLS i DNS-over-HTTPS

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|tlsfrag:1|doh:name=cloudflare-dns.com&address=www.cloudflare.net" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Zwraca też wartość `<title>YouTube</title>`.

### Omijanie blokad za pomocą serwera Outline

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|ss://<your_shadowsocks_credentials>" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Ten kod też zwraca wartość `<title>YouTube</title>`.

## Dalsza analiza i zasoby

Aby wziąć udział w dyskusji lub zadać pytanie, odwiedź [grupę dyskusyjną dotyczącą pakietu SDK Outline](https://github.com/OutlineFoundation/outline-sdk/discussions).
