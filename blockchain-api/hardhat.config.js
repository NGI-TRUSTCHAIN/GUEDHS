require("@nomiclabs/hardhat-ethers");
require("@nomicfoundation/hardhat-verify")
require("@nomicfoundation/hardhat-chai-matchers")
require("dotenv").config();

const { PRIVATE_KEY, JSON_RPC_URL } = process.env;

module.exports = {
  solidity: "0.8.24", // Adjust the version according to your contract's pragma version
  defaultNetwork: "localhost",
  networks: {
    localhost: {
      allowUnlimitedContractSize: true,
      url: JSON_RPC_URL,
      accounts: [`0x${PRIVATE_KEY}`]
    }
  }
};
