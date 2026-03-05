---
title: "Share Management Access"
sidebar_label: "Share Management Access"
---

Wraz rozwojem usługi Outline konieczne może być przekazanie zadań związanych z zarządzaniem innym zaufanym osobom. W tym dokumencie opisano różne dostępne metody przyznawania dostępu administracyjnego innym menedżerom.

Wybór metody zależy od sposobu początkowego wdrożenia serwera Outline.

## Wdrożenia u dostawców chmury

W przypadku serwerów Outline wdrożonych na platformach chmurowych takich jak DigitalOcean, AWS, czy Google Cloud uprawnienia do zarządzania są zwykle obsługiwane przez zintegrowane funkcje zarządzania tożsamościami i dostępem (IAM) dostawcy. Takie podejście jest bezpieczniejsze i bardziej kontrolowane w porównaniu z ręcznym udostępnianiem konfiguracji.

### DigitalOcean

DigitalOcean udostępnia funkcję **zespołów**, która umożliwia zapraszanie innych użytkowników tej platformy do współpracy nad projektami. Jest to zalecany sposób przyznawania uprawnień do zarządzania serwerem Outline hostowanym przez DigitalOcean.

#### 1. Przyznawanie dostępu zespołowi

Najskuteczniejszym sposobem przyznawania dostępu do zarządzania serwerem Outline hostowanym w DigitalOcean jest korzystanie z funkcji **zespołów** na platformie DigitalOcean.

- Zaloguj się na konto DigitalOcean.

- Przejdź do sekcji **Teams** (Zespoły).

- Utwórz nowy zespół lub zaproś innych użytkowników DigitalOcean do istniejącego zespołu.

- Zapraszając osoby, możesz przypisać im określone role i uprawnienia do konkretnych zasobów, takich jak instancje Droplet z uruchomionym serwerem Outline.

#### 2. Kontrolowanie uprawnień

Starannie rozważ, jakie uprawnienia chcesz przyznać osobom w zespole. W przypadku zarządzania serwerem Outline możesz przyznać im uprawnienia do odczytu i zapisu konkretnej instancji Droplet. Umożliwi im to:

- wyświetlanie szczegółów instancji Droplet (adresu IP, statusu itp.),

- uzyskiwanie dostępu do konsoli Droplet (na potrzeby rozwiązywania problemów),

- potencjalnie wykonywanie czynności takich jak ponowne uruchamianie instancji Droplet (w zależności od przyznanych uprawnień).

Użytkownicy, którzy połączyli aplikację Menedżer Outline ze swoim kontem DigitalOcean, będą mogli wyświetlać wszystkie powiązane z nim serwery Outline oraz nimi zarządzać.

## Instalacja ręczna

Jeśli serwer Outline został zainstalowany ręcznie na własnym serwerze za pomocą [skryptu instalacyjnego](../getting-started/server-setup-advanced), podstawowym sposobem przyznania uprawnień do zarządzania jest udostępnienie **konfiguracji dostępu**.

Aplikacja Menedżer Outline wymaga określonego ciągu tekstowego konfiguracji, aby móc łączyć się z serwerem Outline i nim zarządzać. Ten ciąg konfiguracji zawiera wszystkie niezbędne informacje, w tym adres i port serwera oraz klucz tajny na potrzeby uwierzytelniania.

### 1. Znajdowanie pliku `access.txt`

Na serwerze, na którym zainstalowano Outline, przejdź do katalogu Outline. Jego dokładna lokalizacja może się nieco różnić w zależności od metody instalacji, ale najczęstsze z nich to:

- `/opt/outline/access.txt`

- `/etc/outline/access.txt`

- Wolumin Dockera używany przez kontener z serwerem Outline.

### 2. Pobieranie konfiguracji dostępu

Po znalezieniu pliku `access.txt` przekonwertuj go na format JSON, którego Menedżer Outline będzie oczekiwać w następnym kroku.

Dane wyjściowe będą zawierać odcisk cyfrowy podpisanego samodzielnie certyfikatu (`certSha256`) i punkt końcowy interfejsu API zarządzania na serwerze (`apiUrl`):

### 3. Bezpieczne udostępnianie konfiguracji dostępu

Skopiuj dane wyjściowe i bezpiecznie przekaż je nowemu menedżerowi serwera Outline. Nie wysyłaj tych informacji przez niezaszyfrowane kanały, takie jak zwykła poczta e-mail czy komunikator.
Rozważ użycie funkcji bezpiecznego udostępniania w menedżerze haseł lub innej szyfrowanej metody komunikacji.

Wklejenie podanej **konfiguracji dostępu** w aplikacji Menedżer Outline umożliwi nowemu menedżerowi dodanie serwera Outline, a następnie zarządzanie w aplikacji. Dodatkowe informacje na temat korzystania z Menedżera Outline znajdziesz w [Centrum pomocy](https://support.google.com/outline).
