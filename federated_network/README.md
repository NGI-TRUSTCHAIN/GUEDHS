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

1. Start the Docker Containers

    To set up and start the necessary services, run the following command:

    ```bash
    docker compose up -d
    ```

2. Populate the database:

    Once the Docker containers are up and running, populate the database with initial data by executing the following script:

    ```bash
    python governance_ui/db/populate_db.py
    ```

### Network Setup

1. To start the PyGrid domain network, run the following command:

    ```bash
    hagrid launch domain
    ```

    This will launch a PyGrid domain at `http://localhost:8081`.


## Usage

### GUEHDS Portal

To start the GUEHDS Portal web app, use:

```bash
uvicorn governance_ui.app:app
```

The web app will be accessible at `http://guehds.local.promptly.health`.

### Interacting as a Data Scientist

Explore and interact with the federated network as a Data Scientist by following the examples available in the [notebooks](./notebooks) directory.

