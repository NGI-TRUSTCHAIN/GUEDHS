const { ethers } = require("hardhat");

async function main() {
    const contractAddress = "0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9"; // Replace with your deployed contract address
    const GUEDHS = await ethers.getContractFactory("GUEDHS");
    const guedhs = GUEDHS.attach(contractAddress);

    // Create a permission (if not already created)
    await guedhs.RequestPermission("uuid1", "userUUID", "custodianUUID");

    // Grant the permission
    const tx = await guedhs.GrantPermission("uuid1");
    await tx.wait();

    // Fetch the permission to verify the status change
    const permission = await guedhs.GetPermission("uuid1");
    console.log("Updated Permission:", permission);
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});