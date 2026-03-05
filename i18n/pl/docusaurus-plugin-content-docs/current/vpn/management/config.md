---
title: "Configure Access Keys"
sidebar_label: "Configure Access Keys"
---

Outline korzysta z konfiguracji w formacie YAML do definiowania parametrów VPN i obsługi ruchu TCP/UDP. Konfiguracja obsługuje kompozycyjność na wielu poziomach, umożliwiając elastyczne i rozszerzalne konfiguracje.

Konfiguracja najwyższego poziomu określa [TunnelConfig](../reference/access-key-config#tunnelconfig).

## Przykłady

Standardowa konfiguracja Shadowsocks będzie wyglądała w następujący sposób:

Zwróć uwagę, że TCP i UDP mogą być uruchamiane na różnych portach lub punktach końcowych oraz z różnymi zakresami.

Możesz korzystać z kotwic YAML oraz klucza scalającego `<<`, aby uniknąć duplikowania:

Można teraz tworzyć strategie i wykonywać liczne przeskoki:

W przypadku nietypowych protokołów, takich jak Shadowsocks, możesz skorzystać z Shadowsocks-over-Websockets. Zapoznaj się z [przykładową konfiguracją serwera](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml), aby dowiedzieć, się jak przeprowadzić wdrożenie. Konfiguracja klienta będzie wyglądała w następujący sposób:

Zwróć uwagę, że punkt końcowy Websocket może w konsekwencji wybrać punkt końcowy, który może zostać wykorzystany do ominięcia blokady systemu BNS.

Aby zadbać o zgodność między wieloma wersjami klienta Outline, skorzystaj z opcji `first-supported` w swojej konfiguracji. Jest to szczególnie istotne, jako że do Outline dodano nowe strategie i funkcje, a nie wszyscy użytkownicy zaktualizowali oprogramowanie klienta do najnowszej wersji. Korzystając z `first-supported`, możesz zapewnić pojedynczą konfigurację, która działa bezproblemowo na wielu różnych platformach i wersjach klienta, co przełoży się na zgodność wsteczną i spójne wrażenia użytkownika.
