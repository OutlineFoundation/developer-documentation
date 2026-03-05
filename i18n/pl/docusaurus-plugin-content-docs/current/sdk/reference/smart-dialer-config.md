---
title: "Smart Dialer Configuration"
sidebar_label: "Smart Dialer Config"
---

**Inteligentny dialer** wyszukuje strategię, która odblokowuje protokoły DNS i TLS dla podanej listy domen testowych. Wyboru dokonuje na podstawie konfiguracji opisującej wiele strategii.

## Konfiguracja YAML na potrzeby inteligentnego dialera

Inteligentny dialer obsługuje konfigurację w formacie YAML. Oto przykład:

### Konfiguracja DNS

- Pole `dns` określa listę resolverów DNS do przetestowania.

- Każdy resolver DNS może mieć przypisany jeden z tych typów:

    - `system`: używanie resolvera systemowego. Należy określić pusty obiekt.

    - `https`: używanie szyfrowanego resolvera DNS-over-HTTPS (DoH).

    - `tls`: używanie szyfrowanego resolvera DNS-over-TLS (DoT).

    - `udp`: używanie resolvera UDP.

    - `tcp`: używanie resolvera TCP.

#### Resolver DNS-over-HTTPS (DoH)

- `name`: nazwa domeny serwera DoH.

- `address`: adres serwera DoH w formacie host:port. Domyślna wartość to `name`:443.

#### Resolver DNS-over-TLS (DoT)

- `name`: nazwa domeny serwera DoT.

- `address`: adres serwera DoT w formacie host:port. Domyślna wartość to `name`:853.

#### Resolver UDP

- `address`: adres resolvera UDP w formacie host:port.

#### Resolver TCP

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

#### Przykład dotyczący serwera SOCKS5

#### Przykład konfiguracji Psiphon

Aby móc korzystać z sieci [Psiphon](https://psiphon.ca/):

1. Skontaktuj się z zespołem Psiphon, aby otrzymać konfigurację umożliwiającą dostęp do tej sieci. Może to wymagać zawarcia umowy.

2. Dodaj otrzymaną konfigurację Psiphon do sekcji `fallback` konfiguracji inteligentnego dialera. Ponieważ format JSON jest zgodny z YAML, konfigurację Psiphon możesz skopiować i wkleić bezpośrednio do sekcji `fallback`, tak jak w tym przykładzie:

### Jak korzystać z inteligentnego dialera

Aby użyć inteligentnego dialera, utwórz obiekt `StrategyFinder` i wywołaj metodę `NewDialer`, przekazując listę domen testowych i konfigurację w formacie YAML.
Metoda `NewDialer` zwróci wartość implementację interfejsu `transport.StreamDialer`, której będzie można użyć do utworzenia połączeń z wykorzystaniem znalezionej strategii. Przykład:

Jest to podstawowy przykład, który może wymagać dostosowania do konkretnego przypadku użycia.
