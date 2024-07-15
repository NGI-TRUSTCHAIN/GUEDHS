const { ethers } = require("ethers");
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');
const path = require('path');

require('dotenv').config({ path: '../blockchain-api/.env' });

var express = require('express');
var router = express.Router();

const contractABI = require("../artifacts/contracts/GUEDHS.sol/GUEDHS.json");
const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS;
const JSON_RPC_URL = process.env.JSON_RPC_URL;
const provider = new ethers.providers.JsonRpcProvider(JSON_RPC_URL);
const signer = provider.getSigner();
const GUEDHS = new ethers.Contract(CONTRACT_ADDRESS, contractABI.abi, signer);

router.post("/list-data-users", async (req, res, next) => {
    /* 	#swagger.tags = ['Node User Management']
        #swagger.description = 'Endpoint to sign in a specific user' */
    try {
        const { dataCustodianId, nodeId }  = req.body;
        
        try {
            const tx = await GUEDHS.ListOperation(
                dataCustodianId, 
                nodeId,
                req.path);

            await tx.wait();
            console.info("[DEBUG] Logging list data users operation.");

            return res.status(200).json({ message: "Logged list data users successfully", transactionHash: tx.hash });
        } catch(error) {
            console.error("[ERROR] Failed to log list data users operation:", error);
            return res.status(404).json({ message: error.shortMessage });
        }   
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

router.post("/inspect-data-user", async (req, res, next) => {
    /* 	#swagger.tags = ['Node User Management']
        #swagger.description = 'Endpoint to sign in a specific user' */
    try {
        const { dataUserId, dataCustodianId, nodeId } = req.body;
        
        try {
            const tx = await GUEDHS.InspectOperation(
                dataUserId,
                dataCustodianId, 
                nodeId,
                req.path);

            await tx.wait();
            console.info("[DEBUG] Logging inspect data user operation.");

            return res.status(200).json({ message: "Logged inspect data user operation successfully", transactionHash: tx.hash });
        } catch(error) {
            console.error("[ERROR] Failed to log inspect data user operation:", error);
            return res.status(404).json({ message: error.shortMessage });
        }   
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

router.post("/create-data-user", async (req, res, next) => {
    /* 	#swagger.tags = ['Node User Management']
        #swagger.description = 'Endpoint to sign in a specific user' */
    try {
        const { dataUserId, dataCustodianId, nodeId } = req.body;
        
        try {
            const tx = await GUEDHS.CreateOperation(
                dataUserId,
                dataCustodianId, 
                nodeId,
                req.path);

            await tx.wait();
            console.info("[DEBUG] Logging create data user operation.");

            return res.status(200).json({ message: "Logged create data user operation successfully", transactionHash: tx.hash });
        } catch(error) {
            console.error("[ERROR] Failed to log create data user operation:", error);
            return res.status(404).json({ message: error.shortMessage });
        }   
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

router.post("/delete-data-user", async (req, res, next) => {
    /* 	#swagger.tags = ['Node User Management']
        #swagger.description = 'Endpoint to sign in a specific user' */
    try {
        const { dataUserId, dataCustodianId, nodeId } = req.body;
        
        try {
            const tx = await GUEDHS.DeleteOperation(
                dataUserId,
                dataCustodianId, 
                nodeId,
                req.path);

            await tx.wait();
            console.info("[DEBUG] Logging delete data user operation.");

            return res.status(200).json({ message: "Logged delete data user operation successfully", transactionHash: tx.hash });
        } catch(error) {
            console.error("[ERROR] Failed to log delete data user operation:", error);
            return res.status(404).json({ message: error.shortMessage });
        }   
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

module.exports = router;