---
title: "Konfigurowanie odpornego na blokowanie serwera z pływającymi adresami IP"
sidebar_label: "Konfigurowanie odpornego na blokowanie serwera z pływającymi adresami IP"
---

## Wstęp {#introduction}

Czasami serwery Outline są wykrywane i nakładane są na nie blokady uniemożliwiające dostęp do intensywnie cenzurowanych sieci. Jeśli jednak zablokowany serwer został prawidłowy skonfigurowany, można go dosyć łatwo odzyskać. Zrobimy to przy użyciu DNS – technologii internetowej, która służy do zmieniania nazw domen (na przykład `getoutline.org`) na fizyczne adresy IP (takie jak `216.239.36.21`), oraz pływających adresów IP – funkcji chmurowej, która pozwala przypisać do serwera Outline więcej niż 1 adres IP.

## Wymagania {#requirements}

Do wykonania czynności opisanych w tym przewodniku wymagany jest pewien (niewysoki) poziom umiejętności technicznych. Znajomość podstaw DNS może być pomocna, ale nie jest konieczna. Wstępne informacje znajdziesz w przewodniku [MDN](https://developer.mozilla.org/docs/Learn/Common_questions/What_is_a_domain_name) dotyczącym nazw domen.

Jako konkretnego przykładu użyjemy DigitalOcean i Google Domains, ale możesz równie dobrze skorzystać z usług każdego dostawcy chmury, który umożliwia przypisywanie adresów IP (np. Google Cloud lub [AWS Lightsail](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/lightsail-create-static-ip)), i dowolnego rejestratora domen (takiego jak [AWS Route 53](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-using-route-53-to-point-a-domain-to-an-instance)).

## Instrukcje {#instructions}

1. Lista poniżej zawiera podsumowanie kroków potrzebnych do przeprowadzenia rotacji adresów IP serwera:

2. Kup nazwę domeny.

3. Skieruj nazwę domeny na adres IP serwera.

4. Udostępnij klucze dostępu przy użyciu nazwy domeny.

5. Przypisz pływający adres IP do maszyny wirtualnej Droplet serwera.

6. Zmień nazwę domeny, tak żeby była skierowana na nowy adres IP.

## Tworzenie serwera Outline w DigitalOcean {#create_an_outline_server_on_digitalocean}

Jeśl masz uruchomiony serwer DigitalOcean, przejdź do następnego kroku.

1. Otwórz Menedżera Outline i kliknij „+” w lewym dolnym rogu, żeby otworzyć ekran tworzenia serwera.

2. Kliknij „Utwórz serwer” na przycisku „DigitalOcean” i postępuj zgodnie z instrukcjami w aplikacji.

![Utwórz serwer](/images/create-DO-server.png)

## Tworzenie nazwy hosta dla serwera {#make_a_hostname_for_your_server}

1. Przejdź do [Google Domains](https://domains.google.com/m/registrar/) i kliknij „Znajdź idealną domenę”.

2. Wpisz nazwę domeny na pasku wyszukiwania i wybierz ją. Jako przykładu użyliśmy `outlinedemo.info`.

3. Przejdź do karty DNS w Google Domains. W sekcji „Niestandardowe rekordy zasobów” w polu „Adres IPV4” wpisz adres IP serwera.

4. Otwórz kartę „Ustawienia” serwera w aplikacji Menedżer Outline. W sekcji „Nazwa hosta” wpisz zakupioną nazwę hosta i kliknij „ZAPISZ”. Dzięki temu wszystkie przyszłe klucze dostępu będą używać tej nazwy hosta zamiast adresu IP serwera.

![Ustaw nazwę hosta](/images/set-hostname.png)

## Zmienianie adresu IP serwera {#change_the_servers_ip_address}

1. Przejdź do swojego serwera na stronie „Droplets” (maszyny wirtualne Droplet) DigitalOcean.

2. Kliknij „Enable Now” (Włącz teraz) w prawym górnym rogu okna obok „Floating IP” (Pływający adres IP).

![Włącz pływający adres IP](/images/floating-ip-DO.png)

1. Znajdź swój serwer na liście maszyn wirtualnych Droplet i kliknij „Assign Floating IP” (Przypisz pływający adres IP).

![Przypisz pływający adres IP](/images/assign-floating-ip-DO.png)

1. Wróć na kartę DNS w Google Domains.

2. Zmień adres IP tak jak wcześniej, ale tym razem użyj nowego pływającego adresu IP. Może to zająć nawet 48 godzin, ale czasami trzeba poczekać tylko kilka minut.

3. Otwórz [narzędzie online DNS Google](https://toolbox.googleapps.com/apps/dig/#A/) i wpisz nazwę domeny, żeby sprawdzić, kiedy zmiana opisana w ostatnim kroku została wprowadzona.

![Wyszukaj swoją domenę w narzędziu DNS Google](/images/google-dns.png)

Kiedy ta zmiana zostanie zastosowana, klienty będą łączyć się z nowym adresem IP. Możesz połączyć się ze swoim serwerem przy użyciu nowego klucza i otworzyć stronę <https://ipinfo.io>, żeby sprawdzić, czy wyświetla się nowy adres IP serwera.

Podsumowanie: przy użyciu rotacji adresów IP serwera Outline można szybko odblokować serwer i przywrócić usługę dla klientów. Jeśli masz pytania, dodaj komentarz pod [postem z ogłoszeniem](https://redd.it/hrbhz4), odwiedź [stronę pomocy Outline](https://support.getoutline.org/) lub [skontaktuj się z nami bezpośrednio](https://support.getoutline.org/s/contactsupport).
