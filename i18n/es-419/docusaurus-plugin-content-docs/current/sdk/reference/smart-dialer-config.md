---
title: "Configuración de Smart Dialer"
sidebar_label: "Configuración de Smart Dialer"
---

**Smart Dialer** busca una estrategia que desbloquee los protocolos DNS y TLS para una
lista determinada de dominios de prueba. Para ello, admite un archivo de configuración en el que se describen múltiples estrategias entre las que
se puede elegir.

## Configuración en YAML para Smart Dialer {#yaml_config_for_the_smart_dialer}

El archivo de configuración que admite Smart Dialer está en formato YAML. Este es un ejemplo:

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

### Configuración de DNS {#dns_configuration}

- El campo `dns` especifica una lista de agentes de resolución de DNS que se deben probar.

- Cada agente de resolución de DNS puede corresponder a uno de los siguientes tipos:

    - `system`: Usa el agente de resolución del sistema. Se especifica con un objeto vacío.

    - `https`: Usa un agente de resolución de DNS-over-HTTPS (DoH) encriptado.

    - `tls`: Usa un agente de resolución de DNS-over-TLS (DoT) encriptado.

    - `udp`: Usa un agente de resolución de UDP.

    - `tcp`: Usa un agente de resolución de TCP.

#### Agente de resolución de DNS-over-HTTPS (DoH) {#dns-over-https_resolver_doh}

```yaml
https:
  name: dns.google
  address: 8.8.8.8
```

- `name`: Es el nombre de dominio del servidor de DoH.

- `address`: Es la dirección host:puerto del servidor de DoH. El valor predeterminado es `name`:443.

#### Agente de resolución de DNS-over-TLS (DoT) {#dns-over-tls_resolver_dot}

```yaml
tls:
  name: dns.google
  address: 8.8.8.8
```

- `name`: Es el nombre de dominio del servidor de DoT.

- `address`: Es la dirección host:puerto del servidor de DoT. El valor predeterminado es `name`:853.

#### Agente de resolución de UDP {#udp_resolver}

```yaml
udp:
  address: 8.8.8.8
```

- `address`: Es la dirección host:puerto del agente de resolución de UDP.

#### Agente de resolución de TCP {#tcp_resolver}

```yaml
tcp:
  address: 8.8.8.8
```

- `address`: Es la dirección host:puerto del agente de resolución de TCP.

### Configuración de TLS {#tls_configuration}

- El campo `tls` especifica una lista de transportes de TLS que se deben probar.

- Cada transporte de TLS es una cadena que especifica el transporte que se usará.

- Por ejemplo, `override:host=cloudflare.net|tlsfrag:1` especifica un transporte
que utiliza el fronting del dominio con Cloudflare y fragmentación de TLS. Consulta la
[documentación de configuración](https://pkg.go.dev/github.com/OutlineFoundation/outline-sdk/x/configurl#hdr-Config_Format)
para conocer más detalles.

### Configuración de resguardo {#fallback_configuration}

Se usa una configuración de resguardo si ninguna de las estrategias sin proxy permite
conectarse. Por ejemplo, esta configuración puede especificar un servidor proxy de respaldo que intente realizar la conexión
del usuario. Una configuración de resguardo se iniciará más lento, ya que las demás
estrategias de DNS o TLS primero deben fallar o debe agotarse su tiempo de espera.

Cada cadena de resguardo debe cumplir con estas características:

- Ser una cadena de configuración `StreamDialer` válida, como se define en [`configurl`](https://pkg.go.dev/github.com/OutlineFoundation/outline-sdk/x/configurl#hdr-Proxy_Protocols)

- Ser un objeto de configuración de Psiphon como elemento secundario de un campo `psiphon`

#### Ejemplo de servidor de Shadowsocks {#shadowsocks_server_example}

```yaml
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

#### Ejemplo de servidor de SOCKS5 {#socks5_server_example}

```yaml
fallback:
  - socks5://[USERINFO]@[HOST]:[PORT]
```

#### Ejemplo de configuración de Psiphon {#psiphon_config_example}

Para usar la red de [Psiphon](https://psiphon.ca/), deberás hacer lo siguiente:

1. Comunícate con el equipo de Psiphon para obtener un archivo de configuración que te otorgue acceso a
su red (lo que puede requerir la celebración de un contrato).

2. Agrega el archivo de configuración de Psiphon a la sección `fallback` del archivo de configuración de
Smart Dialer. Dado que JSON es compatible con YAML, puedes copiar y pegar
el archivo de configuración de Psiphon directamente en la sección `fallback`, de forma similar a este ejemplo:

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

### Cómo usar Smart Dialer {#how_to_use_the_smart_dialer}

Para usar Smart Dialer, crea un objeto `StrategyFinder`, llama al
método `NewDialer` y pasa la lista de dominios de prueba y el archivo de configuración YAML.
El método `NewDialer` devolverá un `transport.StreamDialer` que se puede usar
para crear conexiones usando la estrategia encontrada. Por ejemplo:

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

Este es un ejemplo básico y tal vez debas adaptarlo a tu caso de uso específico.
