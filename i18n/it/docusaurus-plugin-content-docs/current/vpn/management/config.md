---
title: "Configure Access Keys"
sidebar_label: "Configure Access Keys"
---

Outline utilizza una configurazione basata su YAML per definire i parametri VPN e gestire il traffico TCP/UDP. La configurazione supporta la componibilità a più livelli, consentendo configurazioni flessibili ed estensibili.

La configurazione di livello superiore specifica un [TunnelConfig](../reference/access-key-config#tunnelconfig).

## Esempi

Una tipica configurazione Shadowsocks sarà simile a questa:

Tieni presente che ora possiamo avere TCP e UDP in esecuzione su porte o endpoint diversi e con prefissi diversi.

Puoi utilizzare anchor YAML e la chiave di unione `<<` per evitare duplicati:

Ora è possibile comporre strategie ed eseguire hop multipli:

In caso di blocco dei protocolli "look-like-nothing" come Shadowsocks, puoi utilizzare Shadowsocks-over-Websockets. Fai riferimento alla [configurazione di esempio del server](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml) per sapere come eseguirne il deployment. Una configurazione client apparirà così:

Nota che l'endpoint Websocket può, a sua volta, prendere un endpoint, che può essere sfruttato per bypassare il blocco basato su DNS:

Per garantire la compatibilità tra diverse versioni del client Outline, utilizza l'opzione `first-supported` nella tua configurazione. Ciò è particolarmente importante perché vengono aggiunte nuove strategie e funzionalità a Outline, poiché non tutti gli utenti potrebbero aver aggiornato il software client più recente. Utilizzando `first-supported`, puoi fornire una singola configurazione che funziona senza problemi su diverse piattaforme e versioni client, garantendo la compatibilità con le versioni precedenti e un'esperienza utente coerente.
