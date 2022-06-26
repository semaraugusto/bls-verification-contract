import pytest
from eth_utils import to_tuple
from py_ecc.fields import FQ, FQ2
from py_ecc.bls.hash import expand_message_xmd
from py_ecc.optimized_bls12_381 import FQ2, normalize
import utils
# import web3

UINT_MAX = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
UINT_64_MAX = 18446744073709551615
UINT_32_MAX = 18446744073709551615

def test_base_field(fplib_contract, w3):
    expected = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    # w3.eth.defaultAccount = w3.eth.accounts[0]
    print(fplib_contract)
    print(fplib_contract.functions)
    print(fplib_contract.functions)
    me = w3.eth.accounts[0]
    actual = fplib_contract.functions.get_base_field().call()
    print(f"actual: {actual}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)


def test_gte_small_eq(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(10), FQ(10)
    expected = 1
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.gte(fp_a_repr, fp_b_repr).call()

    print(f"actual: {actual}")
    print(f"expected: {expected}")
    assert expected == actual

def test_gte_small_gt(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(11), FQ(10)
    expected = 1
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.gte(fp_a_repr, fp_b_repr).call()

    print(f"actual: {actual}")
    print(f"expected: {expected}")
    assert expected == actual

def test_gte_small_lt(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(9), FQ(10)
    expected = 0
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.gte(fp_a_repr, fp_b_repr).call()

    print(f"actual: {actual}")
    print(f"expected: {expected}")
    assert expected == actual

def test_gte_medium_eq(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX + 1), FQ(UINT_MAX + 1)
    expected = 1
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.gte(fp_a_repr, fp_b_repr).call()

    print(f"actual: {actual}")
    print(f"expected: {expected}")
    assert expected == actual

def test_gte_medium_gt(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX + 2), FQ(UINT_MAX + 1)
    expected = 1
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.gte(fp_a_repr, fp_b_repr).call()

    print(f"actual: {actual}")
    print(f"expected: {expected}")
    assert expected == actual

def test_gte_medium_lt(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX + 1), FQ(UINT_MAX + 2)
    expected = 0
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.gte(fp_a_repr, fp_b_repr).call()

    print(f"actual: {actual}")
    print(f"expected: {expected}")
    assert expected == actual

def test_gte_medium_gt_2(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(45442060874369865957053122457065728162598490762543039060009208264153100167950), FQ(UINT_MAX)
    expected = 0
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.gte(fp_a_repr, fp_b_repr).call()

    print(f"actual: {actual}")
    print(f"expected: {expected}")
    assert expected == actual

def test_gte_medium_lt_1(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX * 10), FQ(UINT_MAX*10 + 2)
    expected = 0
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.gte(fp_a_repr, fp_b_repr).call()

    print(f"actual: {actual}")
    print(f"expected: {expected}")
    assert expected == actual

def test_bit_length_big(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a = FQ(FQ.field_modulus-1)
    expected = FQ(384)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    actual = fplib_contract.functions.bitLength(fp_a_repr).call()

    print(f"actual: {actual}")
    print(f"expected: {expected}")

def test_bit_length_medium_2(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a = FQ(UINT_MAX*2)
    expected = FQ(257)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    actual = fplib_contract.functions.bitLength(fp_a_repr).call()

    print(f"actual: {actual}")
    print(f"expected: {expected}")

    assert expected == actual

def test_lmul_small(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(3), FQ(3)
    expected = FQ(9)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmul(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lmul_medium_1(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX), FQ(3)
    expected = FQ(UINT_MAX * 3)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmul(fp_a_repr, fp_b_repr).call()
    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lmul_medium_2(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX), FQ(0xf12387)
    expected = FQ(UINT_MAX * 0xf12387)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmul(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lmul_medium_3(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX), FQ(10)
    expected = FQ(UINT_MAX * 10)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmul(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lmul_medium_4(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX * 10), FQ(1)
    expected = FQ(UINT_MAX*10)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmul(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lmul_medium_5(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(1), FQ(UINT_MAX * 10)
    expected = FQ(UINT_MAX*10)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmul(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lmul_big_1(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX), FQ(0xf12387)
    expected = FQ(UINT_MAX * 0xf12387)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmul(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lmul_big_2(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX+10), FQ(0xf12387)
    expected = FQ((UINT_MAX+10) * 0xf12387)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmul(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lpow_as_mod(fplib_contract):
    FQ.field_modulus = 0xfa0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp = FQ(field_modulus + 1)
    expected = FQ(1)
    fp_repr = utils.convert_int_to_fp_repr(fp)
    actual = fplib_contract.functions.lpow(fp_repr, 1).call()
    actual = utils.convert_fp_to_int(actual)

    print(f"actual: {type(actual)}")
    print(f"actual: {actual}")
    print(f"expected: {expected}")

    assert expected == actual

def test_lpow_small_exp_2(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp = FQ(FQ.field_modulus - 1)
    expected = FQ(fp)
    fp_repr = utils.convert_int_to_fp_repr(fp)
    actual = fplib_contract.functions.lpow(fp_repr, 1).call()
    actual = utils.convert_fp_to_int(actual)

    # print(f"actual: {utils.convert_fp_to_int(actual)}")
    # print(f"actual: {actual}")
    print(f"actual: {type(actual)}")
    print(f"actual: {actual}")
    print(f"expected: {expected}")

    assert expected == actual

def test_lsquare_small_1(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp = FQ(10)
    expected = FQ(100)
    fp_repr = utils.convert_int_to_fp_repr(fp)
    actual = fplib_contract.functions.lsquare(fp_repr).call()

    # print(f"actual: {utils.convert_fp_to_int(actual)}")
    # print(f"actual: {actual}")
    print(f"actual: {type(actual)}")
    print(f"actual: {int.from_bytes(actual, 'big')}")
    print(f"expected: {expected}")

    assert expected == int.from_bytes(actual, 'big')

def test_lsquare_small_2(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp = FQ(2)
    expected = FQ(4)
    fp_repr = utils.convert_int_to_fp_repr(fp)
    actual = fplib_contract.functions.lsquare(fp_repr).call()

    # print(f"actual: {utils.convert_fp_to_int(actual)}")
    # print(f"actual: {actual}")
    print(f"actual: {type(actual)}")
    print(f"actual: {int.from_bytes(actual, 'big')}")
    print(f"expected: {expected}")

    assert expected == int.from_bytes(actual, 'big')

def test_lsquare_small_3(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp = FQ(1)
    expected = FQ(1)
    fp_repr = utils.convert_int_to_fp_repr(fp)
    actual = fplib_contract.functions.lsquare(fp_repr).call()

    # print(f"actual: {utils.convert_fp_to_int(actual)}")
    # print(f"actual: {actual}")
    print(f"actual: {type(actual)}")
    print(f"actual: {int.from_bytes(actual, 'big')}")
    print(f"expected: {expected}")

    assert expected == int.from_bytes(actual, 'big')

def test_lsquare_medium_1(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp = FQ(UINT_32_MAX)
    expected = fp*fp
    fp_repr = utils.convert_int_to_fp_repr(fp)
    actual = fplib_contract.functions.lsquare(fp_repr).call()

    # print(f"actual: {utils.convert_fp_to_int(actual)}")
    # print(f"actual: {actual}")
    print(f"actual: {type(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lsquare_medium_2(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp = FQ(UINT_64_MAX)
    expected = fp*fp
    fp_repr = utils.convert_int_to_fp_repr(fp)
    actual = fplib_contract.functions.lsquare(fp_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    # print(f"actual: {actual}")
    print(f"actual: {type(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lsquare_medium_3(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp = FQ(UINT_MAX)
    expected = fp*fp
    fp_repr = utils.convert_int_to_fp_repr(fp)
    actual = fplib_contract.functions.lsquare(fp_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    # print(f"actual: {actual}")
    print(f"actual: {type(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lsquare_big(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp = FQ(FQ.field_modulus - 1)
    expected = fp*fp
    fp_repr = utils.convert_int_to_fp_repr(fp)
    actual = fplib_contract.functions.lsquare(fp_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    # print(f"actual: {actual}")
    print(f"actual: {type(actual)}")
    print(f"expected: {expected}")
    print(f"expected: {expected}")
    print(f"fq: {FQ.field_modulus}")

    assert expected == utils.convert_fp_to_int(actual)

# @pytest.mark.skip(reason="no way of currently testing this")
def test_lsquare_big_2(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp = FQ(FQ.field_modulus - 10)
    expected = fp*fp
    fp_repr = utils.convert_int_to_fp_repr(fp)
    actual = fplib_contract.functions.lsquare(fp_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    # print(f"actual: {actual}")
    print(f"actual: {type(actual)}")
    print(f"expected: {expected}")
    print(f"expected: {expected}")
    print(f"fq: {FQ.field_modulus}")
    print(f"actual - fq: {utils.convert_fp_to_int(actual) - FQ.field_modulus}")

    assert expected == utils.convert_fp_to_int(actual)

def test_ladd_big_1(fplib_contract):
    FQ.field_modulus = 0xfa0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(field_modulus - 2), FQ(100)
    expected = FQ(98)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.ladd(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"fp_a big1: {utils.convert_fp_to_int(fp_a_repr)}")
    print(f"expected: {expected}")
    assert expected == utils.convert_fp_to_int(actual)

def test_ladd_big_2(fplib_contract):
    FQ.field_modulus = 0xfa0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(100), FQ(field_modulus - 2)
    expected = FQ(98)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.ladd(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")
    print(f"fp_b big2: {utils.convert_fp_to_int(fp_b_repr)}")
    assert expected == utils.convert_fp_to_int(actual)

def test_ladd_big_3(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(100+FQ.field_modulus), FQ(FQ.field_modulus-10)
    expected = FQ(90)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.ladd(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")
    assert expected == utils.convert_fp_to_int(actual)

def test_ladd_big_4(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(2), FQ(FQ.field_modulus-1)
    actual = FQ(fp_a + fp_b)
    expected = FQ(1)
    assert actual == expected
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.ladd(fp_a_repr, fp_b_repr).call()
    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")
    print(f"expected: {utils.convert_fp_to_int(fp_b_repr)}")
    # assert utils.convert_fp_to_int(actual- 1) == FQ.field_modulus - 1
    assert expected == utils.convert_fp_to_int(actual)

def test_ladd_big_5(fplib_contract):
    FQ.field_modulus = 0xfa0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(1), FQ(field_modulus-1)
    expected = FQ(0)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.ladd(fp_a_repr, fp_b_repr).call()
    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")
    print(f"field_modulus: {utils.convert_fp_to_int(fp_b_repr)}")
    # assert utils.convert_fp_to_int(actual) == field_modulus
    assert expected == utils.convert_fp_to_int(actual)

def test_ladd_medium(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX), FQ(UINT_MAX)
    expected = FQ(UINT_MAX * 2)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.ladd(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")
    assert expected == utils.convert_fp_to_int(actual)

def test_ladd_small(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(1), FQ(2)
    expected = FQ(3)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.ladd(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")
    assert expected == utils.convert_fp_to_int(actual)

def test_lsub_small(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(50), FQ(10)
    expected = FQ(40)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lsub(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")
    assert expected == utils.convert_fp_to_int(actual)

def test_lsub_medium_1(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX * 2), FQ(UINT_MAX)
    expected = FQ(UINT_MAX)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lsub(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")
    assert expected == utils.convert_fp_to_int(actual)


def test_lsub_medium_2(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX+1), FQ(UINT_MAX)
    expected = FQ(1)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lsub(fp_a_repr, fp_b_repr).call()
    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")
    assert expected == utils.convert_fp_to_int(actual)

def test_lsub_medium_3(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX*10), FQ(UINT_MAX*10)
    expected = FQ(0)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lsub(fp_a_repr, fp_b_repr).call()
    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")
    assert expected == utils.convert_fp_to_int(actual)

def test_lsub_medium_4(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX*10 + 10), FQ(UINT_MAX*10)
    expected = FQ(10)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lsub(fp_a_repr, fp_b_repr).call()
    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")
    assert expected == utils.convert_fp_to_int(actual)

def test_lsub_medium_5(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX), FQ(45442060874369865957053122457065728162598490762543039060009208264153100167950)
    expected = fp_a-fp_b
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lsub(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")
    assert expected == utils.convert_fp_to_int(actual)

def test_lsub_big(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(FQ.field_modulus-1), FQ(UINT_MAX)
    expected = FQ(FQ.field_modulus - UINT_MAX - 1)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lsub(fp_a_repr, fp_b_repr).call()
    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")
    assert expected == utils.convert_fp_to_int(actual)

def test_lmod_small_7(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a = FQ(33)
    fp_b = FQ(10)
    expected = FQ(3)

    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmod(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lmod_small_1(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(10), FQ(10)
    expected = FQ(0)

    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmod(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lmod_small_2(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(100), FQ(10)
    expected = FQ(0)

    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmod(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)


def test_lmod_small_3(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(8), FQ(10)
    expected = FQ(8)

    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmod(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lmod_small_4(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(18), FQ(10)
    expected = FQ(8)

    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmod(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lmod_small_5(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(18), FQ(9)
    expected = FQ(0)

    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmod(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lmod_small_6(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(19), FQ(9)
    expected = FQ(1)

    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmod(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lmod_medium_1(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX + 10), FQ(UINT_MAX + 10)
    expected = FQ(0)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmod(fp_a_repr, fp_b_repr).call()
    actual = utils.convert_fp_to_int(actual)
    # assert actual < utils.convert_fp_to_int(fp_b), "wtf"
    print(f"actual: {actual}")
    print(f"expected: {expected}")
    print(f"fp_a: {fp_a}")
    print(f"fp_b: {fp_b}")
    print(f"uintmax: {UINT_MAX}")
    assert expected == actual

def test_lmod_medium_2(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX * 10 + 10), FQ(UINT_MAX)
    expected = FQ(10)

    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmod(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lmod_medium_3(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(115792089237316195423570985008687907853269984665640564039457584007913129639945), FQ(UINT_MAX)
    expected = FQ(10)

    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmod(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lmod_big_1(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(FQ.field_modulus-2), FQ(FQ.field_modulus-1)
    expected = fp_a

    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmod(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lmod_big_2(fplib_contract):
    FQ.field_modulus = 0xfa0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(field_modulus+2), FQ(field_modulus)
    expected = FQ(2)

    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmod(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_lmod_base_field(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ((FQ.field_modulus-1)*5 + 100), FQ(FQ.field_modulus-1)
    expected = FQ(95)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmod(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")
    assert expected == utils.convert_fp_to_int(actual)

def test_lmod_really_big(fplib_contract):
    FQ.field_modulus = 0xffa0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    contract_field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ((contract_field_modulus*100+1)), FQ(contract_field_modulus)
    expected = FQ(1)
    fp_a_repr = utils.convert_big_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_big_to_fp_repr(fp_b)
    actual = fplib_contract.functions.lmod(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")
    assert expected == utils.convert_fp_to_int(actual)

def test_bit_length_medium_1(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a = FQ(UINT_MAX)
    expected = FQ(256)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    actual = fplib_contract.functions.bitLength(fp_a_repr).call()

    print(f"actual: {actual}")
    print(f"expected: {expected}")

    assert expected == actual

def test_bit_length_small_2(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a = FQ(10)
    expected = FQ(4)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    actual = fplib_contract.functions.bitLength(fp_a_repr).call()

    print(f"actual: {actual}")
    print(f"expected: {expected}")

    assert expected == actual

def test_bit_length_small_1(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a = FQ(1)
    expected = FQ(1)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    actual = fplib_contract.functions.bitLength(fp_a_repr).call()

    print(f"actual: {actual}")
    print(f"expected: {expected}")

    assert expected == actual

def test_ldiv_small(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(10), 2
    expected = FQ(5)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.ldiv(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_ldiv_medium_1(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX * 10 + 10), FQ(UINT_MAX * 10)
    expected = FQ(1)

    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.ldiv(fp_a_repr, fp_b_repr).call()

    print(f"field_module_medium_2: actual: {utils.convert_fp_to_int(actual)}")
    print(f"field_module_medium_2: expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_ldiv_medium_2(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX * 10), FQ(UINT_MAX * 10)
    expected = FQ(1)

    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.ldiv(fp_a_repr, fp_b_repr).call()

    print(f"field_module_medium_2: actual: {utils.convert_fp_to_int(actual)}")
    print(f"field_module_medium_2: expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_ldiv_big(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ(UINT_MAX * 1_000_000_000), 1_000_000_000
    expected = FQ(UINT_MAX)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp_repr(fp_b)
    actual = fplib_contract.functions.ldiv(fp_a_repr, fp_b_repr).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_shl_small(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, n = FQ(1), 10
    expected = FQ(1 << n)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    actual = fplib_contract.functions.shl(fp_a_repr, n).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

def test_shl_medium(fplib_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, n = FQ(UINT_MAX), 10
    expected = FQ(UINT_MAX << n)
    fp_a_repr = utils.convert_int_to_fp_repr(fp_a)
    actual = fplib_contract.functions.shl(fp_a_repr, n).call()

    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == utils.convert_fp_to_int(actual)

