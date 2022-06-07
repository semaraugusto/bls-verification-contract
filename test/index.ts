import { expect } from "chai";
import { ethers } from "hardhat";
 
// import {getImplementation} from "@chainsafe/bls/getImplementation";

// const bls =  require("@chainsafe/bls/blst-native");
// import bls from "@chainsafe/bls-keygen";
import { generateRandomSecretKey, } from "@chainsafe/bls-keygen";
const bls = require('noble-bls12-381');

import { PointG2, PointG1, Fp, Fp2 } from 'noble-bls12-381';

describe("BlsVerify", function () {
  it("Should verify aggregated signature", async function () {
    // const bls = await getImplementation("herumi");

    const Verifier = await ethers.getContractFactory("BlsVerifier");
    const verifier = await Verifier.deploy();
    await verifier.deployed();

    const message = Buffer.from("message!");

    const sk = generateRandomSecretKey();
    console.log(ethers.BigNumber.from(sk).toHexString())
    console.log(sk.length)
    const pk: PointG1 = bls.getPublicKey(sk);
    console.log(pk)
    // console.log(ethers.BigNumber.from(pk).toHexString())
    const signed: PointG2 = await bls.sign(message, sk)
    // const signed = await bls.sign(message, sk)

    console.log(signed);
    
    const verify = await bls.verify(signed, message, pk)
    console.log(verify)
    // // TODO!: Get public key converted to G1
    // // TODO!: Get signature converted to G2
    // const pk_g1 = "todo";
    // const sig_g2 = "todo";
    // await verifier.blsSignatureIsValid(message, pk, signed.toString(), Fp(pk_point.y.value, signed_point.y.value);
    });
})
