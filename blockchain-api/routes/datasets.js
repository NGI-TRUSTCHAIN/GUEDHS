const { ethers } = require("ethers");
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');
const path = require('path');

require('dotenv').config({ path: '../blockchain-api/.env' });

var express = require('express');
var router = express.Router();

const contractABI = require("../artifacts/contracts/GUEDHS.sol/GUEDHS.json");
const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS;
const JSON_RPC_URL = process.env.ENVIRONMENT == "DEV" ? process.env.LOCAL_DEV_URL : process.env.API_URL;
const provider = new ethers.providers.JsonRpcProvider(JSON_RPC_URL);
const signer = provider.getSigner();