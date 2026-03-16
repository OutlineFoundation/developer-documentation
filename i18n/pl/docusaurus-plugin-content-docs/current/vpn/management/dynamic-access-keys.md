---
title: "Dynamic Access Keys"
sidebar_label: "Dynamic Access Keys"
---

W Outline dostępne są 2 rodzaje kluczy dostępu: statyczne i dynamiczne. Klucze statyczne kodują wszystkie informacje dotyczące połączania wewnątrz samego klucza, natomiast klucze dynamiczne kodują lokalizację informacji dotyczących połączenia, dzięki czemu możesz przechowywać je zdalnie i zmieniać, gdy zajdzie taka potrzeba. Oznacza to, że możesz aktualizować konfigurację swojego serwera bez konieczności generowania nowych kluczy i przekazywania ich użytkownikom. Z tego dokumentu dowiesz się, jak korzystać z dynamicznych kluczy dostępu, aby zwiększyć elastyczność i wydajność zarządzania serwerem Outline.

Istnieją 3 sposoby na określenie informacji dostępowych, które będą wykorzystywane przez Twoje dynamiczne klucze dostępu:

### Korzystanie z linku `ss://` {#use_an_ss_link}

*Klient Outline – wersja 1.8.1+.*

Możesz skorzystać bezpośrednio z istniejącego linku `ss://`. Ta metoda jest optymalna, jeśli nie musisz często zmieniać serwera, portu ani metody szyfrowania, ale mimo to zależy Ci na elastyczności w zakresie aktualizowania adresu serwera.

**Przykład:**

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

### Korzystanie z obiektu JSON {#use_a_json_object}

*Klient Outline – wersja 1.8.0+.*

Ta metoda zapewnia większą elastyczność w zakresie zarządzania wszystkimi aspektami połączeń Outline użytkowników. Możesz w ten sposób aktualizować serwer, port, hasło i metodę szyfrowania.

**Przykład:**

```json
{
  "server": "outline-server.example.com",
  "server_port": 8388,
  "password": "example",
  "method": "chacha20-ietf-poly1305"
}
```

- **server**: domena lub adres IP Twojego serwera VPN;

- **server_port**: numer portu, na którym uruchomiony jest Twój serwer VPN;

- **password**: hasło wymagane do połączenia z usługą VPN;

- **method**: metoda szyfrowania używana przez usługę VPN. Zapoznaj się z [algorytmami AEAD](https://shadowsocks.org/doc/aead.html) obsługiwanymi przez Shadowsocks.

### Korzystanie z obiektu YAML {#use_a_yaml_object}

*Klient Outline – wersja 1.15.0+.*

Te metoda jest podobna do poprzedniej metody JSON, ale zapewnia większą elastyczność dzięki wykorzystaniu zaawansowanego formatu konfiguracji Outline. Możesz aktualizować serwer, port, hasło i metodę szyfrowania oraz wykonywać wiele innych czynności.

**Przykład:**

```yaml
transport:
  $type: tcpudp
  tcp:
    $type: shadowsocks
    endpoint: outline-server.example.com:8388
    cipher: chacha20-ietf-poly1305
    secret: example
  udp:
    $type: shadowsocks
    endpoint: outline-server.example.com:8388
    cipher: chacha20-ietf-poly1305
    secret: example
```

- **transport**: definiuje protokoły transportowe, które będą używane (w tym przypadku TCP i UDP);

- **tcp/udp**: określa konfigurację dla każdego protokołu;

    - **$type**: określa rodzaj konfiguracji, w tym przypadku jest to shadowsocks;

    - **endpoint**: domena lub adres IP i port Twojego serwera VPN;

    - **secret**: hasło wymagane do połączenie z usługą VPN;

    - **cipher**: metoda szyfrowania używana przez usługę VPN. Zapoznaj się z [algorytmami AEAD](https://shadowsocks.org/doc/aead.html) obsługiwanymi przez Shadowsocks.

W [Konfiguracji klucza dostępu](config) znajdziesz szczegółowe informacje dotyczące wszystkich sposobów konfigurowania dostępu do serwera Outline, w tym o transportach, punktach końcowych, dialerach i odbiorcach pakietów.

## Pobieranie informacji dostępowych z klucza statycznego {#extract_access_information_from_a_static_key}

Jeśli masz istniejący statyczny klucz dostępu, możesz pobrać informacje, aby utworzyć dynamiczny klucz dostępu w formacie JSON lub YAML. Statyczne klucze dostępu mają następujący wzór:

```none
SS-URI = "ss://" userinfo "@" hostname ":" port [ "/" ] [ "#" tag ]
userinfo = websafe-base64-encode-utf8(method  ":" password)
           method ":" password
```

Przykład:

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

- **Serwer:** `outline-server.example.com`

- **Port serwera:** `8388`

- **Informacje o użytkowniku:** `Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl` dekodowane jako [base64](https://en.wikipedia.org/wiki/Base64) za pomocą narzędzia, takiego jak [kodowanie/dekodowanie narzędzi administracyjnych Google](https://toolbox.googleapps.com/apps/encode_decode/)

    - **Metoda**: `chacha20-ietf-poly1305`

    - **Hasło**: `example`

## Wybór platformy hostingowej {#choose_a_hosting_platform}

Gdy wiesz już, jak tworzyć dynamiczne klucze dostępu, ważne, aby wybrać odpowiednią platformę hostingową dla swojej konfiguracji klucza dostępu. Przy podejmowaniu decyzji weź pod uwagę czynniki, takie jak niezawodność, bezpieczeństwo, łatwość użycia i odporność na cenzurę platformy. Czy platforma będzie stabilnie wyświetlać informacje o kluczu dostępu bez przestojów? Czy zapewnia odpowiednie środki bezpieczeństwa, aby chronić Twoją konfigurację? Jak łatwe jest zarządzanie informacjami o kluczu dostępu na platformie? Czy platforma jest dostępna w regionach z cenzurą internetu?

W przypadku sytuacji ograniczonego dostępu do informacji zastanów się nad hostingiem na platformach odpornych na cenzurę, takich jak [Dysk Google](https://drive.google.com), [pad.riseup.net](https://pad.riseup.net/), [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html) (z dostępem za pomocą ścieżek), [Netlify](https://dev.to/alexmercedcoder/delivering-json-data-with-netlify-1j96) lub [tajne gisty GitHub](https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists/creating-gists).
Oceń określone potrzeby swojego wdrożenia i wybierz platformę, która spełnia Twoje wymagania dotyczące dostępności i bezpieczeństwa.
