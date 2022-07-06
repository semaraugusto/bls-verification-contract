import hashlib
import sys
from typing import (
    Optional,
    Tuple,
    TypeVar,
    Union,
)
from py_ecc.typing import (
    Optimized_Field,
    Optimized_Point3D,
)

import pytest
from eth_utils import to_tuple, keccak
# from py_ecc.fields import FQ, FQ2
from py_ecc.fields import (
    bls12_381_FQ as FQ,
    bls12_381_FQ2 as FQ2,
)
from py_ecc.typing import (
    Field,
    GeneralPoint,
    Point2D,
    # FQ2,
)
from py_ecc.bls.g2_primatives import pubkey_to_G1, signature_to_G2
from py_ecc.bls.hash import expand_message_xmd
from py_ecc.bls.hash_to_curve import (
    clear_cofactor_G2,
    hash_to_field_FQ2,
    hash_to_G2,
)
from pyecc_utils import map_to_curve_G2, optimized_swu_G2_partial, sqrt_division_FQ2, sqrt_division_FQ2_partial, exponentiateBy, get_roots_of_unity
# from py_ecc.bls12_381 import add
from py_ecc.bls import G2ProofOfPossession
from py_ecc.optimized_bls12_381 import FQ2, normalize, add
# from utils import utils.convert_int_to_fp_repr, convert_int_to_fp2_repr, convert_big_to_int, convert_fp_to_int, convert_fp2_to_int, convert_big_to_fp_repr
import utils
import py_ecc

EMPTY_DEPOSIT_ROOT = "d70a234731285c6804c2a4f56711ddb8c82c99740f207854891028af34e27e5e"
UINT_MAX = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
UINT_64_MAX = 18446744073709551615
UINT_32_MAX = 18446744073709551615

# Field = TypeVar(
#     'Field',
#     # General
#     FQ,
#     FQ2,
#     py_ecc.fields.bls12_381_FQ2
# )

def test_compute_signing_root_matches_spec(
    proxy_contract, bls_public_key, withdrawal_credentials, deposit_amount, signing_root, deposit_domain
):
    amount_in_wei = deposit_amount * 10 ** 9
    computed_signing_root = proxy_contract.functions.computeSigningRoot(
        bls_public_key, withdrawal_credentials, amount_in_wei
    ).call()
    print(signing_root, file=sys.stderr)
    print(computed_signing_root)
    assert computed_signing_root == signing_root


def test_expand_message_matches_spec(proxy_contract, signing_root, dst):
    result = proxy_contract.functions.expandMessage(signing_root).call()

    spec_result = expand_message_xmd(signing_root, dst, 256, hashlib.sha256)

    assert result == spec_result

def test_hash_to_field_matches_spec(proxy_contract, signing_root, dst):
    result = proxy_contract.functions.hashToField(signing_root).call()
    converted_result = tuple(utils.convert_fp2_to_int(fp2_repr) for fp2_repr in result)

    spec_result = hash_to_field_FQ2(signing_root, 2, dst, hashlib.sha256)

    assert converted_result == spec_result

def test_ladd_fq2(proxy_contract):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    fp_a, fp_b = FQ2([FQ(1), FQ(1)]), FQ2([FQ(2), FQ(2)])
    expected = (FQ(3), FQ(3))
    fp_a_repr = utils.convert_int_to_fp2_repr(fp_a)
    fp_b_repr = utils.convert_int_to_fp2_repr(fp_b)
    actual = proxy_contract.functions.ladd(fp_a_repr, fp_b_repr).call({'gas': 1000000000})
    actual = tuple(utils.convert_fp_to_int(fp2_repr) for fp2_repr in actual)
    print(f"actual: {utils.convert_fp_to_int(actual)}")
    print(f"expected: {expected}")

    assert expected == actual

@pytest.mark.skip(reason="no way of currently testing this")
def test_lsub_0(proxy_contract, fplib_contract, signing_root):
    points = proxy_contract.functions.signature_to_g2_points(signing_root).call()
    first_g2 = points[0]
    second_g2 = points[1]
    first_g2_pyecc =[]
    for tup in first_g2:
        p = []
        for f in tup:
            p.append(FQ(utils.convert_fp_to_int(f)))

        p = FQ2(p)
        first_g2_pyecc.append(p);
    
    first_g2_pyecc.append(FQ2.one());
    first_g2_pyecc = tuple(first_g2_pyecc)

    second_g2_pyecc =[]
    for tup in second_g2:
        p = []
        for f in tup:
            p.append(FQ(utils.convert_fp_to_int(f)))

        p = FQ2(p)
        second_g2_pyecc.append(p);
    
    second_g2_pyecc.append(FQ2.one());
    second_g2_pyecc = tuple(second_g2_pyecc)
    result, u1, u2 = addTest(first_g2_pyecc,second_g2_pyecc)
    expected = u1 - u2

    u1a, _ = u1.coeffs
    u2a, _ = u2.coeffs
    u1a = utils.convert_int_to_fp_repr(u1a)
    u2a = utils.convert_int_to_fp_repr(u2a)
    actual = fplib_contract.functions.lsub(u1a, u2a).call()
    actual = utils.convert_fp_to_int(actual)
    print(f"{actual=}")
    print(f"{expected=}")
    assert expected.coeffs[0] == actual

@pytest.mark.skip(reason="no way of currently testing this")
def test_lsub_1(proxy_contract, fplib_contract, signing_root):
    FQ.field_modulus = 0xfa0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    FIELD_MODULUS = FQ(0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab)
    points = proxy_contract.functions.signature_to_g2_points(signing_root).call()
    first_g2 = points[0]
    second_g2 = points[1]
    first_g2_pyecc =[]
    for tup in first_g2:
        p = []
        for f in tup:
            p.append(FQ(utils.convert_fp_to_int(f)))

        p = FQ2(p)
        first_g2_pyecc.append(p);
    
    first_g2_pyecc.append(FQ2.one());
    first_g2_pyecc = tuple(first_g2_pyecc)

    second_g2_pyecc =[]
    for tup in second_g2:
        p = []
        for f in tup:
            p.append(FQ(utils.convert_fp_to_int(f)))

        p = FQ2(p)
        second_g2_pyecc.append(p);
    
    second_g2_pyecc.append(FQ2.one());
    second_g2_pyecc = tuple(second_g2_pyecc)
    result, u1, u2 = addTest(first_g2_pyecc,second_g2_pyecc)
    expected = u1 - u2

    _, x = u1.coeffs
    _, y = u2.coeffs
    x_repr = utils.convert_int_to_fp_repr(x)
    y_repr = utils.convert_int_to_fp_repr(y)
    actual_repr = fplib_contract.functions.lsub(x_repr, y_repr).call()
    print(f"{x_repr = }")
    print(f"{y_repr = }")
    print(f"{actual_repr = }")
    print(f"expected_repr{utils.convert_int_to_fp_repr(expected.coeffs[1]) = }")
    actual = utils.convert_big_to_int(actual_repr)
    print(f"{FIELD_MODULUS=}")
    print(f"{x = }")
    print(f"{y = }")
    print(f"  {actual = }")
    print(f"expected = {expected.coeffs[1]}")
    assert expected.coeffs[1] == actual

@pytest.mark.skip(reason="no way of currently testing this")
def test_lsub(proxy_contract, fplib_contract, signing_root):
    points = proxy_contract.functions.signature_to_g2_points(signing_root).call()
    first_g2 = points[0]
    second_g2 = points[1]
    first_g2_pyecc =[]
    for tup in first_g2:
        p = []
        for f in tup:
            p.append(FQ(utils.convert_fp_to_int(f)))

        p = FQ2(p)
        first_g2_pyecc.append(p);
    
    first_g2_pyecc.append(FQ2.one());
    first_g2_pyecc = tuple(first_g2_pyecc)

    second_g2_pyecc =[]
    for tup in second_g2:
        p = []
        for f in tup:
            p.append(FQ(utils.convert_fp_to_int(f)))

        p = FQ2(p)
        second_g2_pyecc.append(p);
    
    second_g2_pyecc.append(FQ2.one());
    second_g2_pyecc = tuple(second_g2_pyecc)
    result, u1, u2 = addTest(first_g2_pyecc,second_g2_pyecc)
    expected = u1 - u2

    u1a, u1b = u1.coeffs
    u2a, u2b = u2.coeffs
    u1a = utils.convert_int_to_fp_repr(u1a)
    u1b = utils.convert_int_to_fp_repr(u1b)
    u2a = utils.convert_int_to_fp_repr(u2a)
    u2b = utils.convert_int_to_fp_repr(u2b)
    u1 = (u1a, u1b)
    u2 = (u2a, u2b)
    actual = proxy_contract.functions.lsub(u1, u2).call()
    actual = FQ2([utils.convert_fp_to_int(a) for a in actual])
    print(f"{actual=}")
    print(f"{expected=}")
    assert expected == actual

@pytest.mark.skip(reason="no way of currently testing this due to bad test coding")
def test_individial_multiplications(proxy_contract, fplib_contract, signing_root):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    FIELD_MODULUS = FQ(0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab)
    points = proxy_contract.functions.signature_to_g2_points(signing_root).call()
    first_g2 = points[0]
    second_g2 = points[1]
    first_g2_pyecc =[]
    for tup in first_g2:
        p = []
        for f in tup:
            p.append(FQ(utils.convert_fp_to_int(f)))

        p = FQ2(p)
        first_g2_pyecc.append(p);
    
    first_g2_pyecc.append(FQ2.one());
    first_g2_pyecc = tuple(first_g2_pyecc)

    second_g2_pyecc =[]
    for tup in second_g2:
        p = []
        for f in tup:
            p.append(FQ(utils.convert_fp_to_int(f)))

        p = FQ2(p)
        second_g2_pyecc.append(p);
    

    second_g2_pyecc.append(FQ2.one());
    second_g2_pyecc = tuple(second_g2_pyecc)
    result, v, v_sqr = addTest(first_g2_pyecc,second_g2_pyecc)
    print(f"       {v.coeffs = }")
    v1, _ = v.coeffs

    v1_repr = utils.convert_int_to_fp_repr(v1)
    actual_repr = fplib_contract.functions.get_partial_muls(v1_repr, v1_repr).call()
    # _, a, b = actual_repr
    # actual = utils.convert_huge_fp_to_int(actual_repr)
    r1, r0 = v1_repr
    result_1 = r0*r0
    result_2 = r1*r0
    result_3 = r0*r1
    result_4 = r1*r1
    # expected_repr = utils.convert_huge_int_to_fp_repr(expected)
    for i, r  in enumerate(actual_repr):
        print(f"actual: {i}: {r}")
    
    actual_1 = utils.convert_big_to_int((actual_repr[0], actual_repr[1]))
    actual_2 = utils.convert_big_to_int((actual_repr[2], actual_repr[3]))
    actual_3 = utils.convert_big_to_int((actual_repr[4], actual_repr[5]))
    actual_4 = utils.convert_big_to_int((actual_repr[6], actual_repr[7]))

    print(f"result 1: {result_1}")
    print(f"result 2: {result_2}")
    print(f"result 3: {result_3}")
    print(f"result 4: {result_4}")

    assert result_1 == actual_1
    assert result_2 == actual_2
    assert result_3 == actual_3
    assert result_4 == actual_4
    # assert expected.coeffs[1] == actual

@pytest.mark.skip(reason="no way of currently testing this due to bad test coding")
def test_lmul_unchecked_0(proxy_contract, fplib_contract, signing_root):
    FQ.field_modulus = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    FIELD_MODULUS = FQ(0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab)
    points = proxy_contract.functions.signature_to_g2_points(signing_root).call()
    first_g2 = points[0]
    second_g2 = points[1]
    first_g2_pyecc =[]
    for tup in first_g2:
        p = []
        for f in tup:
            p.append(FQ(utils.convert_fp_to_int(f)))

        p = FQ2(p)
        first_g2_pyecc.append(p);
    
    first_g2_pyecc.append(FQ2.one());
    first_g2_pyecc = tuple(first_g2_pyecc)

    second_g2_pyecc =[]
    for tup in second_g2:
        p = []
        for f in tup:
            p.append(FQ(utils.convert_fp_to_int(f)))

        p = FQ2(p)
        second_g2_pyecc.append(p);
    

    second_g2_pyecc.append(FQ2.one());
    second_g2_pyecc = tuple(second_g2_pyecc)
    result, v, v_sqr = addTest(first_g2_pyecc,second_g2_pyecc)
    print(f"       {v.coeffs = }")
    v1, _ = v.coeffs

    v1_repr = utils.convert_int_to_fp_repr(v1)
    actual_repr = fplib_contract.functions.lmulUnchecked(v1_repr, v1_repr).call()
    # _, a, b = actual_repr
    actual = FQ(utils.convert_huge_fp_to_int(actual_repr))
    expected = v1*v1
    print(f"actual: {actual_repr}")
    # print(f"actual: {actual}")
    # print(f"expected: {expected}")
    print(f"expected_repr: {utils.convert_huge_int_to_fp_repr(expected)}")
    # # print(f"actual: {utils.convert_huge_fp_to_int(actual_repr)}")

    assert utils.convert_huge_int_to_fp_repr(expected) == tuple(actual_repr)
    # assert expected.coeffs[1] == actual

@pytest.mark.skip(reason="no way of currently testing this due to bad test coding")
def test_lmul_unchecked_1(proxy_contract, fplib_contract, signing_root):
    FQ.field_modulus = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    FIELD_MODULUS = FQ(0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab)
    points = proxy_contract.functions.signature_to_g2_points(signing_root).call()
    first_g2 = points[0]
    second_g2 = points[1]
    first_g2_pyecc =[]
    for tup in first_g2:
        p = []
        for f in tup:
            p.append(FQ(utils.convert_fp_to_int(f)))

        p = FQ2(p)
        first_g2_pyecc.append(p);
    
    first_g2_pyecc.append(FQ2.one());
    first_g2_pyecc = tuple(first_g2_pyecc)

    second_g2_pyecc =[]
    for tup in second_g2:
        p = []
        for f in tup:
            p.append(FQ(utils.convert_fp_to_int(f)))

        p = FQ2(p)
        second_g2_pyecc.append(p);
    

    second_g2_pyecc.append(FQ2.one());
    second_g2_pyecc = tuple(second_g2_pyecc)
    result, v, v_sqr = addTest(first_g2_pyecc,second_g2_pyecc)
    print(f"       {v.coeffs = }")
    _, v0 = v.coeffs

    v0_repr = utils.convert_int_to_fp_repr(v0)
    actual_repr = fplib_contract.functions.lmulUnchecked(v0_repr, v0_repr).call()
    # _, a, b = actual_repr
    actual = FQ(utils.convert_huge_fp_to_int(actual_repr))
    expected = v0*v0
    print(f"actual: {actual_repr}")
    # print(f"actual: {actual}")
    # print(f"expected: {expected}")
    print(f"expected_repr: {utils.convert_huge_int_to_fp_repr(expected)}")
    # # print(f"actual: {utils.convert_huge_fp_to_int(actual_repr)}")

    assert utils.convert_huge_int_to_fp_repr(expected) == tuple(actual_repr)

@pytest.mark.skip(reason="no way of currently testing this due to bad test coding")
def test_lmul_fplib_0(proxy_contract, fplib_contract, signing_root):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    FIELD_MODULUS = FQ(0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab)
    points = proxy_contract.functions.signature_to_g2_points(signing_root).call()
    first_g2 = points[0]
    second_g2 = points[1]
    first_g2_pyecc =[]
    for tup in first_g2:
        p = []
        for f in tup:
            p.append(FQ(utils.convert_fp_to_int(f)))

        p = FQ2(p)
        first_g2_pyecc.append(p);
    
    first_g2_pyecc.append(FQ2.one());
    first_g2_pyecc = tuple(first_g2_pyecc)

    second_g2_pyecc =[]
    for tup in second_g2:
        p = []
        for f in tup:
            p.append(FQ(utils.convert_fp_to_int(f)))

        p = FQ2(p)
        second_g2_pyecc.append(p);
    

    second_g2_pyecc.append(FQ2.one());
    second_g2_pyecc = tuple(second_g2_pyecc)
    result, v, v_sqr = addTest(first_g2_pyecc,second_g2_pyecc)
    print(f"       {v.coeffs = }")
    v_repr = utils.convert_int_to_fp2_repr(v)
    # v1, _ = v_repr
    v1, _ = v.coeffs
    v1_repr = utils.convert_int_to_fp_repr(v1)
    actual_repr = fplib_contract.functions.lmul(v1_repr, v1_repr).call()
    # _, a, b = actual_repr
    expected = FQ(v1*v1)
    print(f"actual: {actual_repr}")
    actual = FQ(utils.convert_fp_to_int(actual_repr))
    print(f"actual: {actual}")
    print(f"expected: {expected}")

    assert expected == actual

@pytest.mark.skip(reason="no way of currently testing this due to bad test coding")
def test_lmul_fplib_1(proxy_contract, fplib_contract, signing_root):
    FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    FIELD_MODULUS = FQ(0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab)
    points = proxy_contract.functions.signature_to_g2_points(signing_root).call()
    first_g2 = points[0]
    second_g2 = points[1]
    first_g2_pyecc =[]
    for tup in first_g2:
        p = []
        for f in tup:
            p.append(FQ(utils.convert_fp_to_int(f)))

        p = FQ2(p)
        first_g2_pyecc.append(p);
    
    first_g2_pyecc.append(FQ2.one());
    first_g2_pyecc = tuple(first_g2_pyecc)

    second_g2_pyecc =[]
    for tup in second_g2:
        p = []
        for f in tup:
            p.append(FQ(utils.convert_fp_to_int(f)))

        p = FQ2(p)
        second_g2_pyecc.append(p);
    

    second_g2_pyecc.append(FQ2.one());
    second_g2_pyecc = tuple(second_g2_pyecc)
    result, v, v_sqr = addTest(first_g2_pyecc,second_g2_pyecc)
    print(f"       {v.coeffs = }")
    v_repr = utils.convert_int_to_fp2_repr(v)
    # v1, _ = v_repr
    _, v0 = v.coeffs
    v0_repr = utils.convert_int_to_fp_repr(v0)
    actual_repr = fplib_contract.functions.lmul(v0_repr, v0_repr).call()
    # _, a, b = actual_repr
    expected = FQ(v0*v0)
    print(f"actual: {actual_repr}")
    actual = FQ(utils.convert_fp_to_int(actual_repr))
    print(f"actual: {actual}")
    # print(f"actual: {actual}")
    print(f"expected: {expected}")
    # print(f"expected_repr: {utils.convert_huge_int_to_fp_repr(expected)}")
    # # print(f"actual: {utils.convert_huge_fp_to_int(actual_repr)}")

    assert expected == actual

# # @pytest.mark.skip(reason="no way of currently testing this")
# def test_lmul_0(proxy_contract, fplib_contract, signing_root):
#     FQ.field_modulus = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
#     FIELD_MODULUS = FQ(0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab)
#     points = proxy_contract.functions.signature_to_g2_points(signing_root).call()
#     first_g2 = points[0]
#     second_g2 = points[1]
#     first_g2_pyecc =[]
#     for tup in first_g2:
#         p = []
#         for f in tup:
#             p.append(FQ(utils.convert_fp_to_int(f)))
#
#         p = FQ2(p)
#         first_g2_pyecc.append(p);
#     
#     first_g2_pyecc.append(FQ2.one());
#     first_g2_pyecc = tuple(first_g2_pyecc)
#
#     second_g2_pyecc =[]
#     for tup in second_g2:
#         p = []
#         for f in tup:
#             p.append(FQ(utils.convert_fp_to_int(f)))
#
#         p = FQ2(p)
#         second_g2_pyecc.append(p);
#     
#
#     second_g2_pyecc.append(FQ2.one());
#     second_g2_pyecc = tuple(second_g2_pyecc)
#     result, v, v_sqr = addTest(first_g2_pyecc,second_g2_pyecc)
#     print(f"       {v.coeffs = }")
#     v_repr = utils.convert_int_to_fp2_repr(v)
#     actual_repr = proxy_contract.functions.lmul(v_repr, v_repr).call()
#     # _, a, b = actual_repr
#     expected = v*v
#     print(f"actual_repr: {actual_repr}")
#     actual = FQ2([FQ(utils.convert_fp_to_int(repr)) for repr in actual_repr])
#     print(f"actual: {actual}")
#     # print(f"actual: {actual}")
#     print(f"expected: {expected}")
#     # expected_repr = utils.convert_fp2_to_int(expected)
#     # print(f"expected_repr: {expected_repr}")
#     print(f"expected_repr: {expected.coeffs = }")
#     expected_repr = [utils.convert_int_to_fp_repr(repr) for repr in expected.coeffs]
#     # # print(f"actual: {utils.convert_huge_fp_to_int(actual_repr)}")
#     print(f"{expected_repr = }")
#
#     assert expected == actual

@pytest.mark.skip(reason="no way of currently testing this")
def test_ladd_G2_1(proxy_contract, signing_root):
    FQ.field_modulus = 0xfa0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    FIELD_MODULUS = FQ(0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab)
    # expected1 = proxy_contract.functions.hashToCurve(signing_root).call()
    points = proxy_contract.functions.signature_to_g2_points(signing_root).call()
    # expected = tuple(utils.convert_fp2_to_int(fp2_repr) for fp2_repr in expected1)
    # spec_result = normalize(hash_to_G2(signing_root, dst, hashlib.sha256))
    # expected1 = tuple(utils.convert_fp2_to_int(fp2_repr) for fp2_repr in expected1)
    first_g2 = points[0]
    second_g2 = points[1]
    # first_g2_ecc = [FQ2([) for tup in first_g2]
    first_g2_pyecc =[]
    for tup in first_g2:
        p = []
        for f in tup:
            p.append(FQ(utils.convert_fp_to_int(f)))

        p = FQ2(p)
        first_g2_pyecc.append(p);
    
    first_g2_pyecc.append(FQ2.one());
    first_g2_pyecc = tuple(first_g2_pyecc)

    second_g2_pyecc =[]
    for tup in second_g2:
        p = []
        for f in tup:
            p.append(FQ(utils.convert_fp_to_int(f)))

        p = FQ2(p)
        second_g2_pyecc.append(p);
    
    second_g2_pyecc.append(FQ2.one());
    second_g2_pyecc = tuple(second_g2_pyecc)
    result, v_sqr_times_v2, v_cubed, w = addTest(first_g2_pyecc,second_g2_pyecc)
    first_g2_pyecc = tuple(first_g2_pyecc)
    # exp1 = proxy_contract.functions.addG2(first_g2, second_g2).call()
    actual1 = proxy_contract.functions.addG2NoPrecompile(first_g2, second_g2).call()
    # exp = tuple(utils.convert_fp2_to_int(fp2_repr) for fp2_repr in exp1)
    actual = tuple(utils.convert_fp2_to_int(fp2_repr) for fp2_repr in actual1)
    print(f"modulus: {FIELD_MODULUS}")
    # print(f"IN_V: {actual[1]}")
    print(f"HERE: {actual[2]}")
    print(f"vtimesv2: {v_sqr_times_v2}")
    print(f"v_cubed: {v_cubed}")
    print(f"w: {w}")
    assert result[0] == actual[0]
    # assert result[2] == actual[2]
    assert result[1] == actual[1]
    # assert v_cubed == actual[1]
    # assert w == actual[2]
    result = normalize(result)
    actual = normalize(actual)

    # assert exp == expected
    assert result == actual
    # assert actual == expected

def test_fast_exp_odd(proxy_contract, signing_root):
    FQ.field_modulus = 0xfa0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    field_elements_parts = proxy_contract.functions.hashToField(signing_root).call()
    field_elements = tuple(
        utils.convert_fp2_to_int(fp2_repr) for fp2_repr in field_elements_parts
    )

    # NOTE: mapToCurve (called below) precompile includes "clearing the cofactor"
    # first_group_element = normalize(
    #     clear_cofactor_G2(map_to_curve_G2(field_elements[0]))
    # )
    (v, u, _) = optimized_swu_G2_partial(field_elements[0])
    v_fp2 = tuple(
        utils.convert_fp2_to_int(fp2_repr) for fp2_repr in field_elements_parts
    )
    print(v)
    expected = exponentiateBy(v, 7)

    v_repr = tuple([utils.convert_int_to_fp_repr(fp) for fp in v.coeffs])

    actual = proxy_contract.functions.fastExp(v_repr, 7).call()
    actual = utils.convert_fp2_to_int(actual)
    print(f"expected: {expected}")
    print(f"actual: {actual}")
    assert actual == expected

def test_fast_exp_even(proxy_contract, signing_root):
    FQ.field_modulus = 0xfa0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    field_elements_parts = proxy_contract.functions.hashToField(signing_root).call()
    field_elements = tuple(
        utils.convert_fp2_to_int(fp2_repr) for fp2_repr in field_elements_parts
    )

    # NOTE: mapToCurve (called below) precompile includes "clearing the cofactor"
    # first_group_element = normalize(
    #     clear_cofactor_G2(map_to_curve_G2(field_elements[0]))
    # )
    (v, u, _) = optimized_swu_G2_partial(field_elements[0])
    v_fp2 = tuple(
        utils.convert_fp2_to_int(fp2_repr) for fp2_repr in field_elements_parts
    )
    print(v)
    expected = exponentiateBy(v, 6)

    v_repr = tuple([utils.convert_int_to_fp_repr(fp) for fp in v.coeffs])

    actual = proxy_contract.functions.fastExp(v_repr, 6).call()
    actual = utils.convert_fp2_to_int(actual)
    print(f"expected: {expected}")
    print(f"actual: {actual}")
    assert actual == expected


def test_check_roots_0(w3, proxy_contract, signing_root):
    FQ.field_modulus = 0xfa0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    field_elements_parts = proxy_contract.functions.hashToField(signing_root).call()
    field_elements = tuple(
        utils.convert_fp2_to_int(fp2_repr) for fp2_repr in field_elements_parts
    )

    # NOTE: mapToCurve (called below) precompile includes "clearing the cofactor"
    # first_group_element = normalize(
    #     clear_cofactor_G2(map_to_curve_G2(field_elements[0]))
    # )
    (v, u, _) = optimized_swu_G2_partial(field_elements[0])
    (temp1, temp2, gamma) = sqrt_division_FQ2_partial(u, v)
    expected = sqrt_division_FQ2(u, v)
    me = w3.eth.accounts[0]
    balance = w3.eth.get_balance(me)
    gamma_repr = tuple([utils.convert_int_to_fp_repr(fp) for fp in gamma.coeffs])
    u_repr = tuple([utils.convert_int_to_fp_repr(fp) for fp in u.coeffs])
    v_repr = tuple([utils.convert_int_to_fp_repr(fp) for fp in v.coeffs])
    # actual = proxy_contract.functions.sqrtDivision(v_repr, u_repr).call()
    actual = proxy_contract.functions.checkRoots(gamma_repr, u_repr, v_repr).call({"from": me, "gas": '20000000'})
    # print(tx_hash)
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # print(tx_receipt)
    actual = tuple([actual[0], utils.convert_fp2_to_int(actual[1])])
    print(f"  actual[0]: {actual[0]}")
    print(f"expected[0]: {expected[0]}")
    print(f"  actual[1]: {actual[1]}")
    print(f"expected[1]: {expected[1]}")
    assert actual[0] == expected[0]
    assert actual[1] == expected[1]
    assert actual == expected

def test_check_roots_1(w3, proxy_contract, signing_root):
    FQ.field_modulus = 0xfa0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    field_elements_parts = proxy_contract.functions.hashToField(signing_root).call()
    field_elements = tuple(
        utils.convert_fp2_to_int(fp2_repr) for fp2_repr in field_elements_parts
    )

    # NOTE: mapToCurve (called below) precompile includes "clearing the cofactor"
    # first_group_element = normalize(
    #     clear_cofactor_G2(map_to_curve_G2(field_elements[0]))
    # )
    (v, u, _) = optimized_swu_G2_partial(field_elements[1])
    (temp1, temp2, gamma) = sqrt_division_FQ2_partial(u, v)
    expected = sqrt_division_FQ2(u, v)
    me = w3.eth.accounts[0]
    balance = w3.eth.get_balance(me)
    gamma_repr = tuple([utils.convert_int_to_fp_repr(fp) for fp in gamma.coeffs])
    u_repr = tuple([utils.convert_int_to_fp_repr(fp) for fp in u.coeffs])
    v_repr = tuple([utils.convert_int_to_fp_repr(fp) for fp in v.coeffs])
    # actual = proxy_contract.functions.sqrtDivision(v_repr, u_repr).call()
    actual = proxy_contract.functions.checkRoots(gamma_repr, u_repr, v_repr).call({"from": me, "gas": '20000000'})
    # print(tx_hash)
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # print(tx_receipt)
    actual = tuple([actual[0], utils.convert_fp2_to_int(actual[1])])
    print(f"  actual[0]: {actual[0]}")
    print(f"expected[0]: {expected[0]}")
    print(f"  actual[1]: {actual[1]}")
    print(f"expected[1]: {expected[1]}")
    assert actual[0] == expected[0]
    assert actual[1] == expected[1]
    assert actual == expected

def test_roots_of_unity(proxy_contract):
    expected = get_roots_of_unity()
    actual = proxy_contract.functions.get_roots_of_unity().call()
    actual = tuple(
        utils.convert_fp2_to_int(fp_repr) for fp_repr in actual
    )
    assert expected == actual

@pytest.mark.timeout(400)
def test_sqrt_division_fq2_gamma_0(w3, proxy_contract, signing_root):
    FQ.field_modulus = 0xfa0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    field_elements_parts = proxy_contract.functions.hashToField(signing_root).call()
    field_elements = tuple(
        utils.convert_fp2_to_int(fp2_repr) for fp2_repr in field_elements_parts
    )

    # NOTE: mapToCurve (called below) precompile includes "clearing the cofactor"
    # first_group_element = normalize(
    #     clear_cofactor_G2(map_to_curve_G2(field_elements[0]))
    # )
    (v, u, _) = optimized_swu_G2_partial(field_elements[0])
    expected = sqrt_division_FQ2_partial(u, v)
    me = w3.eth.accounts[0]
    balance = w3.eth.get_balance(me)
    v_repr = tuple([utils.convert_int_to_fp_repr(fp) for fp in v.coeffs])
    u_repr = tuple([utils.convert_int_to_fp_repr(fp) for fp in u.coeffs])
    # actual = proxy_contract.functions.sqrtDivision(v_repr, u_repr).call()
    actual = proxy_contract.functions.sqrtDivisionTest(u_repr, v_repr).call({"from": me, "gas": '20000000'})
    # print(tx_hash)
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # print(tx_receipt)
    actual = tuple(
        utils.convert_fp2_to_int(fp2_repr) for fp2_repr in actual
    )
    print(f"  actual[0]: {actual[0]}")
    print(f"expected[0]: {expected[0]}")
    print(f"  actual[1]: {actual[1]}")
    print(f"expected[1]: {expected[1]}")
    print(f"  actual[2]: {actual[2]}")
    print(f"expected[2]: {expected[2]}")
    assert actual[0] == expected[0]
    assert actual[1] == expected[1]
    assert actual[2] == expected[2]
    assert actual == expected

@pytest.mark.timeout(400)
def test_sqrt_division_fq2_gamma_1(w3, proxy_contract, signing_root):
    FQ.field_modulus = 0xfa0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    field_elements_parts = proxy_contract.functions.hashToField(signing_root).call()
    field_elements = tuple(
        utils.convert_fp2_to_int(fp2_repr) for fp2_repr in field_elements_parts
    )

    # NOTE: mapToCurve (called below) precompile includes "clearing the cofactor"
    # first_group_element = normalize(
    #     clear_cofactor_G2(map_to_curve_G2(field_elements[0]))
    # )
    (v, u, _) = optimized_swu_G2_partial(field_elements[1])
    expected = sqrt_division_FQ2_partial(u, v)
    me = w3.eth.accounts[0]
    balance = w3.eth.get_balance(me)
    v_repr = tuple([utils.convert_int_to_fp_repr(fp) for fp in v.coeffs])
    u_repr = tuple([utils.convert_int_to_fp_repr(fp) for fp in u.coeffs])
    # actual = proxy_contract.functions.sqrtDivision(v_repr, u_repr).call()
    actual = proxy_contract.functions.sqrtDivisionTest(u_repr, v_repr).call({"from": me, "gas": '20000000'})
    # print(tx_hash)
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # print(tx_receipt)
    actual = tuple(
        utils.convert_fp2_to_int(fp2_repr) for fp2_repr in actual
    )
    print(f"  actual[0]: {actual[0]}")
    print(f"expected[0]: {expected[0]}")
    print(f"  actual[1]: {actual[1]}")
    print(f"expected[1]: {expected[1]}")
    print(f"  actual[2]: {actual[2]}")
    print(f"expected[2]: {expected[2]}")
    assert actual[0] == expected[0]
    assert actual[1] == expected[1]
    assert actual[2] == expected[2]
    assert actual == expected

@pytest.mark.timeout(1500)
def test_sqrt_division_fq2_0(w3, proxy_contract, signing_root):
    FQ.field_modulus = 0xfa0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    field_elements_parts = proxy_contract.functions.hashToField(signing_root).call()
    field_elements = tuple(
        utils.convert_fp2_to_int(fp2_repr) for fp2_repr in field_elements_parts
    )

    # NOTE: mapToCurve (called below) precompile includes "clearing the cofactor"
    # first_group_element = normalize(
    #     clear_cofactor_G2(map_to_curve_G2(field_elements[0]))
    # )
    (v, u, _) = optimized_swu_G2_partial(field_elements[0])
    expected = sqrt_division_FQ2(u, v)
    me = w3.eth.accounts[0]
    balance = w3.eth.get_balance(me)
    v_repr = tuple([utils.convert_int_to_fp_repr(fp) for fp in v.coeffs])
    u_repr = tuple([utils.convert_int_to_fp_repr(fp) for fp in u.coeffs])
    # actual = proxy_contract.functions.sqrtDivision(v_repr, u_repr).call()
    actual = proxy_contract.functions.sqrtDivision(u_repr, v_repr).call({"from": me, "gas": '20000000'})
    # print(tx_hash)
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # print(tx_receipt)
    actual = tuple([actual[0], utils.convert_fp2_to_int(actual[1])])
    print(f"  actual[0]: {actual[0]}")
    print(f"expected[0]: {expected[0]}")
    print(f"  actual[1]: {actual[1]}")
    print(f"expected[1]: {expected[1]}")
    assert actual[0] == expected[0]
    assert actual[1] == expected[1]
    assert actual == expected

@pytest.mark.timeout(1500)
def test_sqrt_division_fq2_1(w3, proxy_contract, signing_root):
    FQ.field_modulus = 0xfa0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    field_elements_parts = proxy_contract.functions.hashToField(signing_root).call()
    field_elements = tuple(
        utils.convert_fp2_to_int(fp2_repr) for fp2_repr in field_elements_parts
    )

    # NOTE: mapToCurve (called below) precompile includes "clearing the cofactor"
    # first_group_element = normalize(
    #     clear_cofactor_G2(map_to_curve_G2(field_elements[0]))
    # )
    (v, u, _) = optimized_swu_G2_partial(field_elements[1])
    expected = sqrt_division_FQ2(u, v)
    me = w3.eth.accounts[0]
    balance = w3.eth.get_balance(me)
    v_repr = tuple([utils.convert_int_to_fp_repr(fp) for fp in v.coeffs])
    u_repr = tuple([utils.convert_int_to_fp_repr(fp) for fp in u.coeffs])
    # actual = proxy_contract.functions.sqrtDivision(v_repr, u_repr).call()
    actual = proxy_contract.functions.sqrtDivision(u_repr, v_repr).call({"from": me, "gas": '20000000'})
    # print(tx_hash)
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # print(tx_receipt)
    actual = tuple([actual[0], utils.convert_fp2_to_int(actual[1])])
    print(f"  actual[0]: {actual[0]}")
    print(f"expected[0]: {expected[0]}")
    print(f"  actual[1]: {actual[1]}")
    print(f"expected[1]: {expected[1]}")
    assert actual[0] == expected[0]
    assert actual[1] == expected[1]
    assert actual == expected

@pytest.mark.timeout(1500)
# @pytest.mark.skip(reason="no way of currently testing this due to removing precompiles")
def test_map_to_curve_matches_spec_0(w3, proxy_contract, signing_root):
    field_elements_parts = proxy_contract.functions.hashToField(signing_root).call()
    field_elements = tuple(
        utils.convert_fp2_to_int(fp2_repr) for fp2_repr in field_elements_parts
    )

    # NOTE: mapToCurve (called below) precompile includes "clearing the cofactor"
    # first_group_element = normalize(
    #     clear_cofactor_G2(map_to_curve_G2(field_elements[0]))
    # )
    (expected_suc, expected) = optimized_swu_G2_partial(field_elements[0])

    me = w3.eth.accounts[0]
    (actual_suc, actual) = proxy_contract.functions.mapToCurve(
        field_elements_parts[0]
    ).call({"from": me, "gas": '20000000'})
    actual = tuple(
        utils.convert_fp2_to_int(fp2_repr) for fp2_repr in actual
    )
    print("actual: {actual}")
    print("expected: {expected}")
    assert actual_suc == expected_suc
    assert actual[0] == expected[0]
    assert actual[1] == expected[1]
    assert actual[2] == expected[2]

@pytest.mark.timeout(1500)
# @pytest.mark.skip(reason="no way of currently testing this due to removing precompiles")
def test_map_to_curve_matches_spec_1(w3, proxy_contract, signing_root):
    field_elements_parts = proxy_contract.functions.hashToField(signing_root).call()
    field_elements = tuple(
        utils.convert_fp2_to_int(fp2_repr) for fp2_repr in field_elements_parts
    )
    (expected_suc, expected) = optimized_swu_G2_partial(field_elements[1])

    me = w3.eth.accounts[0]
    (actual_suc, actual) = proxy_contract.functions.mapToCurve(
        field_elements_parts[1]
    ).call({"from": me, "gas": '20000000'})
    actual = tuple(
        utils.convert_fp2_to_int(fp2_repr) for fp2_repr in actual
    )
    print("actual: {actual}")
    print("expected: {expected}")
    assert actual_suc == expected_suc
    assert actual[0] == expected[0]
    assert actual[1] == expected[1]
    assert actual[2] == expected[2]

@pytest.mark.skip(reason="no way of currently testing this due to removing precompiles")
def test_hash_g2_is_zero(proxy_contract, signing_root, dst):
    
    result = proxy_contract.functions.hashToCurve(signing_root).call()
    converted_result = tuple(utils.convert_fp2_to_int(fp2_repr) for fp2_repr in result)

    spec_result = normalize(hash_to_G2(signing_root, dst, hashlib.sha256))

    assert converted_result == spec_result

@pytest.mark.skip(reason="no way of currently testing this due to removing precompiles")
def test_hash_to_curve_matches_spec(proxy_contract, signing_root, dst):
    result = proxy_contract.functions.hashToCurve(signing_root).call()
    converted_result = tuple(utils.convert_fp2_to_int(fp2_repr) for fp2_repr in result)

    spec_result = normalize(hash_to_G2(signing_root, dst, hashlib.sha256))

    assert converted_result == spec_result

@pytest.mark.skip(reason="no way of currently testing this")
def test_hash_to_curve_no_precompile_matches_spec(proxy_contract, signing_root, dst):
    result = proxy_contract.functions.hashToCurveNoPrecompile(signing_root).call()
    expected1 = proxy_contract.functions.hashToCurve(signing_root).call()
    points = proxy_contract.functions.signature_to_g2_points(signing_root).call()
    converted_expected = tuple(utils.convert_fp2_to_int(fp2_repr) for fp2_repr in expected1)
    converted_result = tuple(utils.convert_fp2_to_int(fp2_repr) for fp2_repr in result)
    spec_result = normalize(hash_to_G2(signing_root, dst, hashlib.sha256))
    # converted_result = tuple(convert_fp2_to_int(fp2_repr) for fp2_repr in result)
    # expected1 = tuple(utils.convert_fp2_to_int(fp2_repr) for fp2_repr in expected1)
    first_g2 = points[0]
    second_g2 = points[1]
    print(f"expected: {converted_expected}")
    print(f"actual: {spec_result}")
    # print(f"first_point: {first_point}")
    first_g2_a = first_g2[0]
    first_g2_a_a = first_g2_a[0]
    first_g2_a_b = first_g2_a[1]
    first_g2_b = first_g2[1]
    first_g2_b_a = first_g2_b[0]
    first_g2_b_b = first_g2_b[1]
    second_g2_a = second_g2[0]
    second_g2_a_a = second_g2_a[0]
    second_g2_a_b = second_g2_a[1]
    second_g2_b = second_g2[1]
    second_g2_b_a = second_g2_b[0]
    second_g2_b_b = second_g2_b[1]
    print(f"first_point_g2_a_a: {first_g2_a_a}")
    print(f"first_point_g2_a_b: {first_g2_a_b}")
    print(f"first_point_g2_b_a: {first_g2_b_a}")
    print(f"first_point_g2_b_b: {first_g2_b_b}")

    print(f"second_point_g2_a_a: {second_g2_a_a}")
    print(f"second_point_g2_a_b: {second_g2_a_b}")
    print(f"second_point_g2_b_a: {second_g2_b_a}")
    print(f"second_point_g2_b_b: {second_g2_b_b}")

    # print(f"second_point: {second_point}")
    assert converted_expected == spec_result
    assert converted_result == spec_result

@pytest.mark.skip(reason="no way of currently testing this")
def test_hash_to_curve_no_precompile_matches_spec_2(proxy_contract, signing_root, dst):
    result = proxy_contract.functions.hashToCurveNoPrecompile(signing_root).call()
    expected = proxy_contract.functions.hashToCurve(signing_root).call()
    converted_result = tuple(convert_fp2_to_int(fp2_repr) for fp2_repr in result)
    # spec_result = normalize(hash_to_G2(signing_root, dst, hashlib.sha256))
    # print(f"expected: {converted_result}")
    # print(f"actual: {spec_result}")
    assert expected == result


@pytest.mark.skip(reason="function was commented out due to gas issues")
def test_bls_pairing_check(proxy_contract, signing_root, bls_public_key, signature):
    public_key_point = pubkey_to_G1(bls_public_key)
    public_key = normalize(public_key_point)
    public_key_repr = (
        utils.convert_int_to_fp_repr(public_key[0]),
        utils.convert_int_to_fp_repr(public_key[1]),
    )

    # skip some data wrangling by calling contract function for this...
    message_on_curve = proxy_contract.functions.hashToCurve(signing_root).call()

    projective_signature_point = signature_to_G2(signature)
    signature_point = normalize(projective_signature_point)
    signature_repr = (
        utils.convert_int_to_fp2_repr(signature_point[0]),
        utils.convert_int_to_fp2_repr(signature_point[1]),
    )
    assert proxy_contract.functions.blsPairingCheck(
        public_key_repr, message_on_curve, signature_repr
    ).call()


@pytest.mark.skip(reason="function was commented out due to gas issues")
def test_bls_signature_is_valid_works_with_valid_signature(
    proxy_contract,
    bls_public_key,
    signing_root,
    signature,
    public_key_witness,
    signature_witness,
):
    public_key_witness_repr = utils.convert_int_to_fp_repr(public_key_witness)
    signature_witness_repr = utils.convert_int_to_fp2_repr(signature_witness)

    assert proxy_contract.functions.blsSignatureIsValid(
        signing_root,
        bls_public_key,
        signature,
        public_key_witness_repr,
        signature_witness_repr,
    ).call()


@pytest.mark.skip(reason="function was commented out due to gas issues")
def test_bls_signature_is_valid_fails_with_invalid_message(
    proxy_contract,
    bls_public_key,
    signing_root,
    signature,
    public_key_witness,
    signature_witness,
):
    public_key_witness_repr = utils.convert_int_to_fp_repr(public_key_witness)
    signature_witness_repr = utils.convert_int_to_fp2_repr(signature_witness)

    message = b"\x01" + signing_root[1:]
    assert message != signing_root

    assert not proxy_contract.functions.blsSignatureIsValid(
        message,
        bls_public_key,
        signature,
        public_key_witness_repr,
        signature_witness_repr,
    ).call()


@pytest.mark.skip(reason="function was commented out due to gas issues")
def test_bls_signature_is_valid_fails_with_invalid_public_key(
    proxy_contract, seed, signing_root, signature, signature_witness
):
    another_seed = "another-secret".encode()
    assert seed != another_seed
    another_private_key = G2ProofOfPossession.KeyGen(another_seed)
    public_key = G2ProofOfPossession.SkToPk(another_private_key)

    group_element = pubkey_to_G1(public_key)
    normalized_group_element = normalize(group_element)
    public_key_witness = normalized_group_element[1]
    public_key_witness_repr = utils.convert_int_to_fp_repr(public_key_witness)

    signature_witness_repr = utils.convert_int_to_fp2_repr(signature_witness)

    assert not proxy_contract.functions.blsSignatureIsValid(
        signing_root,
        public_key,
        signature,
        public_key_witness_repr,
        signature_witness_repr,
    ).call()


@pytest.mark.skip(reason="function was commented out due to gas issues")
def test_bls_signature_is_valid_fails_with_invalid_signature(
    proxy_contract, bls_public_key, signing_root, public_key_witness, bls_private_key
):
    public_key_witness_repr = utils.convert_int_to_fp_repr(public_key_witness)

    another_message = hashlib.sha256(b"not the signing root").digest()
    assert signing_root != another_message
    signature = G2ProofOfPossession.Sign(bls_private_key, another_message)
    group_element = signature_to_G2(signature)
    normalized_group_element = normalize(group_element)
    signature_witness = normalized_group_element[1]

    signature_witness_repr = utils.convert_int_to_fp2_repr(signature_witness)

    assert not proxy_contract.functions.blsSignatureIsValid(
        signing_root,
        bls_public_key,
        signature,
        public_key_witness_repr,
        signature_witness_repr,
    ).call()
