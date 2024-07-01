require('dotenv').config({ path: '../blockchain-api/.env' });

async function main() {
    // Compile the contract if not already compiled
    //await hre.run('compile');
    const [deployer] = await ethers.getSigners();

    const GUEDHS = await ethers.getContractFactory("GUEDHS");

    const guedhs = await GUEDHS.deploy(deployer.getAddress());
    
    await guedhs.deployed();

    console.log("GUEDHS deployed to:", guedhs.address);
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });