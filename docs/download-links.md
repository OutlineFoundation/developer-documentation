Project: /outline/_project.yaml
Book: /outline/_book.yaml

# Concepts

Outline helps users bypass restrictions to access the open internet. Here's are
some key concepts to understand how it works:

## Service providers and end users

The Outline system involves two main roles: **service providers**, who manage
the servers, and **end users**, who access the internet through those servers.

-   **Service providers** create the Outline servers, generate **access keys**,
    and **distribute the keys** to end users. One way to do this is using the
    **Outline Manager** application.
-   **End users** install the **Outline Client** application, paste in the
    **access key** they received, and **connect** to a secure tunnel.

## Access keys {:#access-keys}

Access keys are the credentials that allow users to connect to an Outline
server. They contain the necessary information for the Outline Client to
establish a secure connection. There are two types of access keys:

-   **Static access keys** encode all the server information needed to connect
    (server address, port, password, encryption method), preventing the access
    information from being modified. Users paste this key into the Outline
    Client.

    Example:

    ```none
    ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTo1UkVmeFRqbHR6Mkw@outline-server.example.com:17178/?outline=1
    ```

-   **Dynamic access keys** allow a service provider to host the server access
    information remotely. This lets providers update their server configuration
    (server address, port, passwords, encryption method) without needing to
    reissue new access keys to end users. For more detailed documentation, see
    [Dynamic Access
    Keys](/outline/docs/guides/service-providers/dynamic-access-keys).