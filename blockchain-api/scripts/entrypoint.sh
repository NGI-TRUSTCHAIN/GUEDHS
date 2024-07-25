#!/bin/sh

# Any setup or initialization commands can go here

export CONTRACT_ADDRESS=$(npx hardhat run scripts/deploy.js --network localhost | grep -oE '0x[a-fA-F0-9]+')

# Start the main process
npm run swagger
