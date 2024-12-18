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


## Demo Setup

### Project Setup

**Note:** Run all commands from the `federated_network` directory. You should have already followed the test setup guide for [blockchain-api](../blockchain-api/README.md).

1. Make sure you install the project dependencies as detailed above with `poetry install`.

2. Create a `.env` file in the root of the project with the following content, by copying the `.env.example` file:

    ```bash
    cp .env.example .env
    ```

3. Setup `/etc/hosts`:

    Add the following entries to your `/etc/hosts` file:

    ```
    127.0.0.1   auth.local.promptly.health
    127.0.0.1   guehds.local.promptly.health
    127.0.0.1   syft.local.promptly.health
    127.0.0.1   blockchain.local.promptly.health
    ```

4. To start the PyGrid domain network, run the following command:

    ```bash
    poetry run hagrid launch domain
    ```

    This will launch a PyGrid domain at `http://syft.local.promptly.health`.
    Make note of the name (in green in the CLI) that is given to the node, as you will need it for cleanup later.

5. Start the Docker Containers

    To set up and start the necessary services, run the following command:

    ```bash
    docker compose up -d
    ```

### Interacting as a Data Owner

To interact with the portal as a Data Owner, access the portal at `http://guehds.local.promptly.health` and login with the following credentials:

- **Username**: `info@openmined.org`
- **Password**: `changethis`

### Interacting as a Data Scientist

Explore and interact with the federated network as a Data Scientist by following the examples available in the [notebooks](./notebooks) directory.

### Cleaning up

You can clean up the setup by doing the following:

1. Run `docker compose down --volumes` to clear federated network containers.

2. Run `./remove_pysyft.sh [YOUR_PYSYFT_NODE_NAME]` to clear pysyft containers (you may need to run `chmod +x ./remove_pysyft.sh`).

3. Remove the added entries from your `/etc/hosts` file.

4. Follow the clean up guide on [blockchain-api](../blockchain-api/README.md).


## Development Setup

For local development, you can run the GUEHDS Portal locally, the rest of the services will be running in Docker containers.

To start the GUEHDS Portal web app, use:

```bash
uvicorn governance_ui.app:app
```

The web app will be accessible at `http://guehds.local.promptly.health`.
