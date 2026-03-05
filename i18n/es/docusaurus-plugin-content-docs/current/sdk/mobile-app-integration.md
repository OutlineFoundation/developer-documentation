---
title: "Add Outline SDK to Your Mobile App"
sidebar_label: "Mobile App Integration"
---

En esta página se explica cómo integrar el SDK de Outline en las aplicaciones móviles; se presta especial atención a la biblioteca `MobileProxy`, que simplifica la gestión del proxy local.

`MobileProxy` es una biblioteca basada en Go que se ha diseñado para optimizar la integración de las funciones del proxy en las aplicaciones móviles. A partir del repositorio [Go Mobile](https://go.dev/wiki/Mobile), genera bibliotecas para dispositivos móviles con las que puedes configurar las bibliotecas de redes de tus aplicaciones que enrutan el tráfico a través de un proxy local.

**Aplicación sin MobileProxy**

![Aplicación de contenido sin MobileProxy](/images/mobileproxy-before.png)

**Aplicación con MobileProxy**

![Aplicación de contenido con MobileProxy](/images/mobileproxy-after.png)

## Paso 1: Crear bibliotecas MobileProxy para dispositivos móviles

Usa [gomobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile) para compilar el código de Go en bibliotecas para Android y iOS.

1. 

Clona el repositorio del SDK de Outline:

2. 

Compila los binarios de Go Mobile con [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies):

#### Añade compatibilidad con Psiphon

Para habilitar el uso de la red [Psiphon](https://psiphon.ca/), sigue estos otros pasos:

    - Ponte en contacto con el equipo de Psiphon para obtener una configuración que te dé acceso a su red. Puede que tengas que firmar un contrato.

    - Añade la configuración de Psiphon que recibas a la sección `fallback` de tu configuración de `SmartDialer`.

    - 

Compila MobileProxy con la marca `-tags psiphon`:

La marca `-tags psiphon` es obligatoria porque el código base de Psiphon tiene licencia de GPL, que puede imponer restricciones a tu propio código. Plantéate pedirles una licencia especial.

3. 

Genera bibliotecas para dispositivos móviles y añádelas a tu proyecto:

### Android

En Android Studio, selecciona **File > Import Project…** (Archivo > Importar proyecto…) para importar el paquete `out/mobileproxy.aar` generado. Si necesitas más ayuda, consulta la sección sobre [compilación e implementación en Android](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1) de Go Mobile.

### iOS

Arrastra el paquete `out/mobileproxy.xcframework` al proyecto Xcode. Si necesitas más ayuda, consulta la sección sobre [compilación e implementación en iOS](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1) de Go Mobile.

## Paso 2: Ejecutar MobileProxy

Inicializa e inicia el proxy local `MobileProxy` en el entorno de ejecución de tu aplicación.
Puedes usar una configuración de transporte estática o SmartProxy si prefieres una selección de estrategia dinámica.

- 

**Configuración de transporte estática:** usa la función `RunProxy` con una dirección y una configuración de transporte locales.

### Android

### iOS

- 

**SmartProxy:** SmartProxy selecciona dinámicamente estrategias de DNS o TLS en función de los dominios de prueba especificados. Debes especificar la estrategia de configuración en formato YAML ([ejemplo](https://github.com/Jigsaw-Code/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml)).

### Android

### iOS

## Paso 3: Configurar clientes HTTP y bibliotecas de redes

Configura tus bibliotecas de redes de modo que usen la dirección y el puerto del proxy local.

### HttpClient de Dart o Flutter

Define el proxy con [`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html).

### OkHttp (Android)

Define el proxy con [`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/).

### JVM (Java o Kotlin)

Configura el proxy que se debe usar con [propiedades del sistema](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html):

### Android WebView

Aplica una configuración de proxy a todas las vistas web de tu aplicación con la biblioteca [`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController):

### iOS WebView

En iOS 17, puedes añadir una configuración de proxy a `WKWebView` usando su [propiedad `WKWebsiteDataStore`](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration):

## Procedimiento avanzado: genera una biblioteca para dispositivos móviles personalizada

En casos prácticos avanzados, puedes generar tus propias bibliotecas para dispositivos móviles:

1. **Crea una biblioteca de Go:** desarrolla un paquete de Go que envuelva las funciones del SDK que necesitas.

2. **Genera bibliotecas para dispositivos móviles:** usa `gomobile bind` para producir instancias de Android ARchive (AAR) y frameworks de Apple. Ejemplos:

    - [Android ARchive de Outline](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [Framework de Apple de Outline](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **Intégralas en tu aplicación:** añade las bibliotecas que generes a tu aplicación móvil.
