---
title: "Concepts"
sidebar_label: "Concepts"
---

Outline pomaga użytkownikom ominąć ograniczenia w otwartym dostępie do internetu. Oto kilka najważniejszych pojęć, które pomogą zrozumieć, jak to działa:

## Usługodawcy i użytkownicy {#service_providers_and_end_users}

System Outline obejmuje 2 główne role: **usługodawców**, którzy zarządzają serwerami, i **użytkowników**, którzy za pomocą tych serwerów uzyskują dostęp do internetu.

- **Usługodawcy** tworzą serwery Outline, generują **klucze dostępu** i **rozdają klucze** użytkownikom. Jednym ze sposobów, aby to zrobić, jest skorzystanie z aplikacji **Menedżer Outline**.

- **Użytkownicy** instalują aplikację **klient Outline**, wklejają otrzymany **klucz dostępu** i **łączą się** z bezpiecznym tunelem

## Klucze dostępu {#access-keys}

Klucze dostępu to dane uwierzytelniające, które umożliwiają użytkownikom łączenie się z serwerem Outline. Zawierają informacje potrzebne klientowi Outline do utworzenia bezpiecznego połączenia. Istnieją 2 rodzaje kluczy dostępu:

- **Statyczne klucze dostępu** kodują wszystkie informacje o serwerze potrzebne do połączenia (adres serwera, port, hasło, metodę szyfrowania), zapobiegając modyfikacji danych potrzebnych do uzyskania dostępu Użytkownicy wklejają ten klucz do klienta Outline

Przykład:

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTo1UkVmeFRqbHR6Mkw@outline-server.example.com:17178/?outline=1
```

- **Dynamiczne klucze dostępu** umożliwiają usługodawcy zdalne przechowywanie danych potrzebnych do uzyskania dostępu do serwera. Dzięki temu usługodawcy mogą aktualizować konfigurację serwera (adres serwera, port, hasła, metoda szyfrowania) bez konieczności ponownego przekazywania użytkownikom nowych kluczy dostępu. Szczegółowe informacje znajdziesz w dokumentacji dotyczącej [dynamicznych kluczy dostępu](vpn/management/dynamic-access-keys).
