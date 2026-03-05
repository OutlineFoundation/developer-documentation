---
title: "Configure Access Keys"
sidebar_label: "Configure Access Keys"
---

Outline gebruikt een op YAML gebaseerde configuratie om VPN-parameters te definiëren en TCP-/UDP-verkeer af te handelen. De configuratie kan op verschillende niveaus worden aangepast, waardoor flexibele en uitgebreide installatie mogelijk wordt gemaakt.

De configuratie op het hoogste niveau geeft een [TunnelConfig](../reference/access-key-config#tunnelconfig) op.

## Voorbeelden

Zo ziet een typische Schadowsocks-configuratie eruit:

Je kunt TCP en UDP nu laten uitvoeren op verschillende poorten of eindpunten, met verschillende voorvoegsels.

Je kunt YAML-ankers en de samenvoegingscode `<<` gebruiken om dupliceren te voorkomen:

Het is nu mogelijk om strategieën op te stellen en multi-hops te maken:

Als je 'look-like-nothing'-protocollen zoals Shadowsocks wilt blokkeren, kun je Shadowsocks-over-WebSockets gebruiken. Ga naar de [voorbeeldconfiguratie voor een server](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml) voor meer informatie over hoe je dit implementeert. Zo ziet een clientconfiguratie eruit:

Het WebSocket-eindpunt kan ook een eindpunt bevatten, dat je kunt gebruiken om op DNS gebaseerde blokkeringen te omzeilen.

Gebruik in je configuratie de optie `first-supported` om te zorgen dat deze functie compatibel is met de verschillende Outlook-clientversies. Dit is met name belangrijk als er nieuwe strategieën en functies worden toegevoegd aan Outline, omdat misschien nog niet alle gebruikers hebben geüpdatet naar de nieuwste clientsoftware. Door `first-supported` te gebruiken, kun je één configuratie maken die naadloos werkt op verschillende platforms en clientversies. Zo zorg je voor compatibiliteit met eerdere versies en een consistente gebruikerservaring.
