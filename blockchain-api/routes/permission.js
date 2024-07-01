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

function mapStatus(status) {
    const statusMapping = ["REQUESTED", "GRANTED", "DENIED"];
    return statusMapping[status];
}

router.post("/request-permission", async (req, res, next) => {
    try {
        const permissionUUID = uuidv4();
        const {dataUserUUID, dataCustodianUUID} = req.body;
        console.log("PermissionUUID: ", permissionUUID);
        console.log("Data User UUID: ", dataUserUUID);
        console.log("Data Custodian UUID: ", dataCustodianUUID);
        const GUEDHS = new ethers.Contract(CONTRACT_ADDRESS, contractABI.abi, signer);
        console.log("Signer: ", signer);
        console.log("Provider:", provider);
        try {
            const tx = await GUEDHS.RequestPermission(permissionUUID, dataUserUUID, dataCustodianUUID);
            await tx.wait(); // Wait for the transaction to be mined
            console.info("[DEBUG] Permission requested:", tx);

            return res.status(201).json({ permissionUUID: permissionUUID, message: "Permission requested successfully", transactionHash: tx.hash });
        } catch (error) {
            console.error("[ERROR] Failed to request permission:", error);
            return res.status(400).json({ message: "Failed to request permission", error: error.message });
        }
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

router.post("/grant-permission", async (req, res, next) => {
    try {
        const { permissionUUID } = req.body;
        console.log("PermissionUUID: ", permissionUUID);
        const GUEDHS = new ethers.Contract(CONTRACT_ADDRESS, contractABI.abi, signer);

        try {
            const tx = await GUEDHS.GrantPermission(permissionUUID);
            await tx.wait(); // Wait for the transaction to be mined
            console.info("[DEBUG] Permission granted:", tx);

            return res.status(201).json({ message: "Permission granted successfully", transactionHash: tx.hash });
        } catch (error) {
            console.error("[ERROR] Failed to grant permission:", error);
            return res.status(400).json({ message: "Failed to grant permission", error: error.message });
        }
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

router.post("/deny-permission", async (req, res, next) => {
    try {
        const { permissionUUID } = req.body;
        console.log("PermissionUUID: ", permissionUUID);
        const GUEDHS = new ethers.Contract(CONTRACT_ADDRESS, contractABI.abi, signer);

        try {
            const tx = await GUEDHS.DenyPermission(permissionUUID);
            await tx.wait(); // Wait for the transaction to be mined
            console.info("[DEBUG] Permission denied:", tx);

            return res.status(201).json({ message: "Permission denied successfully", transactionHash: tx.hash });
        } catch (error) {
            console.error("[ERROR] Failed to deny permission:", error.code);
            return res.status(500).json({ message: "Failed to deny permission", error: error.shortMessage });
        }
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

router.get("/get-permission", async (req, res) => {
    try {
        const permissionUUID = req.query.permissionUUID;
        console.log(`Requesting permission for UUID: ${permissionUUID}`);

        const GUEDHS = new ethers.Contract(CONTRACT_ADDRESS, contractABI.abi, provider);
        
        try {
            const permission = await GUEDHS.GetPermission(permissionUUID);
            console.info("[DEBUG] Retrieved permission.");
            if (permission.uuid === "") {
                return res.status(404).json({ message: "Permission not found" });
            }
            // Parse the returned tuple to an object
            const parsedPermission = {
                uuid: permission[0],
                status: mapStatus(permission[1]),
                createdAt: permission[2].toNumber(),
                dataUserUUID: permission[3],
                dataCustodianUUID: permission[4],
            };

            return res.status(200).json({ permission: parsedPermission});
        } catch(error) {
            console.error("[ERROR] Failed to retrieve permission:", error);
            return res.status(404).json({ message: error.shortMessage });
        }   
    } catch (error) {
        console.error(error.shortMessage);
        return res.status(500).json({message: error.shortMessage});
    }
});

module.exports = router;