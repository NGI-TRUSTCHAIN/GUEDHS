# GUEHDS Federated Network

Example federated network for the GUEHDS project. Built using [PySyft](https://github.com/OpenMined/PySyft).

## Installation

First, install [Poetry](https://python-poetry.org/). Then install the project using:

```bash
poetry install
```

## Setup Database

Navigate to the database directory:

```bash
cd governance_ui/db
```

Apply the migrations to the database:

```bash
prisma migrate deploy
```

Generate the Prisma Client:

```bash
prisma generate
```

Populate the database:

```bash
python populate_db.py
```

## Setup Network

Start the network using:

```bash
hagrid launch gateway
```

This will start a PyGrid gateway at `http://localhost:8081`.

Then, deploy domain nodes using:

```bash
hagrid launch domain
```

This will start a PyGrid domain node at `http://localhost:8082`. If you wish, repeat this command to start more domain nodes.

## Usage

Follow the examples in the [notebooks](./notebooks) directory to see how to interact with the network.

You can also start the example webapp using:

```bash
uvicorn governance_ui.app:app
```
