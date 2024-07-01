// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";

contract GUEDHS is Ownable {
    
    constructor(address initialOwner) Ownable(initialOwner) {}

    enum STATUS {REQUESTED, GRANTED, DENIED}
    
    struct Permission {
        string uuid;
        STATUS status;
        uint256 createdAt;
        string dataUserUUID;
        string dataCustodianUUID;
    }
    
    struct User {
        string uuid;
        string[] permissionIds;
    }

    mapping(string => User) dataUsers;
    mapping(string => User) dataCustodians;
    mapping(string => Permission) public permissions;

    event LogPermission(STATUS status, string uuid, string dataCustodian, string dataUsers);

    function GetPermission(string memory _permissionUUID) public view returns (Permission memory) {
        return permissions[_permissionUUID];
    }

    function RequestPermission(
        string memory _permissionUUID, 
        string memory _dataUserUUID, 
        string memory _dataCustodianUUID
    ) public {
        
        Permission memory newPermission = Permission({
            uuid: _permissionUUID,
            status: STATUS.REQUESTED,
            createdAt: block.timestamp,
            dataUserUUID: _dataUserUUID,
            dataCustodianUUID: _dataCustodianUUID
        });
        dataUsers[_dataUserUUID].permissionIds.push(_permissionUUID);
        dataCustodians[_dataCustodianUUID].permissionIds.push(_permissionUUID);
        permissions[_permissionUUID] = newPermission;
    }

    function GrantPermission(string memory _permissionUUID) public {
        Permission storage newPermission = permissions[_permissionUUID];
        require(newPermission.status == STATUS.REQUESTED, "Permission must have requested status!");
        newPermission.status = STATUS.GRANTED;
        permissions[_permissionUUID] = newPermission;
    }
    
    function DenyPermission(string memory _permissionUUID) public {
        Permission storage newPermission = permissions[_permissionUUID];
        require(newPermission.status == STATUS.REQUESTED, "Permission must have requested status!");
        newPermission.status = STATUS.DENIED;
        permissions[_permissionUUID] = newPermission;
    }

    function CheckPermissions(string memory _dataCustodianUUID) public view returns (Permission[] memory){
        string[] memory permissionIds = dataCustodians[_dataCustodianUUID].permissionIds;
        Permission[] memory listOfPermissions = new Permission[](permissionIds.length);
        for (uint i = 0; i < permissionIds.length; i++) {
            listOfPermissions[i] = permissions[permissionIds[i]];
        }
        return listOfPermissions;
    }
}
