// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";

contract GUEDHS is Ownable {
    
    constructor(address initialOwner) Ownable(initialOwner) {}

    enum STATUS {REQUESTED, GRANTED, REJECTED, REVOKED, CREATED, DELETED}
    
    struct StaticIdentifiers {
        string dataCustodianUUID;
        string nodeUUID;
        uint256 timestamp;
        string action;
    }

    struct ListAction {
        StaticIdentifiers ids;
    }

    struct InspectAction {
        string uuid;
        StaticIdentifiers ids;
    }

    struct CreateAction {
        string uuid;
        StaticIdentifiers ids;
    }
    
    struct UpdateAction {
        string uuid;
        STATUS status;
        StaticIdentifiers ids;
    }
    
    struct DeleteAction {
        string uuid;
        StaticIdentifiers ids;
    }

    struct LogEvents {
        ListAction[] listActions;
        InspectAction[] inspectActions;
        CreateAction[] createActions;
        UpdateAction[] updateActions;
        DeleteAction[] deleteActions;
    }
    
    LogEvents logEvents;

    event LoggingAction(string indexed dataCustodianId, string indexed nodeId, string indexed action);

    function getStatusFromString(string memory status) public pure returns (STATUS) {
        bytes32 statusHash = keccak256(abi.encodePacked(status));

        if (statusHash == keccak256(abi.encodePacked("granted"))) {
            return STATUS.GRANTED;
        } else if (statusHash == keccak256(abi.encodePacked("rejected"))) {
            return STATUS.REJECTED;
        } else if (statusHash == keccak256(abi.encodePacked("revoked"))) {
            return STATUS.REVOKED;
        } else {
            revert("Invalid status string");
        }
    }

    function compareStrings(
        string memory _a, 
        string memory _b) 
    public pure returns(bool) {
        return keccak256(abi.encodePacked(_a)) == keccak256(abi.encodePacked(_b));
    }

    function ListOperation(
        string memory _dataCustodianUUID,
        string memory _nodeUUID,
        string memory _action
    ) public {
        
        StaticIdentifiers memory newStaticIdentifier = StaticIdentifiers({
            dataCustodianUUID: _dataCustodianUUID,
            nodeUUID: _nodeUUID,
            timestamp: block.timestamp,
            action: _action
        });

        ListAction memory newListAction = ListAction({
            ids: newStaticIdentifier
        });

        logEvents.listActions.push(newListAction);
        emit LoggingAction(_dataCustodianUUID, _nodeUUID, _action);
    }

    function InspectOperation(
        string memory _uuid,
        string memory _dataCustodianUUID,
        string memory _nodeUUID,
        string memory _action
    ) public {
        
        StaticIdentifiers memory newStaticIdentifier = StaticIdentifiers({
            dataCustodianUUID: _dataCustodianUUID,
            nodeUUID: _nodeUUID,
            timestamp: block.timestamp,
            action: _action
        });

        InspectAction memory newInspectAction = InspectAction({
            uuid: _uuid,
            ids: newStaticIdentifier
        });

        logEvents.inspectActions.push(newInspectAction);
        emit LoggingAction(_dataCustodianUUID, _nodeUUID, _action);
    }

    function CreateOperation(
        string memory _uuid,
        string memory _dataCustodianUUID,
        string memory _nodeUUID,
        string memory _action
    ) public {
        
        StaticIdentifiers memory newStaticIdentifier = StaticIdentifiers({
            dataCustodianUUID: _dataCustodianUUID,
            nodeUUID: _nodeUUID,
            timestamp: block.timestamp,
            action: _action
        });

        CreateAction memory newCreateAction = CreateAction({
            uuid: _uuid,
            ids: newStaticIdentifier
        });

        logEvents.createActions.push(newCreateAction);
        emit LoggingAction(_dataCustodianUUID, _nodeUUID, _action);
    }

    function DeleteOperation(
        string memory _uuid,
        string memory _dataCustodianUUID,
        string memory _nodeUUID,
        string memory _action
    ) public {
        
        StaticIdentifiers memory newStaticIdentifier = StaticIdentifiers({
            dataCustodianUUID: _dataCustodianUUID,
            nodeUUID: _nodeUUID,
            timestamp: block.timestamp,
            action: _action
        });

        DeleteAction memory newDeleteAction = DeleteAction({
            uuid: _uuid,
            ids: newStaticIdentifier
        });

        logEvents.deleteActions.push(newDeleteAction);
        emit LoggingAction(_dataCustodianUUID, _nodeUUID, _action);
    }

    function UpdateOperation(
        string memory _uuid,
        string memory _status,
        string memory _dataCustodianUUID,
        string memory _nodeUUID,
        string memory _action
    ) public {
        
        StaticIdentifiers memory newStaticIdentifier = StaticIdentifiers({
            dataCustodianUUID: _dataCustodianUUID,
            nodeUUID: _nodeUUID,
            timestamp: block.timestamp,
            action: _action
        });

        UpdateAction memory newUpdateAction = UpdateAction({
            uuid: _uuid,
            status: getStatusFromString(_status),
            ids: newStaticIdentifier
        });

        logEvents.updateActions.push(newUpdateAction);
        emit LoggingAction(_dataCustodianUUID, _nodeUUID, _action);
    }

    function GetLogs() public view returns (LogEvents memory) {
        return logEvents;
    }
}
