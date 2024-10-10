# Blockchain API

This project demonstrates a basic Hardhat use case. It comes with a sample contract, a test for that contract, and a Hardhat Ignition module that deploys that contract.

Try running some of the following tasks:

## Requirements

- Docker
- Node
- Kubernetes (kubectl)
- Helm
- Kubernetes cluster

## Run the Blockchain API

1. Install the packages needed to run the API

```bash
npm install
```

2. Setup and run the blockchain node

```bash
  docker-compose build
  docker-compose up -d
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

5. Run the WebAPI
```bash
  npm start
```

6. Access the swagger 

``` 
localhost:3000/docs 
```

#Kubernetes - Helm

##Run the Blockchain API

1. Install the packages needed to run the API

```bash
npm install
```

2. Setup and run the blockchain node - replace "node" by the helm name intended and "namespace" with the desired namespace to deploy
```bash
  helm install "node" ./hardhat -n "namespace"
```
3. Grab contract address and private key via blockchain node logs - replace "pod_name_for_blockchain_node" with the pod name and "namespace" with the namespace where it is
```bash
  kubectl logs "pod_name_for_blockchain_node" -n "namespace"
```

4. Put contract address and private key on env via values.yaml of helm/values.yaml

5. Setup and run the blockchain api - replace "api" by the helm name intended and "namespace" with the desired namespace to deploy
```bash
  helm install "api" ./helm -n "namespace"
```

6. Open browser and go to "http://node-ip:30001/docs" and use the api - replace "nodeip" with the actual ip address of the worker node where the api is running
