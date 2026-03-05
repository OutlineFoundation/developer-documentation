---
title: "Add Outline SDK to Your Mobile App"
sidebar_label: "Mobile App Integration"
---

En este documento, se describe cómo integrar el SDK de Outline en tus aplicaciones
para dispositivos móviles, con un enfoque en la biblioteca `MobileProxy` para simplificar la administración del proxy
local.

`MobileProxy` es una biblioteca basada en Go diseñada para optimizar la integración de las
funciones del proxy en apps para dispositivos móviles. Utiliza [Go
para dispositivos móviles](https://go.dev/wiki/Mobile) con el objetivo de generar bibliotecas para dispositivos móviles, lo que te permite
configurar las bibliotecas de redes de tu app para enrutar el tráfico a través de un proxy
local.

**App sin MobileProxy**

![Contenido de &quot;App sin MobileProxy&quot;](/images/mobileproxy-before.png)

**App con MobileProxy**

![Contenido de &quot;App con MobileProxy&quot;](/images/mobileproxy-after.png)

## Paso 1: Compila las bibliotecas MobileProxy para dispositivos móviles

Usa [gomobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile) para compilar
el código de Go en bibliotecas para iOS y Android.

1. Clona el repositorio del SDK de Outline:

2. Compila los objetos binarios de Go para dispositivos móviles con [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies):

#### Cómo agregar compatibilidad con Psiphon

Puedes agregar compatibilidad con el uso de la red de [Psiphon](https://psiphon.ca/)
siguiendo estos pasos adicionales:

    - Comunícate con el equipo de Psiphon para obtener un archivo de configuración que te otorgue acceso a
su red (lo que puede requerir la celebración de un contrato).

    - Agrega el archivo de configuración de Psiphon a la sección `fallback` de tu
archivo de configuración `SmartDialer`.

    - Crea el MobileProxy con la marca `-tags psiphon`:

La marca `-tags psiphon` es obligatoria porque la base de código de Psiphon tiene
una licencia de GPL, que puede imponer restricciones de licencia en tu propio
código. Te recomendamos que obtengas una licencia especial de Psiphon.

3. Genera bibliotecas para dispositivos móviles y agrégalas a tu proyecto:

### Android

En Android Studio, selecciona **File > Import Project…** para importar el paquete `out/mobileproxy.aar` generado. Para obtener más ayuda, consulta la sección [Building and deploying to Android](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1) del artículo sobre Go para dispositivos móviles.

### iOS

Arrastra el paquete `out/mobileproxy.xcframework` al proyecto de Xcode. Para
obtener más ayuda, consulta la sección [Building and deploying to iOS](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1) del artículo sobre Go para
dispositivos móviles.

## Paso 2: Ejecuta MobileProxy

Inicializa e inicia el proxy local `MobileProxy` en el entorno de ejecución de tu app.
Puedes usar una configuración de transporte estático o el proxy inteligente para
la selección de una estrategia dinámica.

- **Configuración de transporte estático**: Usa la función `RunProxy` con una dirección
local y una configuración de transporte.

### Android

### iOS

- **Smart Proxy**: Smart Proxy selecciona de forma dinámica estrategias de DNS y TLS
en función de dominios de prueba especificados. Debes especificar la estrategia de
configuración en formato YAML
([ejemplo](https://github.com/Jigsaw-Code/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml)).

### Android

### iOS

## Paso 3: Configura clientes HTTP y bibliotecas de redes

Configura tus bibliotecas de redes para que usen el puerto y la dirección del proxy local.

### HttpClient Dart o Flutter

Configura el proxy con
[`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html).

### OkHttp (Android)

Configura el proxy con
[`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/).

### JVM (Java y Kotlin)

Configura el proxy para usarlo con [propiedades del
sistema](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html):

### WebView de Android

Aplica la configuración de proxy a todas las vistas web de tu aplicación con
la
biblioteca
[`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController):

### WebView de iOS

A partir de iOS 17, puedes agregar una configuración de proxy a `WKWebView` usando su
[propiedad
`WKWebsiteDataStore`](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration):

## Uso avanzado: Genera una biblioteca para dispositivos móviles personalizada

Para los casos de uso avanzados, puedes generar tus propias bibliotecas para dispositivos móviles:

1. **Crea una biblioteca de Go**: Desarrolla un paquete de Go uniendo las funciones requeridas del
SDK.

2. **Genera bibliotecas para dispositivos móviles**: Usa `gomobile bind` para producir Android
ARchives (AAR) y frameworks de Apple. Ejemplos:

    - [Esquema de Android ARchive](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [Esquema de framework de Apple](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **Integra la biblioteca en tu app**: Agrega la biblioteca generada a tu aplicación para dispositivos
móviles.
