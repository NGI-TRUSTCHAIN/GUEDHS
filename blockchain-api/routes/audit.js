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

function filterLogs(logActions, dataCustodianId, nodeId) {
    if (!dataCustodianId || !nodeId) {
        return logActions;
    }

    return logActions.filter(action =>
        action.ids.dataCustodianUUID === dataCustodianId &&
        action.ids.nodeUUID === nodeId
    );
}

function mapStatus(status) {
    result = ["Requested", "Granted", "Rejected", "Revoked", "Created", "Deleted"];
    return result[status];
}

function parseLog(action) {
    let parsedAction = {
        status: mapStatus(action.status) || "N/A",
        dataCustodianUUID: action.ids.dataCustodianUUID,
        nodeUUID: action.ids.nodeUUID,
        timestamp: new Date(action.ids.timestamp * 1000).toString(),
        action: action.ids.action
    };

    if (action.ids.action.includes("dataset")) {
        parsedAction.datasetUUID = action.uuid || "N/A";
    } else if (action.ids.action.includes("access")) {
        parsedAction.accessUUID = action.uuid || "N/A";
    } else if (action.ids.action.includes("data-user")) {
        parsedAction.dataUserUUID = action.uuid || "N/A";
    } else {
        parsedAction.uuid = action.uuid || "N/A";
    }

    return parsedAction;
}

router.get("/list-operation", async (req, res) => {
    try {
        const { dataCustodianId, nodeId } = req.query;
        const logEvents = await GUEDHS.GetLogs();
        const filteredLogs = filterLogs(logEvents.listActions, dataCustodianId, nodeId);
        const parsedLogs = filteredLogs.map(parseLog);

        return res.status(200).json({ listActions: parsedLogs });
    } catch (error) {
        console.error("[ERROR] Failed to retrieve list operation logs:", error);
        return res.status(500).json({ message: error.message });
    }
});

router.get("/inspect-operation", async (req, res) => {
    try {
        const { dataCustodianId, nodeId } = req.query;
        const logEvents = await GUEDHS.GetLogs();
        const filteredLogs = filterLogs(logEvents.inspectActions, dataCustodianId, nodeId);
        const parsedLogs = filteredLogs.map(parseLog);

        return res.status(200).json({ inspectActions: parsedLogs });
    } catch (error) {
        console.error("[ERROR] Failed to retrieve inspect operation logs:", error);
        return res.status(500).json({ message: error.message });
    }
});

router.get("/create-operation", async (req, res) => {
    try {
        const { dataCustodianId, nodeId } = req.query;
        const logEvents = await GUEDHS.GetLogs();
        const filteredLogs = filterLogs(logEvents.createActions, dataCustodianId, nodeId);
        const parsedLogs = filteredLogs.map(parseLog);

        return res.status(200).json({ createActions: parsedLogs });
    } catch (error) {
        console.error("[ERROR] Failed to retrieve create operation logs:", error);
        return res.status(500).json({ message: error.message });
    }
});

router.get("/update-operation", async (req, res) => {
    try {
        const { dataCustodianId, nodeId } = req.query;
        const logEvents = await GUEDHS.GetLogs();
        const filteredLogs = filterLogs(logEvents.updateActions, dataCustodianId, nodeId);
        const parsedLogs = filteredLogs.map(parseLog);

        return res.status(200).json({ updateActions: parsedLogs });
    } catch (error) {
        console.error("[ERROR] Failed to retrieve update operation logs:", error);
        return res.status(500).json({ message: error.message });
    }
});

router.get("/delete-operation", async (req, res) => {
    try {
        const { dataCustodianId, nodeId } = req.query;
        const logEvents = await GUEDHS.GetLogs();
        const filteredLogs = filterLogs(logEvents.deleteActions, dataCustodianId, nodeId);
        const parsedLogs = filteredLogs.map(parseLog);

        return res.status(200).json({ deleteActions: parsedLogs });
    } catch (error) {
        console.error("[ERROR] Failed to retrieve delete operation logs:", error);
        return res.status(500).json({ message: error.message });
    }
});

router.get("/all-operations", async (req, res) => {
    try {
        const { dataCustodianId, nodeId } = req.query;
        const logEvents = await GUEDHS.GetLogs();

        const filteredListLogs = filterLogs(logEvents.listActions, dataCustodianId, nodeId).map(parseLog);
        const filteredInspectLogs = filterLogs(logEvents.inspectActions, dataCustodianId, nodeId).map(parseLog);
        const filteredCreateLogs = filterLogs(logEvents.createActions, dataCustodianId, nodeId).map(parseLog);
        const filteredUpdateLogs = filterLogs(logEvents.updateActions, dataCustodianId, nodeId).map(parseLog);
        const filteredDeleteLogs = filterLogs(logEvents.deleteActions, dataCustodianId, nodeId).map(parseLog);

        return res.status(200).json({
            listActions: filteredListLogs,
            inspectActions: filteredInspectLogs,
            createActions: filteredCreateLogs,
            updateActions: filteredUpdateLogs,
            deleteActions: filteredDeleteLogs
        });
    } catch (error) {
        console.error("[ERROR] Failed to retrieve all operation logs:", error);
        return res.status(500).json({ message: error.message });
    }
});

module.exports = router;