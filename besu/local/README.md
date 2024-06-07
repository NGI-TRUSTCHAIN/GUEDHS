# Local Besu Setup

Simple 4 node Besu network setup using docker-compose.

## Start the network

```bash
bash start.sh
```

Test the network by connecting to the nodes using the following ports:

- Node 1: `http://localhost:11045`
- Node 2: `http://localhost:12045`
- Node 3: `http://localhost:13045`
- Node 4: `http://localhost:14045`

You can use the [testing accounts provided by Besu](https://besu.hyperledger.org/private-networks/reference/accounts-for-testing) to simulate transactions.