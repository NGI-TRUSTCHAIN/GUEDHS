const { ethers } = require("ethers");

require('dotenv').config({ path: '../blockchain-api/.env' });

var express = require('express');
var router = express.Router();

const contractABI = require("../artifacts/contracts/GUEDHS.sol/GUEDHS.json");
const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS;
const JSON_RPC_URL = process.env.JSON_RPC_URL;
const PRIVATE_KEY = process.env.PRIVATE_KEY;
const provider = new ethers.providers.JsonRpcProvider(JSON_RPC_URL);
const signer = new ethers.Wallet(PRIVATE_KEY, provider);
const GUEDHS = new ethers.Contract(CONTRACT_ADDRESS, contractABI.abi, signer);

router.post("/list-datasets", async (req, res, next) => {
    /* 	#swagger.tags = ['Datasets']
        #swagger.description = 'Logs the listing of a dataset by the data custodian on its FHDN node'
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
            console.info("[DEBUG] Logging listing dataset operation.");

            return res.status(200).json({ message: "Logged list dataset successfully", transactionHash: tx.hash });
        } catch(error) {
            console.error("[ERROR] Failed to log list dataset operation:", error);
            return res.status(404).json({ message: error.shortMessage });
        }   
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

router.post("/inspect-dataset", async (req, res, next) => {
    /* 	#swagger.tags = ['Datasets']
        #swagger.description = 'Logs the inspection of a dataset by the data custodian on its FHDN node'
        #swagger.requestBody = {
            required: true,
            content: {
                "application/json": {
                    schema: {
                        $ref: "#/components/schemas/datasetSpecificOperation"
                    }  
                }
            }
        } 
    */
    try {
        const { datasetId, dataCustodianId, nodeId } = req.body;
        
        try {
            const tx = await GUEDHS.InspectOperation(
                datasetId,
                dataCustodianId, 
                nodeId,
                req.path);

            await tx.wait();
            console.info("[DEBUG] Logging inspect dataset operation.");

            return res.status(200).json({ message: "Logged inspect dataset successfully", transactionHash: tx.hash });
        } catch(error) {
            console.error("[ERROR] Failed to log inspect dataset operation:", error);
            return res.status(404).json({ message: error.shortMessage });
        }   
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

router.post("/publish-dataset", async (req, res, next) => {
    /* 	#swagger.tags = ['Datasets']
        #swagger.description = 'Logs the publishing of a dataset by the data custodian on its FHDN node'
        #swagger.requestBody = {
            required: true,
            content: {
                "application/json": {
                    schema: {
                        $ref: "#/components/schemas/datasetSpecificOperation"
                    }  
                }
            }
        } 
    */
    try {
        const { datasetId, dataCustodianId, nodeId } = req.body;
        
        try {
            const tx = await GUEDHS.CreateOperation(
                datasetId,
                dataCustodianId, 
                nodeId,
                req.path);

            await tx.wait();
            console.info("[DEBUG] Logging create dataset operation.");

            return res.status(200).json({ message: "Logged create dataset successfully", transactionHash: tx.hash });
        } catch(error) {
            console.error("[ERROR] Failed to log create dataset operation:", error);
            return res.status(404).json({ message: error.shortMessage });
        }   
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

router.post("/remove-dataset", async (req, res, next) => {
    /* 	#swagger.tags = ['Datasets']
        #swagger.description = 'Logs the removal of a dataset by the data custodian on its FHDN node'
        #swagger.requestBody = {
            required: true,
            content: {
                "application/json": {
                    schema: {
                        $ref: "#/components/schemas/datasetSpecificOperation"
                    }  
                }
            }
        } 
    */
    try {
        const { datasetId, dataCustodianId, nodeId } = req.body;
        
        try {
            const tx = await GUEDHS.DeleteOperation(
                datasetId,
                dataCustodianId, 
                nodeId,
                req.path);

            await tx.wait();
            console.info("[DEBUG] Logging delete dataset operation.");

            return res.status(200).json({ message: "Logged delete dataset successfully", transactionHash: tx.hash });
        } catch(error) {
            console.error("[ERROR] Failed to log delete dataset operation:", error);
            return res.status(404).json({ message: error.shortMessage });
        }   
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

module.exports = router;