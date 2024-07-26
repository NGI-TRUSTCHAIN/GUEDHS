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

router.post("/list-data-op-rule", async (req, res, next) => {
    /* 	#swagger.tags = ['Data Operation Rule']
        #swagger.description = 'Logs the listing of a data operation rule by the data custodian on its FHDN node'
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
            console.info("[DEBUG] Logging list data operation rule.");

            return res.status(200).json({ message: "Logged list data operation successfully", transactionHash: tx.hash });
        } catch(error) {
            console.error("[ERROR] Failed to log list data operation rule:", error);
            return res.status(404).json({ message: error.shortMessage });
        }   
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

router.post("/inspect-data-op-rule", async (req, res, next) => {
    /* 	#swagger.tags = ['Data Operation Rule']
        #swagger.description = 'Logs the inspection of a data operation rule by the data custodian on its FHDN node'
        #swagger.requestBody = {
            required: true,
            content: {
                "application/json": {
                    schema: {
                        $ref: "#/components/schemas/dataOpSpecificOperation"
                    }  
                }
            }
        } 
    */
    try {
        const { dataOpId, dataCustodianId, nodeId } = req.body;
        
        try {
            const tx = await GUEDHS.InspectOperation(
                dataOpId,
                dataCustodianId, 
                nodeId,
                req.path);

            await tx.wait();
            console.info("[DEBUG] Logging inspect data operation rule.");

            return res.status(200).json({ message: "Logged inspect data operation rule successfully", transactionHash: tx.hash });
        } catch(error) {
            console.error("[ERROR] Failed to log inspect data operation rule:", error);
            return res.status(404).json({ message: error.shortMessage });
        }   
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

router.post("/create-data-op-rule", async (req, res, next) => {
    /* 	#swagger.tags = ['Data Operation Rule']
        #swagger.description = 'Logs the creation of a data operation rule by the data custodian on its FHDN node'
        #swagger.requestBody = {
            required: true,
            content: {
                "application/json": {
                    schema: {
                        $ref: "#/components/schemas/dataOpSpecificOperation"
                    }  
                }
            }
        } 
    */
    try {
        const { dataOpId, dataCustodianId, nodeId } = req.body;
        
        try {
            const tx = await GUEDHS.CreateOperation(
                dataOpId,
                dataCustodianId, 
                nodeId,
                req.path);

            await tx.wait();
            console.info("[DEBUG] Logging create data operation rule.");

            return res.status(200).json({ message: "Logged create data operation rule successfully", transactionHash: tx.hash });
        } catch(error) {
            console.error("[ERROR] Failed to log create data operation rule:", error);
            return res.status(404).json({ message: error.shortMessage });
        }   
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

router.post("/update-data-op-rule", async (req, res, next) => {
    /* 	#swagger.tags = ['Data Operation Rule']
        #swagger.description = 'Logs the update of a data operation rule by the data custodian on its FHDN node'
        #swagger.requestBody = {
            required: true,
            content: {
                "application/json": {
                    schema: {
                        $ref: "#/components/schemas/dataOpSpecificUpdateOperation"
                    }  
                }
            }
        } 
    */
    try {
        const { dataOpId, dataCustodianId, nodeId, status } = req.body;
        
        try {
            const tx = await GUEDHS.UpdateOperation(
                dataOpId,
                status,
                dataCustodianId, 
                nodeId,
                req.path);

            await tx.wait();
            console.info("[DEBUG] Logging update data operation rule.");

            return res.status(200).json({ message: "Logged update data operation rule successfully", transactionHash: tx.hash });
        } catch(error) {
            console.error("[ERROR] Failed to log update data operation rule:", error);
            return res.status(404).json({ message: error.shortMessage });
        }   
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

router.post("/remove-data-op-rule", async (req, res, next) => {
    /* 	#swagger.tags = ['Data Operation Rule']
        #swagger.description = 'Logs the removal of a data operation rule by the data custodian on its FHDN node'
        #swagger.requestBody = {
            required: true,
            content: {
                "application/json": {
                    schema: {
                        $ref: "#/components/schemas/dataOpSpecificOperation"
                    }  
                }
            }
        } 
    */
    try {
        const { dataOpId, dataCustodianId, nodeId } = req.body;
        
        try {
            const tx = await GUEDHS.DeleteOperation(
                dataOpId,
                dataCustodianId, 
                nodeId,
                req.path);

            await tx.wait();
            console.info("[DEBUG] Logging delete data operation rule.");

            return res.status(200).json({ message: "Logged delete data operation rule successfully", transactionHash: tx.hash });
        } catch(error) {
            console.error("[ERROR] Failed to log delete data operation rule:", error);
            return res.status(404).json({ message: error.shortMessage });
        }   
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

module.exports = router;