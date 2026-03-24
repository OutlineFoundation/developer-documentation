---
title: "Comparte el acceso de administración con otras personas"
sidebar_label: "Comparte el acceso de administración con otras personas"
---

A medida que crezca tu servicio de Outline, tal vez necesites delegar
las responsabilidades de administración a otras personas de confianza. En este documento, se describen
los diversos métodos disponibles para compartir el acceso de administración con otros encargados.

El método varía según la forma en que se implementó inicialmente
el servidor de Outline.

## Implementaciones en proveedores de servicios en la nube {#cloud_provider_deployments}

En el caso de los servidores de Outline implementados en plataformas de nube (como DigitalOcean, AWS o
Google Cloud), el acceso de administración suele manejarse a través de las funciones
integradas de administración de identidades y accesos (IAM) del proveedor, lo que ofrece un
enfoque más seguro y controlado que el uso compartido a través de configuración manual.

### DigitalOcean {#digitalocean}

DigitalOcean proporciona una sólida función de **equipos** que permite invitar a otros
usuarios de la plataforma a colaborar en proyectos. Este es el método recomendado
para otorgar acceso de administración a un servidor de Outline alojado en DigitalOcean.

#### 1. Otórgale acceso a un equipo {#1_grant_team_access}

La manera más eficaz de compartir la administración de un servidor de Outline alojado en
DigitalOcean es a través de **equipos**.

- Accede a tu cuenta de DigitalOcean.

- Ve a la sección **Teams**.

- Crea un equipo nuevo (si aún no lo has hecho) o invita a usuarios existentes
de DigitalOcean a tu equipo.

- Cuando invitas a miembros, puedes asignarles roles específicos y otorgarles
acceso a recursos específicos, incluidos los Droplets en los que se ejecute Outline.

#### 2. Controla los permisos {#2_control_permissions}

Ten cuidado con los permisos que les otorgarás a los miembros del equipo. Para administrar el
servidor de Outline, podrías otorgarles acceso de lectura o escritura a un Droplet específico, lo que les permitirá hacer lo siguiente:

- Consultar los detalles del Droplet (dirección IP, estado, etcétera)

- Acceder a la consola del Droplet (si es necesario para solucionar problemas)

- Realizar acciones como reiniciar el Droplet (según los
permisos otorgados)

Los usuarios que conecten Outline Manager a su cuenta de DigitalOcean ahora podrán
consultar y administrar todos los servidores de Outline vinculados a ella.


:::tip
Recomiéndales a los nuevos administradores que habiliten la autenticación de varios factores (MFA) en sus cuentas del proveedor de servicios en la nube para aumentar la seguridad.
:::

## Instalaciones manuales {#manual_installations}


:::caution
Compartir el acceso de administración a instalaciones manuales dificulta revocar el acceso. El método más directo es reinstalar el servidor por completo, lo que genera una nueva configuración, pero también restablece todas las claves de acceso de los usuarios.
:::

Si instalaste Outline de forma manual en tus propios servidores usando la
[secuencia de comandos](../getting-started/server-setup-advanced), el principal método para otorgar
acceso de administración es compartir el **archivo de configuración de acceso**.

La aplicación Outline Manager necesita una cadena de configuración específica para conectarse
a un servidor de Outline y administrarlo. Esta contiene toda la
información necesaria, como la dirección del servidor, el puerto y una clave secreta para la
autenticación.

### 1. Ubica el archivo `access.txt` {#1_locate_the_accesstxt_file}

En el servidor donde está instalado Outline, ve al directorio de Outline. La
ubicación exacta puede variar levemente según el método de instalación, pero estas son las más comunes:

- `/opt/outline/access.txt`

- `/etc/outline/access.txt`

- En el volumen de Docker que usa el contenedor de servidor de Outline

### 2. Recupera el archivo de configuración de acceso {#2_retrieve_the_access_config}

Cuando encuentres el archivo `access.txt`, conviértelo en el formato JSON
que requiere Outline Manager para el siguiente paso.

```sh
sed -n '2s/^apiUrl://p; 1s/^certSha256://p' /opt/outline/access.txt | paste -d'\n' -s | sed 'H;1h;$!d;x;s/\n/", \"apiUrl\": \"/g; s/^/{"certSha256": \"/; s/$/\"}/'
```

El resultado contendrá la huella digital del certificado autofirmado (`certSha256`)
y el endpoint de la API de administración en el servidor (`apiUrl`):

```json
{"certSha256": "1DCC18CC9F6C34EBBB639255F4D1BC6984C2F6A47B15F7A49AA8AFB69B7E4DDE", "apiUrl": "https://1.1.1.1:12345/Fw-CkWFNSN7Ml8LLM8Pduw"}
```


:::warning[Important]
Esta línea contiene información sensible. Compártela solo con personas de confianza que necesiten tener acceso de administración.
:::

### 3. Comparte el archivo de configuración de acceso de forma segura {#3_share_the_access_config_securely}

Copia el resultado y compártelo de forma segura con el nuevo administrador de Outline. Evita
enviarlo usando canales no encriptados, como mensajería instantánea o correos electrónicos sin formato.
Te recomendamos usar una función para compartir segura, como un administrador de contraseñas o algún otro método
de comunicación encriptado.

Cuando el nuevo administrador pegue el **archivo de configuración de acceso**
proporcionado en Outline Manager, podrá agregar y administrar el servidor de Outline a través de la
interfaz de la aplicación. Consulta el [Centro de ayuda de Outline](https://support.getoutline.org)
si necesitas más información para usar Outline Manager.
