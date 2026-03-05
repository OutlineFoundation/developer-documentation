---
title: "Concepts"
sidebar_label: "Concepts"
---

Outline ayuda a los usuarios a evitar restricciones para acceder al Internet abierto. A continuación encontrarás algunos conceptos clave para entender cómo funciona:

## Proveedores de servicios y usuarios finales

El sistema de Outline incluye dos roles principales: **proveedores de servicios**, que gestionan los servidores, y **usuarios finales**, que acceden a Internet mediante esos servidores.

- Los **proveedores de servicios** crean los servidores de Outline, generan **claves de acceso** y **distribuyen las claves** a los usuarios finales. Una forma de hacer todo esto es usar la aplicación **Administrador de Outline**.

- Los **usuarios finales** instalan la aplicación de **cliente de Outline**, copian la **clave de acceso** que han recibido y **se conectan** a un túnel seguro.

## Claves de acceso

Las claves de acceso son las credenciales que permiten a los usuarios conectarse a un servidor de Outline. Contienen la información necesaria para que el cliente de Outline establezca una conexión segura. Hay dos tipos de claves de acceso:

- Las **claves de acceso estáticas** permiten codificar toda la información del servidor necesaria para establecer la conexión (dirección del servidor, puerto, contraseña y método de cifrado), de forma que la información de acceso no se modifique. Los usuarios copian esta clave en el cliente de Outline.

Ejemplo:

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTo1UkVmeFRqbHR6Mkw@outline-server.example.com:17178/?outline=1
```

- Las **claves de acceso dinámicas** permiten que un proveedor de servicios aloje la información de acceso al servidor de forma remota. Esto hace posible que los proveedores actualicen la configuración de su servidor (dirección del servidor, puerto, contraseñas y método de cifrado) sin necesidad de volver a emitir nuevas claves de acceso para los usuarios finales. Para acceder a documentación más detallada, consulta el artículo [Claves de acceso dinámicas](vpn/management/dynamic-access-keys).
