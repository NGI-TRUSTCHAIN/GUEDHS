# GUEHDS Federated Network

GUEHDS is a portal for managing and interacting with a Federated Network powered by [PySyft](https://github.com/OpenMined/PySyft). The portal's user interface (UI) is built using [Shiny for Python](https://shiny.posit.co/py/).


## Installation

### Requirements:

- [Docker](https://www.docker.com/)
- [Poetry](https://python-poetry.org/)

### Dependencies

Install the project dependencies by running the following command:

```bash
poetry install
```


## Setup

### Project Setup

**Note:** Run all commands from the `federated_network` directory.

1. Create a `.env` file in the root of the project with the following content, by copying the `.env.example` file:

    ```bash
    cp .env.example .env
    ```

2. Setup `/etc/hosts`:

    Add the following entries to your `/etc/hosts` file:

    ```
    127.0.0.1   auth.local.promptly.health
    127.0.0.1   guehds.local.promptly.health
    127.0.0.1   syft.local.promptly.health
    127.0.0.1   blockchain.local.promptly.health
    ```

3. To start the PyGrid domain network, run the following command:

    ```bash
    hagrid launch domain
    ```

    This will launch a PyGrid domain at `http://syft.local.promptly.health`.

4. Start the Blockchain Service

    To start the blockchain service, run the following command:

    ```bash
    cd ../blockchain-api
    docker compose up -d
    ```

5. Start the Docker Containers

    To set up and start the necessary services, run the following command:

    ```bash
    cd ../federated_network
    docker compose up -d
    ```

### Interacting as a Data Owner

To interact with the portal as a Data Owner, access the portal at `http://guehds.local.promptly.health` and login with the following credentials:

- **Username**: `info@openmined.org`
- **Password**: `changethis`

### Interacting as a Data Scientist

Explore and interact with the federated network as a Data Scientist by following the examples available in the [notebooks](./notebooks) directory.


## Local Setup - Development

For local development, you can run the GUEHDS Portal locally, the rest of the services will be running in Docker containers.

To start the GUEHDS Portal web app, use:

```bash
uvicorn governance_ui.app:app
```

The web app will be accessible at `http://guehds.local.promptly.health`.
