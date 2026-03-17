---
title: "Configuración del marcador inteligente"
sidebar_label: "Configuración del marcador inteligente"
---

El **marcador inteligente** busca una estrategia que desbloquee DNS y TLS en la lista proporcionada de dominios de prueba. Necesita una configuración que describa varias estrategias entre las que elegir.

## Configuración de YAML para el marcador inteligente {#yaml_config_for_the_smart_dialer}

El marcador inteligente necesita una configuración en formato YAML. Aquí tienes un ejemplo:

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

- El campo `dns` especifica la lista de resoluciones de DNS que se deben probar.

- Las resoluciones de DNS pueden ser de uno de estos tipos:

    - `system`: usa la resolución del sistema. Se especifica con un objeto vacío.

    - `https`: usa una resolución de DNS‑over‑HTTPS (DoH) cifrada.

    - `tls`: usa una resolución de DNS a través de TLS cifrada.

    - `udp`: usa una resolución de UDP.

    - `tcp`: usa una resolución de TCP.

#### Resolución de DNS‑over‑HTTPS (DoH) {#dns-over-https_resolver_doh}

```yaml
https:
  name: dns.google
  address: 8.8.8.8
```

- `name`: nombre de dominio del servidor de DoH.

- `address`: host:puerto del servidor de DoH. El valor predeterminado es `name`:443.

#### Resolución de DNS a través de TLS (DoT) {#dns-over-tls_resolver_dot}

```yaml
tls:
  name: dns.google
  address: 8.8.8.8
```

- `name`: nombre de dominio del servidor de DoT.

- `address`: host:puerto del servidor de DoT. El valor predeterminado es `name`:853.

#### Resolución de UDP {#udp_resolver}

```yaml
udp:
  address: 8.8.8.8
```

- `address`: host:puerto de la resolución de UDP.

#### Resolución de TCP {#tcp_resolver}

```yaml
tcp:
  address: 8.8.8.8
```

- `address`: host:puerto de la resolución de TCP.

### Configuración de TLS {#tls_configuration}

- El campo `tls` especifica la lista de transportes TLS que se deben probar.

- Cada transporte TLS es una cadena que especifica qué transporte se debe usar.

- Por ejemplo, `override:host=cloudflare.net|tlsfrag:1` especifica un transporte que usa ocultación de dominios con Cloudflare y fragmentación de TLS. Para obtener más información, consulta la [documentación sobre la configuración](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#hdr-Config_Format).

### Configuración de respaldo {#fallback_configuration}

Si ninguna de las estrategias sin proxy logra conectar, se usa una configuración de respaldo. Por ejemplo, se puede especificar que un servidor proxy de copia de seguridad intente establecer la conexión del usuario. El método de respaldo tarda más en iniciarse, ya que antes deben fallar o agotar el tiempo de espera las demás estrategias de DNS o TLS.

Las cadenas de respaldo deben ser lo siguiente:

- Una cadena de configuración `StreamDialer` válida, tal como se defina en [`configurl`](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#hdr-Proxy_Protocols).

- Un objeto de configuración de Psiphon válido que sea un elemento secundario de un campo `psiphon`.

#### Ejemplo de servidor Shadowsocks {#shadowsocks_server_example}

```yaml
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

#### Ejemplo de servidor SOCKS5 {#socks5_server_example}

```yaml
fallback:
  - socks5://[USERINFO]@[HOST]:[PORT]
```

#### Ejemplo de configuración de Psiphon {#psiphon_config_example}

Para usar la red [Psiphon](https://psiphon.ca/), debes hacer lo siguiente:

1. Ponerte en contacto con el equipo de Psiphon para obtener una configuración que te dé acceso a su red. Puede que tengas que firmar un contrato.

2. Añadir la configuración de Psiphon que recibas a la sección `fallback` de la configuración de tu marcador inteligente. JSON es compatible con YAML, así que puedes copiar y pegar la configuración de Psiphon directamente en la sección `fallback`, como en este ejemplo:

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


:::note
El código base de Psiphon tiene licencia de GPL, que puede imponer restricciones a tu propio código. Plantéate pedirles una licencia especial.
:::

### Cómo usar el marcador inteligente {#how_to_use_the_smart_dialer}

Para usar el marcador inteligente, crea un objeto `StrategyFinder` y llama al método `NewDialer` pasando la lista de dominios de prueba y la configuración de YAML.
El método `NewDialer` devuelve un objeto `transport.StreamDialer` que sirve para crear conexiones empleando la estrategia encontrada. Por ejemplo:

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

Este es un ejemplo básico que quizá debas adaptar a tu caso práctico específico.
