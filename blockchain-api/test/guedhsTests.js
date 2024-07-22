const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("GUEDHS Contract", function () {
  let GUEDHS;
  let guedhs;
  let owner;
  let addr1;

  beforeEach(async function () {
    GUEDHS = await ethers.getContractFactory("GUEDHS");
    [owner, addr1] = await ethers.getSigners();
    guedhs = await GUEDHS.deploy(owner.address);
    await guedhs.deployed();
  });

  it("Should initialize the contract with the correct owner", async function () {
    expect(await guedhs.owner()).to.equal(owner.address);
  });

  it("Should emit LoggingAction event on ListOperation", async function () {
    await expect(guedhs.ListOperation("custodianUUID", "nodeUUID", "action"))
      .to.emit(guedhs, "LoggingAction")
      .withArgs("custodianUUID", "nodeUUID", "action");
  });

  it("Should emit LoggingAction event on InspectOperation", async function () {
    await expect(
      guedhs.InspectOperation("uuid", "custodianUUID", "nodeUUID", "action")
    )
      .to.emit(guedhs, "LoggingAction")
      .withArgs("custodianUUID", "nodeUUID", "action");
  });

  it("Should emit LoggingAction event on CreateOperation", async function () {
    await expect(
      guedhs.CreateOperation("uuid", "custodianUUID", "nodeUUID", "action")
    )
      .to.emit(guedhs, "LoggingAction")
      .withArgs("custodianUUID", "nodeUUID", "action");
  });

  it("Should emit LoggingAction event on DeleteOperation", async function () {
    await expect(
      guedhs.DeleteOperation("uuid", "custodianUUID", "nodeUUID", "action")
    )
      .to.emit(guedhs, "LoggingAction")
      .withArgs("custodianUUID", "nodeUUID", "action");
  });

  it("Should emit LoggingAction event on UpdateOperation", async function () {
    await expect(
      guedhs.UpdateOperation("uuid", "granted", "custodianUUID", "nodeUUID", "action")
    )
      .to.emit(guedhs, "LoggingAction")
      .withArgs("custodianUUID", "nodeUUID", "action");
  });

  it("Should get correct status from string", async function () {
    expect(await guedhs.getStatusFromString("granted")).to.equal(1);
    expect(await guedhs.getStatusFromString("rejected")).to.equal(2);
    expect(await guedhs.getStatusFromString("revoked")).to.equal(3);
    await expect(guedhs.getStatusFromString("invalid")).to.be.revertedWith(
      "Invalid status string"
    );
  });

  it("Should compare strings correctly", async function () {
    expect(await guedhs.compareStrings("test", "test")).to.be.true;
    expect(await guedhs.compareStrings("test", "Test")).to.be.false;
  });

  it("Should store ListOperation logs correctly", async function () {
    await guedhs.ListOperation("custodianUUID", "nodeUUID", "action");
    const logs = await guedhs.GetLogs();
    expect(logs.listActions.length).to.equal(1);
    expect(logs.listActions[0].ids.dataCustodianUUID).to.equal("custodianUUID");
  });

  it("Should store InspectOperation logs correctly", async function () {
    await guedhs.InspectOperation("uuid", "custodianUUID", "nodeUUID", "action");
    const logs = await guedhs.GetLogs();
    expect(logs.inspectActions.length).to.equal(1);
    expect(logs.inspectActions[0].ids.dataCustodianUUID).to.equal("custodianUUID");
  });

  it("Should store CreateOperation logs correctly", async function () {
    await guedhs.CreateOperation("uuid", "custodianUUID", "nodeUUID", "action");
    const logs = await guedhs.GetLogs();
    expect(logs.createActions.length).to.equal(1);
    expect(logs.createActions[0].ids.dataCustodianUUID).to.equal("custodianUUID");
  });

  it("Should store DeleteOperation logs correctly", async function () {
    await guedhs.DeleteOperation("uuid", "custodianUUID", "nodeUUID", "action");
    const logs = await guedhs.GetLogs();
    expect(logs.deleteActions.length).to.equal(1);
    expect(logs.deleteActions[0].ids.dataCustodianUUID).to.equal("custodianUUID");
  });

  it("Should store UpdateOperation logs correctly", async function () {
    await guedhs.UpdateOperation("uuid", "granted", "custodianUUID", "nodeUUID", "action");
    const logs = await guedhs.GetLogs();
    expect(logs.updateActions.length).to.equal(1);
    expect(logs.updateActions[0].ids.dataCustodianUUID).to.equal("custodianUUID");
    expect(logs.updateActions[0].status).to.equal(1);
  });
});