---
title: "Maskowanie przy użyciu prefiksów połączenia"
sidebar_label: "Maskowanie przy użyciu prefiksów połączenia"
---

Od wersji 1.9.0 klienta Outline klucze dostępu obsługują opcję „prefiks”. „Prefiks” to lista bajtów wykorzystywanych jako pierwsze bajty [ciągu zaburzającego](https://shadowsocks.org/guide/aead.html) połączenia Shadowsocks TCP.
Może on sprawić, że połączenie będzie wyglądać jak protokół, który jest dozwolony w sieci, co pozwoli obejść zapory sieciowe odrzucające nierozpoznane protokoły.

## Kiedy warto tego spróbować? {#when_should_i_try_this}

Jeśli podejrzewasz, że użytkownicy Twojego wdrożenia Outline są wciąż blokowani, rozważ wypróbowanie kilku różnych prefiksów.

## Instrukcje {#instructions}

Długość prefiksu nie powinna przekraczać 16 bajtów. Dłuższe prefiksy mogą powodować konflikty ciągów zaburzających, co może zmniejszyć bezpieczeństwo szyfrowania i doprowadzić do wykrycia połączeń. Do ominięcia blokad należy użyć możliwie najkrótszego prefiksu.

Używany port powinien być zgodny z protokołem, pod który podszywa się prefiks.
Organizacja IANA prowadzi [rejestr numerów portów protokołów transportowych](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml), który mapuje protokoły i numery portów.

Niektóre przykładowe skuteczne prefiksy wyglądają jak typowe protokoły:

Zalecany port
Zakodowany w formacie JSON
Zakodowany w formacie adresu URL

Żądanie HTTP
80 (HTTP)
`"POST "`
`POST%20`

Odpowiedź HTTP
80 (HTTP)
`"HTTP/1.1 "`
`HTTP%2F1.1%20`

Żądanie DNS przez TCP
53 (DNS)
`"\u0005\u00DC\u005F\u00E0\u0001\u0020"`
`%05%C3%9C_%C3%A0%01%20`

ClientHello protokołu TLS
443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps – dane), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (APN firmy Apple), 5228 (Sklep Play), 5349 (protokoły turn)
`"\u0016\u0003\u0001\u0000\u00a8\u0001\u0001"`
`%16%03%01%00%C2%A8%01%01`

Dane aplikacji TLS
443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps – dane), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (APN firmy Apple), 5228 (Sklep Play), 5349 (protokoły turn)
`"\u0013\u0003\u0003\u003F"`
`%13%03%03%3F`

ServerHello protokołu TLS
443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps – dane), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (APN firmy Apple), 5228 (Sklep Play), 5349 (protokoły turn)
`"\u0016\u0003\u0003\u0040\u0000\u0002"`
`%16%03%03%40%00%02`

SSH
22 (ssh), 830 (netconf-ssh), 4334 (netconf-ch-ssh), 5162 (snmpssh-trap)
`"SSH-2.0\r\n"`
`SSH-2.0%0D%0A`

### Dynamiczne klucze dostępu {#dynamic_access_keys}

Żeby używać funkcji prefiksu z [dynamicznymi kluczami dostępu](../management/dynamic-access-keys) (`ssconf://`), dodaj klucz „prefiksu” do obiektu JSON z wartością **zakodowaną w formacie JSON**, która reprezentuje wybrany prefiks (zobacz przykłady w tabeli powyżej). Możesz użyć kodów modyfikacji (takich jak \u00FF), żeby reprezentować niedrukowalne punkty kodowe Unicode w przedziale od `U+0` do `U+FF`, na przykład:

```json
{
    "server": "example.com",
    "server_port": 8388,
    "password": "example",
    "method": "chacha20-ietf-poly1305",
    "prefix": "\u0005\u00DC\u005F\u00E0\u0001\u0020"
}
```

### Statyczne klucze dostępu {#static_access_keys}

Żeby użyć prefiksów ze **statycznymi kluczami dostępu** (ss://), musisz zmodyfikować istniejący klucz przed jego rozpowszechnieniem. Jeśli masz statyczny klucz dostępu wygenerowany przez Menedżera Outline, uzyskaj wersję prefiksu **zakodowaną w formacie adresu URL** (zobacz przykłady w tabeli powyżej) i dodaj ją na końcu klucza dostępu w ten sposób:

`ss://Z34nthataITHiTNIHTohithITHbVBqQ1o3bkk@127.0.0.1:33142/?outline=1&prefix=<your url-encoded prefix goes here>`

Zaawansowani użytkownicy mogą przekonwertować prefiks **zakodowany w formacie JSON** na **zakodowany w formacie adresu URL** przy użyciu funkcji `encodeURIComponent()` przeglądarki. W tym celu należy otworzyć konsolę do badania sieci (*Deweloper > Konsola sieciowa w Javascripcie *w Chrome) i wpisać:

```js
encodeURIComponent("<your json-encoded prefix goes here>")
```

Naciśnij Enter. Wygenerowana zostanie wartość w *wersji *zakodowanej w formacie adresu URL, na przykład:

```js
encodeURIComponent("\u0016\u0003\u0001\u0000\u00a8\u0001\u0001")
'%16%03%01%00%C2%A8%01%01'
```
