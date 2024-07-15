require('dotenv').config({ path: '../blockchain-api/.env' });
const fs = require('fs');
const path = require('path');

async function main() {
    const [deployer] = await ethers.getSigners();

    const GUEDHS = await ethers.getContractFactory("GUEDHS");

    const guedhs = await GUEDHS.deploy(deployer.getAddress());
    
    await guedhs.deployed();

    const logPath = path.resolve(__dirname, '../deploy.log');
    fs.writeFileSync(logPath, `GUEDHS deployed to: ${guedhs.address}\n`);

    console.log("GUEDHS contract deployed to:", guedhs.address);
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });