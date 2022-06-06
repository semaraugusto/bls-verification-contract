import { expect } from "chai";
import { ethers } from "hardhat";

describe("BlsVerify", function () {
  it("Should verify aggregated signature", async function () {
    const Verifier = await ethers.getContractFactory("BlsVerifier");
    const verifier = await Verifier.deploy();
    await verifier.deployed();

    const pk1 = ethers.BigNumber.from("f1f3d1733381e9182d7ca1e965cce5c27b3ae8f271ee951b78bab8759add18937b946c4831744f505ff696038468491599e67f1b80e8980d78eefe5178742d870e68b8647ad5d0f6cb02edcb2d226a47149e267195d7296447c03163278a3814a6e98f5d705ac068b8af6bd3f77c9cd2d32b5bf1f084d5049380db168f5fdcd18d88eb0a0c339a13f7e563a1037ef201761aa449800e3d50166c908deb6f68b457c96a408a25aa363439119b24c74ecf4717dcdd18fbe051cb842330595d69073f403487445cbb54c847e5e2bbfac4d02787a9c615a21fd656c15b527a540e0f19109eb8a81c7e90c5bdac80d5d3b0049ada9235dbff2fe2888f458d0c38aeeed5e2c2df5013d75d00e7714bbbb3a572b38ba85d124180fb96ca3e94cd72eb00");
  });
    const signed = ethers.BigNumber.from("84476d960787870670baf6d4e7902910e10fd51e6d79a6c73a4c7ed385f347f44d51d89d07d8165c8e09cf892f936811e5f60e258893d084334db0a4e8bdff7b194df96913f90c4a849522b77451026bdfbe67a0dcd7b029a21981b06bcb8310f539cc1f0552fc55c2f3a084af82837dc1f1ff25617b61994bba9c14dea20b62ad6e02fccca38cd1922b9d77016fde17");

    const message = Buffer.from("message!");

    // TODO!: Get public key converted to G1
    // TODO!: Get signature converted to G2
    const pk_g1 = "todo";
    const sig_g2 = "todo";

    verifier.verify(pk1.toString(), signed.toString(), message, pk_g1, sig_g2)
});
