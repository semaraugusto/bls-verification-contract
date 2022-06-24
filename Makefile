# NOTE: following the `Makefile` from the `eth2-deposit-contract` submodule for generation of the contract JSON.

VERIFIER_JSON=deposit_verifier.json
MATH_JSON=math.json
FPLIB_TEST_JSON=fplib_test.json

clean:
	@rm -rf build
	@rm -f $JSON_TARGET

# Note: using /bin/echo for macOS support
compile: clean
	@solc --metadata-literal --optimize --optimize-runs 5000000 --bin --abi --combined-json=abi,bin,bin-runtime,srcmap,srcmap-runtime,ast,metadata,storage-layout --overwrite -o build contracts/deposit_verifier.sol contracts/libs/types.sol contracts/libs/math.sol contracts/libs/FpLib.sol contracts/tests/FpLibTest.sol
	@/bin/echo -n '{"abi": ' > $(VERIFIER_JSON)
	@cat build/DepositVerifier.abi >> $(VERIFIER_JSON)
	@/bin/echo -n ', "bytecode": "0x' >> $(VERIFIER_JSON)
	@cat build/DepositVerifier.bin >> $(VERIFIER_JSON)
	@/bin/echo -n '"}' >> $(VERIFIER_JSON)
	@/bin/echo -n '{"abi": ' > $(MATH_JSON)
	@cat build/Math.abi >> $(MATH_JSON)
	@/bin/echo -n ', "bytecode": "0x' >> $(MATH_JSON)
	@cat build/Math.bin >> $(MATH_JSON)
	@/bin/echo -n '"}' >> $(MATH_JSON)
	@/bin/echo -n '{"abi": ' > $(FPLIB_TEST_JSON)
	@cat build/FpLibTest.abi >> $(FPLIB_TEST_JSON)
	@/bin/echo -n ', "bytecode": "0x' >> $(FPLIB_TEST_JSON)
	@cat build/FpLibTest.bin >> $(FPLIB_TEST_JSON)
	@/bin/echo -n '"}' >> $(FPLIB_TEST_JSON)
