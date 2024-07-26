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

function connectWithPrivateKey(privateKey) {
    const userWallet = new ethers.Wallet(privateKey, provider);
    return GUEDHS.connect(userWallet);
}

router.post("/list-access", async (req, res) => {
    /* 	#swagger.tags = ['Code Request Review']
        #swagger.description = 'Logs the listing of a data access requests by the data custodian on its FHDN node'
        #swagger.requestBody = {
            required: true,
            content: {
                "application/json": {
                    schema: {
                        $ref: "#/components/schemas/listOperation"
                    }  
                }
            }
        } 
    */
    try {
        const { dataCustodianId, nodeId }  = req.body;
        
        try {
            
            const tx = await GUEDHS.ListOperation(
                dataCustodianId, 
                nodeId,
                req.path);

            await tx.wait();
            console.info("[DEBUG] Logging list access operation.");

            return res.status(200).json({ message: "Logged list access successfully", transactionHash: tx.hash });
        } catch(error) {
            console.error("[ERROR] Failed to log list access operation:", error);
            return res.status(404).json({ message: error.shortMessage });
        }   
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

router.post("/inspect-access", async (req, res) => {
    /* 	#swagger.tags = ['Code Request Review']
        #swagger.description = 'Logs the inspection of a data access request by the data custodian on its FHDN node' 
        #swagger.requestBody = {
            required: true,
            content: {
                "application/json": {
                    schema: {
                        $ref: "#/components/schemas/accessSpecificOperation"
                    }  
                }
            }
        } 
    */
    try {
        const { accessId, dataCustodianId, nodeId } = req.body;
        
        try {
            const tx = await GUEDHS.InspectOperation(
                accessId,
                dataCustodianId, 
                nodeId,
                req.path);

            await tx.wait();
            console.info("[DEBUG] Logging inspect access operation.");

            return res.status(200).json({ message: "Logged inspect access operation successfully", transactionHash: tx.hash });
        } catch(error) {
            console.error("[ERROR] Failed to log inspect access operation:", error);
            return res.status(404).json({ message: error.shortMessage });
        }   
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

router.post("/request-access", async (req, res, next) => {
    /* 	#swagger.tags = ['Code Request Review']
        #swagger.description = 'Logs the data user requests for access in the data custodian's FHDN node'
        #swagger.requestBody = {
            required: true,
            content: {
                "application/json": {
                    schema: {
                        $ref: "#/components/schemas/accessSpecificOperation"
                    }  
                }
            }
        } 
    */
    try {
        const { accessId, dataCustodianId, nodeId } = req.body;
        
        try {
            const tx = await GUEDHS.CreateOperation(
                accessId,
                dataCustodianId, 
                nodeId,
                req.path);

            await tx.wait();
            console.info("[DEBUG] Logging request access operation.");

            return res.status(200).json({ message: "Logged request access operation successfully", transactionHash: tx.hash });
        } catch(error) {
            console.error("[ERROR] Failed to log request access operation:", error);
            return res.status(404).json({ message: error.shortMessage });
        }   
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

router.post("/update-access-request", async (req, res, next) => {
    /* 	#swagger.tags = ['Code Request Review']
        #swagger.description = 'Logs the data access request update by the data custodian on its FHDN node'
        #swagger.requestBody = {
            required: true,
            content: {
                "application/json": {
                    schema: {
                        $ref: "#/components/schemas/accessSpecificUpdateOperation"
                    }  
                }
            }
        } 
    */
    try {
        const { accessId, dataCustodianId, nodeId, status } = req.body;
        
        try {
            const tx = await GUEDHS.UpdateOperation(
                accessId,
                status,
                dataCustodianId, 
                nodeId,
                req.path);

            await tx.wait();
            console.info("[DEBUG] Logging update access operation.");

            return res.status(200).json({ message: "Logged update access operation successfully", transactionHash: tx.hash });
        } catch(error) {
            console.error("[ERROR] Failed to log update access operation:", error);
            return res.status(404).json({ message: error.shortMessage });
        }   
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

module.exports = router;