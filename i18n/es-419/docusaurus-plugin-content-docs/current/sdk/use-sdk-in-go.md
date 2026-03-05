---
title: "Add Outline SDK to Your Go Code"
sidebar_label: "Go Integration"
---

En esta guía, se explica el proceso de configuración de tu entorno de Go y
cómo usar el SDK de Outline en ese lenguaje de programación.

Para demostrar una función del SDK,
crearemos una aplicación de ejemplo llamada `splitfetch`. Esta recupera una página web, pero, en vez de enviar
la solicitud en un solo paquete de red, **usa el SDK de Outline para dividir la
transmisión de TCP inicial en dos paquetes separados**, lo que puede ayudar a evitar algunas formas
de intervención de la red.

Podrás ejecutar la aplicación en **Linux, macOS y Windows**.
Para realizar integraciones con apps para dispositivos móviles, consulta [Agrega el SDK de Outline a tu app para dispositivos móviles](mobile-app-integration).

## Paso 1: Configura Go

Primero, necesitarás el [lenguaje de programación Go](https://go.dev/).
Si ya tienes instalada la versión 1.21 (o una posterior), puedes avanzar al
siguiente paso.

Para instalarlo, puedes seguir la [guía oficial](https://go.dev/doc/install)
o seguir estos pasos si usas un administrador de paquetes:

### Linux

Sigue los pasos que se indican en [Go Wiki: Ubuntu](https://go.dev/wiki/Ubuntu).

### macOS

### Windows

Luego, para verificar que Go se haya instalado correctamente,
ejecuta este comando en la terminal:

## Paso 2: Crea la aplicación `splitfetch`

Configuremos el proyecto `splitfetch`. Primero, crea el directorio del proyecto y, luego,
inicializa un módulo de Go:

Luego, agrega el SDK de Outline y crea el archivo `main.go`.

## Paso 3: Usa el SDK de Outline en la aplicación

Abre el archivo `main.go` en el editor de código que prefieras y pega el siguiente
código en él, que contiene toda la lógica de la aplicación `splitfetch`.

Después de guardar el código, ejecuta el siguiente comando en la terminal para asegurarte
de que el archivo `go.mod` se haya actualizado correctamente.

## Paso 4: Ejecuta la aplicación

Ahora que implementaste el código, puedes ejecutar la aplicación `splitfetch`.

En el directorio `splitfetch`, ejecuta el siguiente comando en la
terminal, pasando una URL como argumento:

Con esta acción, se compila y ejecuta la aplicación, que muestra el contenido HTML de la página web.

Si quieres crear y distribuir un programa independiente que puedas ejecutar
sin `go`, usa el comando `go build`:

### Linux y macOS

### Windows

Cuando se termine de compilar la aplicación, podrás distribuirla y ejecutarla.
Por ejemplo:
