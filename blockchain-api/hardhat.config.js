require("@nomiclabs/hardhat-ethers");
require("@nomicfoundation/hardhat-verify")
require("@nomicfoundation/hardhat-chai-matchers")
require("dotenv").config();

const JSON_RPC_URL = process.env.JSON_RPC_URL;

module.exports = {
  solidity: "0.8.24", // Adjust the version according to your contract's pragma version
  defaultNetwork: "localhost",
  networks: {
    localhost: {
      url: JSON_RPC_URL
    }
  }
};
