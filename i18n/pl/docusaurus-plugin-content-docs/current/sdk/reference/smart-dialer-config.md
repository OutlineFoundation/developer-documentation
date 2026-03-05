---
title: "Smart Dialer Configuration"
sidebar_label: "Smart Dialer Config"
---

**Inteligentny dialer** wyszukuje strategię, która odblokowuje protokoły DNS i TLS dla podanej listy domen testowych. Wyboru dokonuje na podstawie konfiguracji opisującej wiele strategii.

## Konfiguracja YAML na potrzeby inteligentnego dialera

Inteligentny dialer obsługuje konfigurację w formacie YAML. Oto przykład:

```yaml
dns:
  - system: {}
  - https:
      name: 8.8.8.8
  - https:
      name: 9.9.9.9
tls:
  - ""
  - split:2
  - tlsfrag:1

fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

### Konfiguracja DNS

- Pole `dns` określa listę resolverów DNS do przetestowania.

- Każdy resolver DNS może mieć przypisany jeden z tych typów:

    - `system`: używanie resolvera systemowego. Należy określić pusty obiekt.

    - `https`: używanie szyfrowanego resolvera DNS-over-HTTPS (DoH).

    - `tls`: używanie szyfrowanego resolvera DNS-over-TLS (DoT).

    - `udp`: używanie resolvera UDP.

    - `tcp`: używanie resolvera TCP.

#### Resolver DNS-over-HTTPS (DoH)

```yaml
https:
  name: dns.google
  address: 8.8.8.8
```

- `name`: nazwa domeny serwera DoH.

- `address`: adres serwera DoH w formacie host:port. Domyślna wartość to `name`:443.

#### Resolver DNS-over-TLS (DoT)

```yaml
tls:
  name: dns.google
  address: 8.8.8.8
```

- `name`: nazwa domeny serwera DoT.

- `address`: adres serwera DoT w formacie host:port. Domyślna wartość to `name`:853.

#### Resolver UDP

```yaml
udp:
  address: 8.8.8.8
```

- `address`: adres resolvera UDP w formacie host:port.

#### Resolver TCP

```yaml
tcp:
  address: 8.8.8.8
```

- `address`: adres resolvera TCP w formacie host:port.

### Konfiguracja TLS

- Pole `tls` określa listę transportów TLS do przetestowania.

- Każdy transport TLS jest ciągiem tekstowym określającym transport, który ma być używany.

- Na przykład `override:host=cloudflare.net|tlsfrag:1` określa transport, który używa frontowania domen razem z Cloudflare i fragmentacją TLS. Szczegóły znajdziesz w [dokumentacji konfiguracji](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x/configurl#hdr-Config_Format).

### Konfiguracja zastępcza

Konfiguracja zastępcza jest używana, jeśli żadna ze strategii bez proxy nie umożliwia połączenia. Może ona na przykład obejmować określony zapasowy serwer proxy do obsług prób połączeń użytkownika. Na początku konfiguracja zastępcza może działać wolniej, ponieważ najpierw strategie DNS/TLS muszą zakończyć się niepowodzeniem lub osiągnięciem limitu czasu.

Zastępczymi ciągami tekstowymi powinny być:

- prawidłowy ciąg konfiguracji `StreamDialer` zgodnie z definicją w [`configurl`](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x/configurl#hdr-Proxy_Protocols),

- prawidłowy obiekt konfiguracji Psiphon jako element podrzędny pola `psiphon`.

#### Przykład dotyczący serwera Shadowsocks

```yaml
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

#### Przykład dotyczący serwera SOCKS5

```yaml
fallback:
  - socks5://[USERINFO]@[HOST]:[PORT]
```

#### Przykład konfiguracji Psiphon

Aby móc korzystać z sieci [Psiphon](https://psiphon.ca/):

1. Skontaktuj się z zespołem Psiphon, aby otrzymać konfigurację umożliwiającą dostęp do tej sieci. Może to wymagać zawarcia umowy.

2. Dodaj otrzymaną konfigurację Psiphon do sekcji `fallback` konfiguracji inteligentnego dialera. Ponieważ format JSON jest zgodny z YAML, konfigurację Psiphon możesz skopiować i wkleić bezpośrednio do sekcji `fallback`, tak jak w tym przykładzie:

```yaml
fallback:
  - psiphon: {
      "PropagationChannelId": "FFFFFFFFFFFFFFFF",
      "SponsorId": "FFFFFFFFFFFFFFFF",
      "DisableLocalSocksProxy" : true,
      "DisableLocalHTTPProxy" : true,
      ...
    }
```

### Jak korzystać z inteligentnego dialera

Aby użyć inteligentnego dialera, utwórz obiekt `StrategyFinder` i wywołaj metodę `NewDialer`, przekazując listę domen testowych i konfigurację w formacie YAML.
Metoda `NewDialer` zwróci wartość implementację interfejsu `transport.StreamDialer`, której będzie można użyć do utworzenia połączeń z wykorzystaniem znalezionej strategii. Przykład:

```go
finder := &smart.StrategyFinder{
    TestTimeout:  5 * time.Second,
    LogWriter:   os.Stdout,
    StreamDialer: &transport.TCPDialer{},
    PacketDialer: &transport.UDPDialer{},
}

configBytes := []byte(`
dns:
  - system: {}
  - https:
      name: 8.8.8.8
  - https:
      name: 9.9.9.9
tls:
  - ""
  - split:2
  - tlsfrag:1
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
`)

dialer, err := finder.NewDialer(
  context.Background(),
  []string{"www.google.com"},
  configBytes
)
if err != nil {
    // Handle error.
}

// Use dialer to create connections.
```

Jest to podstawowy przykład, który może wymagać dostosowania do konkretnego przypadku użycia.
