Project: /outline/_project.yaml
Book: /outline/_book.yaml

# Deploy using an installation script

This guide walks you through the process of setting up an Outline Server to
provide secure and unrestricted internet access.

## Prerequisites

- A server (physical or virtual) running a supported operating system (Ubuntu
20.04 LTS or Debian 10)
- Root or sudo access to the server

## Instructions

1. Download and run the Outline installation script.

    ```sh
    sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/Jigsaw-Code/outline-apps/master/server_manager/install_scripts/install_server.sh)"
    ```

1. Follow the on-screen prompts.
