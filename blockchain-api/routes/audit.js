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
        dataCustodianId: action.ids.dataCustodianUUID,
        nodeId: action.ids.nodeUUID,
        timestamp: new Date(action.ids.timestamp * 1000).toString(),
        action: action.ids.action
    };

    if (action.ids.action.includes("dataset")) {
        parsedAction.datasetId = action.uuid || "N/A";
    } else if (action.ids.action.includes("access")) {
        parsedAction.accessId = action.uuid || "N/A";
    } else if (action.ids.action.includes("data-user")) {
        parsedAction.dataUserId = action.uuid || "N/A";
    } else {
        parsedAction.dataOpId = action.uuid || "N/A";
    }

    return parsedAction;
}

router.get("/list-operation", async (req, res) => {
    /* 	#swagger.tags = ['Auditing']
        #swagger.description = 'Endpoint to retrieve all the list operations of a data custodian'
    */
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
    /* 	#swagger.tags = ['Auditing']
        #swagger.description = 'Endpoint to retrieve all the inspect operations of a data custodian' 
    */
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
    /* 	#swagger.tags = ['Auditing']
        #swagger.description = 'Endpoint to retrieve all the create/publish operations of a data custodian'
    */
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
    /* 	#swagger.tags = ['Auditing']
        #swagger.description = 'Endpoint to retrieve all the update operations of a data custodian' 
    */
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
    /* 	#swagger.tags = ['Auditing']
        #swagger.description = 'Endpoint to retrieve all the delete/remove operations of a data custodian'
    */
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
    /* 	#swagger.tags = ['Auditing']
        #swagger.description = 'Endpoint to retrieve all the operations of a data custodian' 
    */
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