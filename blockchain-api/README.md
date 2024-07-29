# Blockchain API

This project demonstrates a basic Hardhat use case. It comes with a sample contract, a test for that contract, and a Hardhat Ignition module that deploys that contract.

Try running some of the following tasks:

## Requirements

- Docker
- Node

## Run for testing

All the components have been dockerized, so to run the API for testing purposes you simply have to run the following command:

```bash
docker-compose up -d
```

This will start all the required services, and you will be able to observe the logs of the `test-runner` container to validate the unit test results.

The API will also be operational on `localhost:3000`, and you can access the swagger documentation on `localhost:3000/docs` and experiment with the endpoints.

## Run for development

1. Install the packages needed to run the API

```bash
npm install
```

2. Setup and run the blockchain node

```bash
  docker-compose up -d blockchain-node
```

3. Deploy the smart contract onto the blockchain node

    ```bash
    npx hardhat run scripts/deploy.js --network localhost
    ```

    The response should be: 
    ```bash
    GUEDHS deployed to: "<CONTRACT_ADDRESS>"
    ```

4. Rename the sample.env file to .env
    
    4.1. Copy the contract address to the .env file and paste to the CONTRACT_ADDRESS variable

5. Run the WebAPI locally
```bash
  npm start
```

6. Access the swagger 

``` 
localhost:3000/docs 
```