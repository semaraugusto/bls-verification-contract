const fs = require("fs");
const FpLib = artifacts.require("FpLib");
const FpLibTest = artifacts.require("FpLibTest");
const Verifier = artifacts.require("Verifier");

module.exports = function (deployer) {
    deployer.deploy(FpLib);
    deployer.link(FpLib, Verifier);
    deployer.link(FpLib, FpLibTest);
    deposit_domain = fs.readFileSync("domain.txt");
    deployer.deploy(Verifier, deposit_domain);
    deployer.deploy(FpLibTest);
    FpLib.deployed().then((instance) => {
        console.log("fplib, ", instance.address.toString());
        string = instance.address;
        fs.writeFile("fplib_addr.txt", string, (err) => {
            if (err) {
                console.error(err);
            }
            // file written successfully
        });
        // fs.writeFile("fplib_addr.txt", instance.address);
    });
    Verifier.deployed().then((instance) => {
        console.log("Verifier, ", instance.address);
        // string = ("addr: ", instance.address);
        fs.writeFile("verifier_addr.txt", instance.address, (err) => {
            if (err) {
                console.error(err);
            }
            // file written successfully
        });
    });
    FpLibTest.deployed().then((instance) => {
        console.log("FpLibTest, ", instance.address);
        // string = ("addr: ", instance.address);
        fs.writeFile("fplib_test_addr.txt", instance.address, (err) => {
            if (err) {
                console.error(err);
            }
            // file written successfully
        });
    });
    // console.log(
};
