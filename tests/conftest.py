import hashlib
import json
import os
import sys

import eth_tester
import pytest
from eth2spec.phase0.spec import (
    DOMAIN_DEPOSIT,
    DepositMessage,
    DepositData,
    compute_domain,
    compute_signing_root,
)
from eth2spec.utils.ssz.ssz_impl import hash_tree_root
from eth.vm.forks.berlin import BerlinVM
from eth_tester import EthereumTester, PyEVMBackend
from py_ecc.bls.ciphersuites import G2ProofOfPossession
from py_ecc.bls.g2_primatives import pubkey_to_G1, signature_to_G2
from py_ecc.optimized_bls12_381.optimized_curve import normalize
from web3 import Web3
from web3.providers.eth_tester import EthereumTesterProvider
import utils

DIR = os.path.dirname(__file__)


def _get_json(filename):
    with open(filename) as f:
        return json.load(f)

def _get_address(filename):
    with open(filename) as f:
        return f.read()

def get_math_lib_json():
    filename = os.path.join(DIR, "../math.json")
    return _get_json(filename)

def get_proxy_contract_json():
    filename = os.path.join(DIR, "../build/contracts/Verifier.json")
    return _get_json(filename)

def get_proxy_contract_address():
    filename = os.path.join(DIR, "../verifier_addr.txt")
    return _get_address(filename)

def get_fplib_test_json():
    filename = os.path.join(DIR, "../build/contracts/FpLibTest.json")
    return _get_json(filename)

def get_fplib_test_address():
    filename = os.path.join(DIR, "../fplib_test_addr.txt")
    return _get_address(filename)


@pytest.fixture
def berlin_vm_configuration():
    return ((0, BerlinVM),)


@pytest.fixture
def tester(berlin_vm_configuration):
    return EthereumTester(PyEVMBackend(vm_configuration=berlin_vm_configuration))


@pytest.fixture
def field_elements(proxy_contract, signing_root):
    field_elements_parts = proxy_contract.functions.hashToField(signing_root).call()
    field_elements = tuple(
        utils.convert_fp2_to_int(fp2_repr) for fp2_repr in field_elements_parts
    )
    return field_elements

@pytest.fixture
# def w3(tester):
def w3():
    # web3 = Web3(EthereumTesterProvider(tester))
    web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:9545"))
    # web3.eth.defaultAccount = web3.eth.accounts[0]
    return web3

def _deploy_contract(contract_json, contract_address, w3, *args):
    contract_bytecode = contract_json["bytecode"]
    contract_abi = contract_json["abi"]
    registration = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    me = w3.eth.accounts[0]
    tx_hash = registration.constructor(*args).transact({"from": me})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_deployed = w3.eth.contract(
        address=contract_address, abi=contract_abi
    )
    return contract_deployed

# @pytest.fixture
# def math_contract(w3):
#     return _deploy_contract(get_math_lib_json(), w3)

@pytest.fixture
def deposit_domain():
    domain = compute_domain(DOMAIN_DEPOSIT)
    with open("domain.txt", "wb") as f:
        f.write(domain)
    return domain


@pytest.fixture
def proxy_contract_deployer():
    def _deployer(w3, deposit_domain):
        return _deploy_contract(get_proxy_contract_json(), get_proxy_contract_address(), w3, deposit_domain)

    return _deployer

@pytest.fixture
def fplib_test_deployer():
    def _deployer(w3):
        return _deploy_contract(get_fplib_test_json(), get_fplib_test_address(), w3)

    return _deployer

@pytest.fixture
def proxy_contract(w3, deposit_domain, proxy_contract_deployer):
    return proxy_contract_deployer(w3, deposit_domain)

@pytest.fixture
def fplib_contract(w3, fplib_test_deployer):
    return fplib_test_deployer(w3)

@pytest.fixture
def assert_tx_failed(tester):
    def assert_tx_failed(
        function_to_test, exception=eth_tester.exceptions.TransactionFailed
    ):
        snapshot_id = tester.take_snapshot()
        with pytest.raises(exception):
            function_to_test()
        tester.revert_to_snapshot(snapshot_id)

    return assert_tx_failed


@pytest.fixture
def seed():
    return "some-secret".encode()


@pytest.fixture
def bls_private_key(seed):
    return G2ProofOfPossession.KeyGen(seed)


@pytest.fixture
def bls_public_key(bls_private_key):
    return G2ProofOfPossession.SkToPk(bls_private_key)


@pytest.fixture
def withdrawal_credentials():
    return b"\x00" + hashlib.sha256("some-secret".encode()).digest()[1:]


@pytest.fixture
def deposit_amount():
    # NOTE: 32 ETH in Gwei
    return 32 * 10 ** 9


@pytest.fixture
def deposit_message(bls_public_key, withdrawal_credentials, deposit_amount):
    return DepositMessage(
        pubkey=bls_public_key,
        withdrawal_credentials=withdrawal_credentials,
        amount=deposit_amount,
    )


@pytest.fixture
def signing_root(deposit_message, deposit_domain):
    return compute_signing_root(deposit_message, deposit_domain)
    # return result


@pytest.fixture
def deposit_data_root(deposit_message, signature):
    deposit_data = DepositData(
        pubkey=deposit_message.pubkey,
        withdrawal_credentials=deposit_message.withdrawal_credentials,
        amount=deposit_message.amount,
        signature=signature,
    )
    root = hash_tree_root(deposit_data)
    return root


@pytest.fixture
def signature(bls_private_key, signing_root):
    return G2ProofOfPossession.Sign(bls_private_key, signing_root)


@pytest.fixture
def public_key_witness(bls_public_key):
    group_element = pubkey_to_G1(bls_public_key)
    normalized_group_element = normalize(group_element)
    return normalized_group_element[1]


@pytest.fixture
def signature_witness(signature):
    group_element = signature_to_G2(signature)
    normalized_group_element = normalize(group_element)
    return normalized_group_element[1]


@pytest.fixture
def dst():
    return G2ProofOfPossession.DST
