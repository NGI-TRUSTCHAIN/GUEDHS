const { loadFixture } = require('@nomicfoundation/hardhat-network-helpers');
const { expect } = require('chai');

describe('GUEDHS', function () {
  // We define a fixture to reuse the same setup in every test.
  // We use loadFixture to run this setup once, snapshot that state,
  // and reset Hardhat Network to that snapshot in every test.
  async function deployContractAndSetVariables() {
    const [deployer] = await ethers.getSigners();
    const GUEDHS = await ethers.getContractFactory("GUEDHS");
    const guedhs = await GUEDHS.deploy(deployer.getAddress());

    console.log('Signer 1 address: ', deployer.address);
    return { guedhs, deployer };
  }

  it('should deploy and set the owner correctly', async function () {
    const { guedhs, deployer } = await loadFixture(deployContractAndSetVariables);

    expect(await guedhs.owner()).to.equal(deployer.address);
  });
});