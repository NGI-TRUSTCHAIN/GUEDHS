# GUEHDS Federated Network

Example federated network for the GUEHDS project. Built using [PySyft](https://github.com/OpenMined/PySyft).

## Installation

First, install [Poetry](https://python-poetry.org/). Then install the project using:

```bash
poetry install
```

## Setup

Start the network using:

```bash
hagrid deploy gateway
```

This will start a PyGrid gateway at `http://localhost:8081`.

Then, deploy domain nodes using:

```bash
hagrid deploy domain
```

This will start a PyGrid domain node at `http://localhost:8082`. If you wish, repeat this command to start more domain nodes.

## Usage

Follow the examples in the [notebooks](./notebooks) directory to see how to interact with the network.

You can also start the example webapp using:

```bash
streamlit run ui/guehds.py
```
