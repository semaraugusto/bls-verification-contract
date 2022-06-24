from eth_utils import to_tuple
from py_ecc.fields import FQ, FQ2
from py_ecc.optimized_bls12_381 import FQ2, normalize

# def convert_int_to_fp_repr(field_element):
#     element_as_bytes = int(field_element).to_bytes(48, byteorder="big")
#     a_bytes = element_as_bytes[:16]
#     b_bytes = element_as_bytes[16:]
#     return (
#         int.from_bytes(a_bytes, byteorder="big"),
#         int.from_bytes(b_bytes, byteorder="big"),
#     )

def convert_g2_to_tuple(g2_point):
    g2_point_pyecc =[]
    for tup in g2_point:
        p = []
        for f in tup:
            p.append(FQ(convert_fp_to_int(f)))

        p = FQ2(p)
        g2_point_pyecc.append(p);
    
    g2_point_pyecc.append(FQ2.one());
    g2_point_pyecc = tuple(g2_point_pyecc)
    return g2_point_pyecc

def convert_int_to_fp_repr(field_element):
    element_as_bytes = int(field_element).to_bytes(48, byteorder="big")
    a_bytes = element_as_bytes[:16]
    b_bytes = element_as_bytes[16:]
    return (
        int.from_bytes(a_bytes, byteorder="big"),
        int.from_bytes(b_bytes, byteorder="big"),
    )

@to_tuple
def convert_int_to_fp2_repr(field_element):
    for coeff in field_element.coeffs:
        yield convert_int_to_fp_repr(coeff)

def convert_big_to_fp_repr(field_element):
    element_as_bytes = int(field_element).to_bytes(64, byteorder="big")
    a_bytes = element_as_bytes[:32]
    b_bytes = element_as_bytes[32:]
    return (
        int.from_bytes(a_bytes, byteorder="big"),
        int.from_bytes(b_bytes, byteorder="big"),
    )

def convert_huge_int_to_fp_repr(field_element):
    element_as_bytes = int(field_element).to_bytes(96, byteorder="big")
    a_bytes = element_as_bytes[:32]
    b_bytes = element_as_bytes[32:64]
    c_bytes = element_as_bytes[64:]
    return (
        int.from_bytes(a_bytes, byteorder="big"),
        int.from_bytes(b_bytes, byteorder="big"),
        int.from_bytes(c_bytes, byteorder="big"),
    )

def convert_huge_fp_to_int(fp_repr):
    a, b, c = fp_repr
    a_bytes = a.to_bytes(32, byteorder="big")
    b_bytes = b.to_bytes(32, byteorder="big")
    c_bytes = c.to_bytes(32, byteorder="big")
    full_bytes = b"".join((a_bytes, b_bytes, c_bytes))
    return int.from_bytes(full_bytes, byteorder="big")

# def convert_huge_to_int(fp_repr):
#     a, b, c = fp_repr
#     a_bytes = a.to_bytes(32, byteorder="big")
#     b_bytes = b.to_bytes(32, byteorder="big")
#     c_bytes = c.to_bytes(32, byteorder="big")
#     full_bytes = b"".join((a_bytes, b_bytes, c_bytes))
#     return int.from_bytes(full_bytes, byteorder="big")

def convert_huge_to_fp_repr(fp_repr):
    a, b, c = fp_repr
    # a_bytes = a.to_bytes(32, byteorder="big")
    # b_bytes = b.to_bytes(32, byteorder="big")
    # c_bytes = c.to_bytes(32, byteorder="big")
    # full_bytes = b"".join((a_bytes, b_bytes, c_bytes))
    return int.from_bytes(full_bytes, byteorder="big")

def convert_big_to_int(fp_repr):
    a, b = fp_repr
    a_bytes = a.to_bytes(32, byteorder="big")
    b_bytes = b.to_bytes(32, byteorder="big")
    full_bytes = b"".join((a_bytes, b_bytes))
    return int.from_bytes(full_bytes, byteorder="big")

def convert_fp_to_int(fp_repr):
    a, b = fp_repr
    a_bytes = a.to_bytes(16, byteorder="big")
    b_bytes = b.to_bytes(32, byteorder="big")
    full_bytes = b"".join((a_bytes, b_bytes))
    return int.from_bytes(full_bytes, byteorder="big")


def convert_fp2_to_int(fp2_repr):
    a, b = fp2_repr
    return FQ2((convert_fp_to_int(a), convert_fp_to_int(b)))
