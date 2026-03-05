---
title: "Concepts"
sidebar_label: "Concepts"
---

Outline ayuda a los usuarios a evitar las restricciones para que accedan al Internet abierto. Estos son
algunos conceptos clave para que entiendas cómo funciona:

## Proveedores de servicios y usuarios finales

El sistema de Outline incluye dos roles principales: los **proveedores de servicios**, que administran
los servidores, y los **usuarios finales**, que acceden a Internet a través de esos servidores.

- Los **proveedores de servicios** crean los servidores de Outline, generan **claves de acceso**
y **las distribuyen** a los usuarios finales. Una forma de hacer esto es usar la
aplicación de **Outline Manager**.

- Los **usuarios finales** instalan la aplicación **cliente de Outline**, pegan la
**clave de acceso** que recibieron y se **conectan** a un túnel seguro.

## Claves de acceso

Las claves de acceso son las credenciales que les permiten a los usuarios conectarse a un servidor de
Outline. Contienen la información necesaria para que el cliente de Outline
establezca una conexión segura. Existen dos tipos de claves de acceso:

- Las **claves de acceso estáticas**, que codifican toda la información del servidor necesaria para conectarse
(dirección del servidor, puerto, contraseña y método de encriptación), lo que impide
que la información se modifique. Los usuarios pegan esta clave en el cliente de
Outline.

Ejemplo:

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTo1UkVmeFRqbHR6Mkw@outline-server.example.com:17178/?outline=1
```

- Las **claves de acceso dinámicas**, que permiten que un proveedor de servicios aloje la información de acceso
del servidor de forma remota. Esto permite que los proveedores actualicen su configuración del servidor
(dirección del servidor, puerto, contraseña y método de encriptación) sin
emitir nuevas claves de acceso para los usuarios finales. Para ver una documentación más detallada, consulta
[Claves de acceso
dinámicas](vpn/management/dynamic-access-keys).
