---
title: "Przyznawanie dostępu administracyjnego innym użytkownikom"
sidebar_label: "Przyznawanie dostępu administracyjnego innym użytkownikom"
---

Wraz rozwojem usługi Outline konieczne może być przekazanie zadań związanych z zarządzaniem innym zaufanym osobom. W tym dokumencie opisano różne dostępne metody przyznawania dostępu administracyjnego innym menedżerom.

Wybór metody zależy od sposobu początkowego wdrożenia serwera Outline.

## Wdrożenia u dostawców chmury {#cloud_provider_deployments}

W przypadku serwerów Outline wdrożonych na platformach chmurowych takich jak DigitalOcean, AWS, czy Google Cloud uprawnienia do zarządzania są zwykle obsługiwane przez zintegrowane funkcje zarządzania tożsamościami i dostępem (IAM) dostawcy. Takie podejście jest bezpieczniejsze i bardziej kontrolowane w porównaniu z ręcznym udostępnianiem konfiguracji.

### DigitalOcean {#digitalocean}

DigitalOcean udostępnia funkcję **zespołów**, która umożliwia zapraszanie innych użytkowników tej platformy do współpracy nad projektami. Jest to zalecany sposób przyznawania uprawnień do zarządzania serwerem Outline hostowanym przez DigitalOcean.

#### 1. Przyznawanie dostępu zespołowi {#1_grant_team_access}

Najskuteczniejszym sposobem przyznawania dostępu do zarządzania serwerem Outline hostowanym w DigitalOcean jest korzystanie z funkcji **zespołów** na platformie DigitalOcean.

- Zaloguj się na konto DigitalOcean.

- Przejdź do sekcji **Teams** (Zespoły).

- Utwórz nowy zespół lub zaproś innych użytkowników DigitalOcean do istniejącego zespołu.

- Zapraszając osoby, możesz przypisać im określone role i uprawnienia do konkretnych zasobów, takich jak instancje Droplet z uruchomionym serwerem Outline.

#### 2. Kontrolowanie uprawnień {#2_control_permissions}

Starannie rozważ, jakie uprawnienia chcesz przyznać osobom w zespole. W przypadku zarządzania serwerem Outline możesz przyznać im uprawnienia do odczytu i zapisu konkretnej instancji Droplet. Umożliwi im to:

- wyświetlanie szczegółów instancji Droplet (adresu IP, statusu itp.),

- uzyskiwanie dostępu do konsoli Droplet (na potrzeby rozwiązywania problemów),

- potencjalnie wykonywanie czynności takich jak ponowne uruchamianie instancji Droplet (w zależności od przyznanych uprawnień).

Użytkownicy, którzy połączyli aplikację Menedżer Outline ze swoim kontem DigitalOcean, będą mogli wyświetlać wszystkie powiązane z nim serwery Outline oraz nimi zarządzać.

## Instalacja ręczna {#manual_installations}

Jeśli serwer Outline został zainstalowany ręcznie na własnym serwerze za pomocą [skryptu instalacyjnego](../getting-started/server-setup-advanced), podstawowym sposobem przyznania uprawnień do zarządzania jest udostępnienie **konfiguracji dostępu**.

Aplikacja Menedżer Outline wymaga określonego ciągu tekstowego konfiguracji, aby móc łączyć się z serwerem Outline i nim zarządzać. Ten ciąg konfiguracji zawiera wszystkie niezbędne informacje, w tym adres i port serwera oraz klucz tajny na potrzeby uwierzytelniania.

### 1. Znajdowanie pliku `access.txt` {#1_locate_the_accesstxt_file}

Na serwerze, na którym zainstalowano Outline, przejdź do katalogu Outline. Jego dokładna lokalizacja może się nieco różnić w zależności od metody instalacji, ale najczęstsze z nich to:

- `/opt/outline/access.txt`

- `/etc/outline/access.txt`

- Wolumin Dockera używany przez kontener z serwerem Outline.

### 2. Pobieranie konfiguracji dostępu {#2_retrieve_the_access_config}

Po znalezieniu pliku `access.txt` przekonwertuj go na format JSON, którego Menedżer Outline będzie oczekiwać w następnym kroku.

```sh
sed -n '2s/^apiUrl://p; 1s/^certSha256://p' /opt/outline/access.txt | paste -d'\n' -s | sed 'H;1h;$!d;x;s/\n/", \"apiUrl\": \"/g; s/^/{"certSha256": \"/; s/$/\"}/'
```

Dane wyjściowe będą zawierać odcisk cyfrowy podpisanego samodzielnie certyfikatu (`certSha256`) i punkt końcowy interfejsu API zarządzania na serwerze (`apiUrl`):

```json
{"certSha256": "1DCC18CC9F6C34EBBB639255F4D1BC6984C2F6A47B15F7A49AA8AFB69B7E4DDE", "apiUrl": "https://1.1.1.1:12345/Fw-CkWFNSN7Ml8LLM8Pduw"}
```

### 3. Bezpieczne udostępnianie konfiguracji dostępu {#3_share_the_access_config_securely}

Skopiuj dane wyjściowe i bezpiecznie przekaż je nowemu menedżerowi serwera Outline. Nie wysyłaj tych informacji przez niezaszyfrowane kanały, takie jak zwykła poczta e-mail czy komunikator.
Rozważ użycie funkcji bezpiecznego udostępniania w menedżerze haseł lub innej szyfrowanej metody komunikacji.

Wklejenie podanej **konfiguracji dostępu** w aplikacji Menedżer Outline umożliwi nowemu menedżerowi dodanie serwera Outline, a następnie zarządzanie w aplikacji. Dodatkowe informacje na temat korzystania z Menedżera Outline znajdziesz w [Centrum pomocy](https://support.google.com/outline).
