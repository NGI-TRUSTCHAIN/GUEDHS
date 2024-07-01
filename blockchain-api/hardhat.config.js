require("@nomiclabs/hardhat-ethers");
require("@nomicfoundation/hardhat-verify")
require("@nomicfoundation/hardhat-chai-matchers")
require("dotenv").config();

const LOCAL_DEV_URL = process.env.LOCAL_DEV_URL;
const API_URL = process.env.API_URL;
const PRIVATE_KEY = process.env.PRIVATE_KEY;
const ETHERSCAN_API_KEY = process.env.ETHERSCAN_API_KEY;

module.exports = {
  solidity: "0.8.24", // Adjust the version according to your contract's pragma version
  defaultNetwork: "localhost",
  networks: {
    localhost: {
      url: LOCAL_DEV_URL
    },
    polygonAmoy: {
      allowUnlimitedContractSize: true,
      url: API_URL,
      accounts: [`0x${PRIVATE_KEY}`]
    }
  },
  etherscan: {
    apiKey: ETHERSCAN_API_KEY,
    customChains: [
      {
        network: "polygonAmoy",
        chainId: 80002,
        urls: {
          apiURL:
            "https://api-amoy.polygonscan.com/api",
          browserURL: "https://amoy.polygonscan.com/",
        },
      },
    ],
  },
  sourcify: {
    enabled: true
  }
};
