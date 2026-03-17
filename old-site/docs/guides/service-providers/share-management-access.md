# Share management access with others

As your Outline service expands, you might find it necessary to delegate
management responsibilities to other trusted individuals. This document outlines
the various methods available for sharing management access with other managers.

The method for sharing management access varies depending on how your Outline
server was initially deployed.

## Cloud provider deployments

For Outline servers deployed on cloud platforms such as DigitalOcean, AWS, or
Google Cloud, management access is typically handled through the provider's
integrated identity and access management (IAM) capabilities, offering a more
secure and controlled approach compared to manual configuration sharing.

### DigitalOcean

DigitalOcean provides a robust **Teams** feature that lets you invite other
DigitalOcean users to collaborate on your projects. This is the recommended way
to grant management access to your Outline server hosted on their platform.

#### 1. Grant team access

The most effective way to share management of your Outline server hosted on
DigitalOcean is by utilizing DigitalOcean's **Teams** feature.

*   Sign in to your DigitalOcean account.
*   Navigate to the **Teams** section.
*   Create a new team (if you haven't already) or invite existing DigitalOcean
    users to your team.
*   When inviting members, you can assign them specific roles and grant them
    access to specific resources, including your Droplet(s) running Outline.

#### 2. Control permissions

Carefully consider the permissions you grant to team members. For managing the
Outline server, you might grant them "Read" and "Write" access to the specific
Droplet. This will allow them to:

*   View the Droplet's details (IP address, status, etc.).
*   Access the Droplet's console (if necessary for troubleshooting).
*   Potentially perform actions like restarting the Droplet (depending on the
    granted permissions).

Users that connect the Outline Manager to their DigitalOcean account will now be
able to view and manage all Outline servers linked to that account.

Tip: Encourage new managers to enable multi-factor authentication (MFA) on their
cloud provider accounts for enhanced security.

## Manual installations

Caution: Sharing management access to manual installations makes revoking access
challenging. The most direct method is a full server reinstallation, which
generates a new configuration but also resets all user access keys.

For those who have manually installed Outline on their own servers using the
[installation script](server-setup-advanced.md), the primary way to grant
management access is by sharing the **access config**.

The Outline Manager application needs a specific configuration string to connect
to and manage an Outline server. This configuration string contains all the
necessary information, including the server address, port, and a secret key for
authentication.

### 1. Locate the `access.txt` file

On the server where Outline is installed, navigate to the Outline directory. The
exact location might vary slightly depending on your installation method, but
common locations include:

*   `/opt/outline/access.txt`
*   `/etc/outline/access.txt`
*   Within the Docker volume used by the Outline server container.

### 2. Retrieve the access config

Once you found the `access.txt` file, convert it into JSON, which is the format
the Outline Manager expects in the next step.

```sh
sed -n '2s/^apiUrl://p; 1s/^certSha256://p' /opt/outline/access.txt | paste -d'\n' -s | sed 'H;1h;$!d;x;s/\n/", \"apiUrl\": \"/g; s/^/{"certSha256": \"/; s/$/\"}/'
```

The output will contain the self-signed certificate fingerprint (`certSha256`)
and the endpoint of the management API on the server (`apiUrl`):

```json
{"certSha256": "1DCC18CC9F6C34EBBB639255F4D1BC6984C2F6A47B15F7A49AA8AFB69B7E4DDE", "apiUrl": "https://1.1.1.1:12345/Fw-CkWFNSN7Ml8LLM8Pduw"}
```

Important: This line contains sensitive information. Share it only with trusted
individuals who need management access.

### 3. Share the access config securely

Copy the output and securely share it with the new Outline Manager. Avoid
sending it using unencrypted channels like plain email or instant messaging.
Consider using a password manager's secure sharing feature or another encrypted
communication method.

Pasting the provided **access config** into the Outline Manager allows the new
manager to add and subsequently manage the Outline server through the
application's interface. Additional support for using the Outline Manager is
available in the [Outline Help Center](https://support.google.com/outline).
