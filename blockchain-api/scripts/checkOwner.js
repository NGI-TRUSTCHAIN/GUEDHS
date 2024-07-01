require('dotenv').config({ path: '../blockchain-api/.env' });
const { ethers } = require("hardhat");

async function main() {
    // Fetch the contract address from the deployment log or hardcode if known
    const contractAddress = process.env.CONTRACT_ADDRESS;

    // We get the contract to interact with
    const GUEDHS = await ethers.getContractFactory("GUEDHS");
    const guedhs = GUEDHS.attach(contractAddress);

    // Call the owner function from Ownable contract
    const owner = await guedhs.owner();

    console.log("Owner of the GUEDHS contract:", owner);
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
