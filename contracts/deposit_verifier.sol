// SPDX-License-Identifier: The Unlicense
pragma solidity 0.8.14;
pragma experimental ABIEncoderV2;

/* import {Math} from "./libs/math.sol"; */
import {FpLib} from "./libs/FpLib.sol";

contract DepositVerifier  {
    uint constant PUBLIC_KEY_LENGTH = 48;
    uint constant SIGNATURE_LENGTH = 96;
    uint constant WITHDRAWAL_CREDENTIALS_LENGTH = 32;
    uint constant WEI_PER_GWEI = 1e9;
    uint constant UINT_MAX = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff;

    string constant BLS_SIG_DST = "BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_POP_+";
    /* bytes1 constant BLS_BYTE_WITHOUT_FLAGS_MASK = bytes1(0x1f); */

    // Fp is a field element with the high-order part stored in `a`.

    // Fp2 is an extension field element with the coefficient of the
    // quadratic non-residue stored in `b`, i.e. p = a + i * b
    struct Fp2 {
        FpLib.Fp a;
        FpLib.Fp b;
    }

    // G1Point represents a point on BLS12-381 over Fp with coordinates (X,Y);
    struct G1Point {
        FpLib.Fp X;
        FpLib.Fp Y;
    }

    // G2Point represents a point on BLS12-381 over Fp2 with coordinates (X,Y);
    struct G2Point {
        Fp2 X;
        Fp2 Y;
    }
    struct G2PointTmp {
        Fp2 X;
        Fp2 Y;
        Fp2 Z;
    }
    Fp2 ONE = Fp2(FpLib.Fp(0, 1), FpLib.Fp(0, 0));
    uint256 constant BLS_BASE_FIELD_B = 0x64774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab;
    uint256 constant BLS_BASE_FIELD_A = 0x1a0111ea397fe69a4b1ba7b6434bacd7;
    FpLib.Fp BASE_FIELD = FpLib.Fp(BLS_BASE_FIELD_A, BLS_BASE_FIELD_B);
    /* Fp constant BASE_FIELD = Fp(BLS_BASE_FIELD_A, BLS_BASE_FIELD_B); */
    // uint constant BLS12_381_BASE_FIELD_MODULUS = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab;

    // uint constant BLS12_381_FP_QR_RES = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaaa;
    //
    // uint constant BLS12_381_G1_X = 0x17f1d3a73197d7942695638c4fa9ac0fc3688c4f9774b905a14e3a3f171bac586c55e83ff97a1aeffb3af00adb22c6bb;
    // uint constant BLS12_381_G1_Y = 0x08b3f481e3aaa0f1a09e30ed741d8ae4fcf5e095d5d00af600db18cb2c04b3edd03cc744a2888ae40caa232946c5e7e1;
    //
    // uint constant BLS12_381_G2_P1_X = 0x024aa2b2f08f0a91260805272dc51051c6e47ad4fa403b02b4510b647ae3d1770bac0326a805bbefd48056c8c121bdb8;
    // uint constant BLS12_381_G2_P1_Y = 0x0ce5d527727d6e118cc9cdc6da2e351aadfd9baa8cbdd3a76d429a695160d12c923ac9cc3baca289e193548608b82801;
    // uint constant BLS12_381_G2_P2_X = 0x13e02b6052719f607dacd3a088274f65596bd0d09920b61ab5da61bbdc7f5049334cf11213945d57e5ac7d055d042b7e;
    // uint constant BLS12_381_G2_P2_Y = 0x0606c4a02ea734cc32acd2b02bc28b99cb3e287e85a763af267492ab572e99ab3f370d275cec1da1aaa9075ff05f79be;
    //
    // Constant related to versioning serializations of deposits on eth2
    bytes32 immutable DEPOSIT_DOMAIN;

    uint256 MAX_U256 = 2**256-1;

    constructor(bytes32 deposit_domain) {
        DEPOSIT_DOMAIN = deposit_domain;
    }

    // Return a `wei` value in units of Gwei and serialize as a (LE) `bytes8`.
    function serializeAmount(uint amount) private pure returns (bytes memory) {
        uint depositAmount = amount / WEI_PER_GWEI;

        bytes memory encodedAmount = new bytes(8);

        for (uint i = 0; i < 8; i++) {
            encodedAmount[i] = bytes1(uint8(depositAmount / (2**(8*i))));
        }

        return encodedAmount;
    }

    // Compute the "signing root" from the deposit message. This root is the Merkle root
    // of a specific tree specified by SSZ serialization that takes as leaves chunks of 32 bytes.
    // NOTE: This computation is done manually in ``computeSigningRoot``.
    // NOTE: function is exposed for testing...
    function computeSigningRoot(
        bytes memory publicKey,
        bytes memory withdrawalCredentials,
        uint amount
    ) public view returns (bytes32) {
        bytes memory serializedPublicKey = new bytes(64);
        for (uint i = 0; i < PUBLIC_KEY_LENGTH; i++) {
            serializedPublicKey[i] = publicKey[i];
        }

        bytes32 publicKeyRoot = sha256(serializedPublicKey);
        bytes32 firstNode = sha256(abi.encodePacked(publicKeyRoot, withdrawalCredentials));

        bytes memory amountRoot = new bytes(64);
        bytes memory serializedAmount = serializeAmount(amount);
        for (uint i = 0; i < 8; i++) {
            amountRoot[i] = serializedAmount[i];
        }
        bytes32 secondNode = sha256(amountRoot);

        bytes32 depositMessageRoot = sha256(abi.encodePacked(firstNode, secondNode));
        return sha256(abi.encodePacked(depositMessageRoot, DEPOSIT_DOMAIN));
    }


    // NOTE: function exposed for testing...
    function expandMessage(bytes32 message) public pure returns (bytes memory) {
        bytes memory b0Input = new bytes(143);
        for (uint i = 0; i < 32; i++) {
            b0Input[i+64] = message[i];
        }
        b0Input[96] = 0x01;
        for (uint i = 0; i < 44; i++) {
            b0Input[i+99] = bytes(BLS_SIG_DST)[i];
        }

        bytes32 b0 = sha256(abi.encodePacked(b0Input));

        bytes memory output = new bytes(256);
        bytes32 chunk = sha256(abi.encodePacked(b0, bytes1(0x01), bytes(BLS_SIG_DST)));
        assembly {
            mstore(add(output, 0x20), chunk)
        }
        for (uint i = 2; i < 9; i++) {
            bytes32 input;
            assembly {
                input := xor(b0, mload(add(output, add(0x20, mul(0x20, sub(i, 2))))))
            }
            chunk = sha256(abi.encodePacked(input, bytes1(uint8(i)), bytes(BLS_SIG_DST)));
            assembly {
                mstore(add(output, add(0x20, mul(0x20, sub(i, 1)))), chunk)
            }
        }

        return output;
    }

    // NOTE: function is exposed for testing...
    function hashToField(bytes32 message) public view returns (Fp2[2] memory result) {
        bytes memory some_bytes = expandMessage(message);
        result[0] = Fp2(
            FpLib.convertSliceToFp(some_bytes, 0, 64),
            FpLib.convertSliceToFp(some_bytes, 64, 128)
        );
        result[1] = Fp2(
            FpLib.convertSliceToFp(some_bytes, 128, 192),
            FpLib.convertSliceToFp(some_bytes, 192, 256)
        );
    }

    function mapToCurve(Fp2 memory fieldElement) public view returns (G2Point memory result) {
        uint[4] memory input;
        input[0] = fieldElement.a.a;
        input[1] = fieldElement.a.b;
        input[2] = fieldElement.b.a;
        input[3] = fieldElement.b.b;

        uint[8] memory output;

        bool success;
        assembly {
            success := staticcall(
                sub(gas(), 2000),
                0x12,
                input,
                128,
                output,
                256
            )
            // Use "invalid" to make gas estimation work
            switch success case 0 { invalid() }
        }
        require(success, "call to map to curve precompile failed");

        return G2Point(
            Fp2(
                FpLib.Fp(output[0], output[1]),
                FpLib.Fp(output[2], output[3])
            ), 
            Fp2( 
                FpLib.Fp(output[4], output[5]),
                FpLib.Fp(output[6], output[7])
            )
        );
    }
    function G2_isZeroNoPrecompile(Fp2 memory x, Fp2 memory y) public pure returns (bool) {
        return((x.a.a | x.a.b | x.b.a | x.b.b | y.a.a | y.a.b | y.b.a | y.b.b) == 0);
    }

    /* function lmulTest(Fp2 memory x, Fp2 memory y) public view returns (Fp2 memory) { */
    /*     Fp2 memory ONE = Fp2(FpLib.Fp(0, 1), FpLib.Fp(0, 0)); */
    /*     if (leq(x, ONE)) { */
    /*         return y; */
    /*     } */
    /*     if (leq(y, ONE)) { */
    /*         return x; */
    /*     } */
    /*     FpLib.Fp memory r1 = FpLib.lmulTest(x.a, y.a);  */
    /*     FpLib.Fp memory r0 = FpLib.lmulTest(x.b, y.b);  */
    /*     return Fp2(r1, r0); */
    /* } */
    function lmul(Fp2 memory x, Fp2 memory y) public view returns (Fp2 memory) {
        Fp2 memory ONE = Fp2(FpLib.Fp(0, 1), FpLib.Fp(0, 0));
        if (leq(x, ONE)) {
            return y;
        }
        if (leq(y, ONE)) {
            return x;
        }
        // (a+bi)(c+di) = (ac−bd) + (ad+bc)i
        FpLib.Fp memory t1 = FpLib.lmul(x.a, y.a); 
        FpLib.Fp memory t0 = FpLib.lmul(x.b, y.b); 
        /* t1.subtract(t2),  */
        FpLib.Fp memory r1 = FpLib.lsub(t1, t0); 
        FpLib.Fp memory t1_plus_t0 = FpLib.ladd(t1, t0); 
        FpLib.Fp memory yb_plus_ya = FpLib.ladd(y.a, y.b); 
        FpLib.Fp memory xb_plus_xa = FpLib.ladd(x.a, x.b); 
        FpLib.Fp memory xy_mul = FpLib.lmul(xb_plus_xa, yb_plus_ya); 
        FpLib.Fp memory r0 = FpLib.lsub(xy_mul, t1_plus_t0); 
        

        /* FpLib.Fp memory r0 = FpLib.lmul(x.b, y.b);  */
        return Fp2(r1, r0);
// (T1 - T2) + (y. + c1) * (r0 + r1) - (T1 + T2))*i
        /* return Fp2( */
        /* t1.subtract(t2),  */
        /* r0 = y.b */
        /* r1 = y.a */
        /* c0.add(c1).multiply(r0.add(r1)).subtract(t1.add(t2)) */
    }
    function lmul(Fp2 memory x, uint scalar) public view returns (Fp2 memory) {
        FpLib.Fp memory scalar_point = FpLib.Fp(0, scalar);
        /* FpLib.Fp memory r1; */
        /* FpLib.Fp memory r0; */
        if(scalar == 0) {
            // TODO: Fix this. Probably a bug, but dont know what to put instead
            return ONE;
        }


        FpLib.Fp memory r1 = FpLib.lmul(x.a, scalar_point); 
        FpLib.Fp memory r0 = FpLib.lmul(x.b, scalar_point); 
        return Fp2(r1, r0);
    }

    function lsquare(Fp2 memory x) public view returns (Fp2 memory) {
        FpLib.Fp memory p1 = FpLib.lmul(x.a, x.a);
        FpLib.Fp memory p2 = FpLib.lmul(x.b, x.b);
        return Fp2(p1, p2);
    }


    function ldiv(Fp2 memory x, Fp2 memory y) public view returns (Fp2 memory) { unchecked {
        FpLib.Fp memory a = FpLib.ldiv(x.a, y.a);
        FpLib.Fp memory b = FpLib.ldiv(x.b, y.b);
        return Fp2(a, b);
    }}
    function lsub(Fp2 memory x, Fp2 memory y) public view returns (Fp2 memory) { unchecked {
        FpLib.Fp memory a = FpLib.lsub(x.a, y.a);
        FpLib.Fp memory b = FpLib.lsub(x.b, y.b);
        return Fp2(a, b);
    }}

    function ladd(Fp2 memory x, Fp2 memory y) public view returns (Fp2 memory) { unchecked {
        FpLib.Fp memory a = FpLib.ladd(x.a, y.a);
        FpLib.Fp memory b = FpLib.ladd(x.b, y.b);
        return Fp2(a, b);
    }}

    function leq(Fp2 memory x, Fp2 memory y) internal pure returns (bool) {
        return(FpLib.leq(x.a, y.a) && FpLib.leq(x.b, y.b));
        /* return(x.a == y.a && x.b == y.b); */
    }
    // TODO: Need to test this explicitly
    /* function doubleG2(G2Point memory a) public view returns (G2PointTmp memory) { */
    /*         Fp2 memory W = lmul(lmul(a.X, a.X), 3); */
    /*         Fp2 memory S = lmul(a.Y, ONE); */
    /*         Fp2 memory B = lmul(lmul(a.X, a.Y), S);  */
    /*         Fp2 memory H = lsub(lmul(W, W), lmul(B, 8));  */
    /*         Fp2 memory S_sqr = lsquare(S);  */
    /*          */
    /*         Fp2 memory X = lmul(lmul(H, S), 2); */
    /*         Fp2 memory Y_part1 = lmul(W, lsub(lmul(B, 4), H)); */
    /*         Fp2 memory Y_part2 = lmul(lmul(lsquare(a.Y), S_sqr), 8); */
    /*         Fp2 memory Y = lsub(Y_part1, Y_part2); */
    /*         Fp2 memory Z = lmul(lmul(S, S_sqr), 8); */
    /*         X = ldiv(X, Z); */
    /*         Y = ldiv(Y, Z); */
    /*         return G2PointTmp(X, Y, Z); */
    /**/
    /* } */

    function addG2NoPrecompile(G2Point memory a, G2Point memory b) public view returns (G2PointTmp memory) {
        if(G2_isZeroNoPrecompile(a.X, a.Y)) { 
            G2PointTmp memory res = G2PointTmp(b.X, b.Y, Fp2(FpLib.Fp(0,0), FpLib.Fp(0,0)));
            return res;
        }
        if (G2_isZeroNoPrecompile(b.X, b.Y)) { 
            G2PointTmp memory res = G2PointTmp(a.X, a.Y, Fp2(FpLib.Fp(0,0), FpLib.Fp(0,0)));
            return res;
        }
        if(leq(a.X, b.X) && leq(a.Y, b.Y)) {

        } else {
            Fp2 memory ONE = Fp2(FpLib.Fp(0, 1), FpLib.Fp(0, 0));
            Fp2 memory X;
            Fp2 memory Y;
            Fp2 memory Z;
            Fp2 memory U1 = lmul(b.Y, ONE);
            Fp2 memory U2 = lmul(a.Y, ONE);
            Fp2 memory V1 = lmul(b.X, ONE);
            Fp2 memory V2 = lmul(a.X, ONE);
            if (leq(V1, V2) && leq(U1, U2)) {
                // TODO: Change this to double function back
                return G2PointTmp(ONE, ONE, Fp2(FpLib.Fp(0,0), FpLib.Fp(0,0)));
                /* return doubleG2(a); */
            } else if (leq(V1, V2)) {
                return G2PointTmp(ONE, ONE, Fp2(FpLib.Fp(0,0), FpLib.Fp(0,0)));
            }
            Fp2 memory U = lsub(U1, U2);
            Fp2 memory V = lsub(V1, V2);
            Fp2 memory V_sqr = lmul(V, V);


            return G2PointTmp(U, V, V_sqr);

        }
    /* function addG2NoPrecompile(G2Point memory a, G2Point memory b) public view returns (G2PointTmp memory) { */
    /*     if(G2_isZeroNoPrecompile(a.X, a.Y)) {  */
    /*         G2PointTmp memory res = G2PointTmp(b.X, b.Y, Fp2(FpLib.Fp(0,0), FpLib.Fp(0,0))); */
    /*         return res; */
    /*     } */
    /*     if (G2_isZeroNoPrecompile(b.X, b.Y)) {  */
    /*         G2PointTmp memory res = G2PointTmp(a.X, a.Y, Fp2(FpLib.Fp(0,0), FpLib.Fp(0,0))); */
    /*         return res; */
    /*     } */
    /*     if(leq(a.X, b.X) && leq(a.Y, b.Y)) { */
    /**/
    /*     } else { */
    /*         Fp2 memory ONE = Fp2(FpLib.Fp(0, 1), FpLib.Fp(0, 0)); */
    /*         Fp2 memory X; */
    /*         Fp2 memory Y; */
    /*         Fp2 memory Z; */
    /*         Fp2 memory U1 = lmul(b.Y, ONE); */
    /*         Fp2 memory U2 = lmul(b.Y, ONE); */
    /*         Fp2 memory V1 = lmul(b.Y, ONE); */
    /*         Fp2 memory V2 = lmul(b.Y, ONE); */
    /**/
    /*         return G2PointTmp(X, Y, Z); */
    /**/
    /*     } */
        /* Fp2 memory X; */
        /* Fp2 memory Y; */
        /* Fp2 memory Z; */
        /* Fp2 memory y_sub = lsub(b.Y, a.Y); */
        /* Fp2 memory y_sub_sqr = lsquare(y_sub); */
        /* Fp2 memory x_sub = lsub(b.X, a.X); */
        /* Fp2 memory H = lsub(b.X, a.X); */
        /* Fp2 memory HH = lsquare(H); */
        /* Fp2 memory I = lmul(HH, 4); */
        /* Fp2 memory J = lmul(H, I); */
        /* Fp2 memory sub_res = lsub(b.Y, a.Y); */
        /* Fp2 memory r = lmul(lsub(b.Y, a.Y), 2); */
        /* Fp2 memory V = lmul(a.X, I); */
        /* X = lsub(lsub(lsquare(r), J), lmul(V, 2)); */
        /* Y = lsub(lmul(r, lsub(V, X)), lmul(lmul(a.Y, H), J)); */
        /* Z = lmul(H, 2); */
        /* return G2PointTmp(X, Y, Z); */
    }

    function addG2(G2Point memory a, G2Point memory b) public view returns (G2Point memory) {
        uint[16] memory input;
        input[0]  = a.X.a.a;
        input[1]  = a.X.a.b;
        input[2]  = a.X.b.a;
        input[3]  = a.X.b.b;
        input[4]  = a.Y.a.a;
        input[5]  = a.Y.a.b;
        input[6]  = a.Y.b.a;
        input[7]  = a.Y.b.b;

        input[8]  = b.X.a.a;
        input[9]  = b.X.a.b;
        input[10] = b.X.b.a;
        input[11] = b.X.b.b;
        input[12] = b.Y.a.a;
        input[13] = b.Y.a.b;
        input[14] = b.Y.b.a;
        input[15] = b.Y.b.b;

        uint[8] memory output;

        bool success;
        assembly {
            success := staticcall(
                sub(gas(), 2000),
                0xD,
                input,
                512,
                output,
                256
            )
            // Use "invalid" to make gas estimation work
            switch success case 0 { invalid() }
        }
        require(success, "call to addition in G2 precompile failed");

        return G2Point(
            Fp2(
                FpLib.Fp(output[0], output[1]),
                FpLib.Fp(output[2], output[3])
            ),
            Fp2(
                FpLib.Fp(output[4], output[5]),
                FpLib.Fp(output[6], output[7])
            )
        );
    }
    function signature_to_g2_points(bytes32 message) public view returns (G2Point memory, G2Point memory) {
        Fp2[2] memory messageElementsInField = hashToField(message);
        G2Point memory firstPoint = mapToCurve(messageElementsInField[0]);
        G2Point memory secondPoint = mapToCurve(messageElementsInField[1]);
        return (firstPoint, secondPoint);
    }

    // Implements "hash to the curve" from the IETF BLS draft.
    // NOTE: function is exposed for testing...
    /* function hashToCurveNoPrecompile(bytes32 message) public view returns (G2Point memory) { */
    /*     Fp2[2] memory messageElementsInField = hashToField(message); */
    /*     G2Point memory firstPoint = mapToCurve(messageElementsInField[0]); */
    /*     G2Point memory secondPoint = mapToCurve(messageElementsInField[1]); */
    /*     return addG2NoPrecompile(firstPoint, secondPoint); */
    /* } */
    // Implements "hash to the curve" from the IETF BLS draft.
    // NOTE: function is exposed for testing...
    function hashToCurve(bytes32 message) public view returns (G2Point memory) {
        Fp2[2] memory messageElementsInField = hashToField(message);
        G2Point memory firstPoint = mapToCurve(messageElementsInField[0]);
        G2Point memory secondPoint = mapToCurve(messageElementsInField[1]);
        return addG2(firstPoint, secondPoint);
    }

    // NOTE: function is exposed for testing...
    /* function blsPairingCheck(G1Point memory publicKey, G2Point memory messageOnCurve, G2Point memory signature) public view returns (bool) { */
    /*     uint[24] memory input; */
    /**/
    /*     input[0] =  publicKey.X.a; */
    /*     input[1] =  publicKey.X.b; */
    /*     input[2] =  publicKey.Y.a; */
    /*     input[3] =  publicKey.Y.b; */
    /**/
    /*     input[4] =  messageOnCurve.X.a.a; */
    /*     input[5] =  messageOnCurve.X.a.b; */
    /*     input[6] =  messageOnCurve.X.b.a; */
    /*     input[7] =  messageOnCurve.X.b.b; */
    /*     input[8] =  messageOnCurve.Y.a.a; */
    /*     input[9] =  messageOnCurve.Y.a.b; */
    /*     input[10] = messageOnCurve.Y.b.a; */
    /*     input[11] = messageOnCurve.Y.b.b; */
    /**/
    /*     // NOTE: this constant is -P1, where P1 is the generator of the group G1. */
    /*     input[12] = 31827880280837800241567138048534752271; */
    /*     input[13] = 88385725958748408079899006800036250932223001591707578097800747617502997169851; */
    /*     input[14] = 22997279242622214937712647648895181298; */
    /*     input[15] = 46816884707101390882112958134453447585552332943769894357249934112654335001290; */
    /**/
    /*     input[16] =  signature.X.a.a; */
    /*     input[17] =  signature.X.a.b; */
    /*     input[18] =  signature.X.b.a; */
    /*     input[19] =  signature.X.b.b; */
    /*     input[20] =  signature.Y.a.a; */
    /*     input[21] =  signature.Y.a.b; */
    /*     input[22] =  signature.Y.b.a; */
    /*     input[23] =  signature.Y.b.b; */
    /**/
    /*     uint[1] memory output; */
    /**/
    /*     bool success; */
    /*     assembly { */
    /*         success := staticcall( */
    /*             sub(gas(), 2000), */
    /*             0x10, */
    /*             input, */
    /*             768, */
    /*             output, */
    /*             32 */
    /*         ) */
    /*         // Use "invalid" to make gas estimation work */
    /*         switch success case 0 { invalid() } */
    /*     } */
    /*     require(success, "call to pairing precompile failed"); */
    /**/
    /*     return output[0] == 1; */
    /* } */
    /**/
    /* function decodeG1Point(bytes memory encodedX, FpLib.Fp memory Y) private pure returns (G1Point memory) { */
    /*     encodedX[0] = encodedX[0] & BLS_BYTE_WITHOUT_FLAGS_MASK; */
    /*     uint a = Math.sliceToUint(encodedX, 0, 16); */
    /*     uint b = Math.sliceToUint(encodedX, 16, 48); */
    /*     FpLib.Fp memory X = FpLib.Fp(a, b); */
    /*     return G1Point(X,Y); */
    /* } */
    /**/
    /* function decodeG2Point(bytes memory encodedX, Fp2 memory Y) private pure returns (G2Point memory) { */
    /*     encodedX[0] = encodedX[0] & BLS_BYTE_WITHOUT_FLAGS_MASK; */
    /*     // NOTE: the "flag bits" of the second half of `encodedX` are always == 0x0 */
    /**/
    /*     // NOTE: order is important here for decoding point... */
    /*     uint aa = Math.sliceToUint(encodedX, 48, 64); */
    /*     uint ab = Math.sliceToUint(encodedX, 64, 96); */
    /*     uint ba = Math.sliceToUint(encodedX, 0, 16); */
    /*     uint bb = Math.sliceToUint(encodedX, 16, 48); */
    /*     Fp2 memory X = Fp2( */
    /*         FpLib.Fp(aa, ab), */
    /*         FpLib.Fp(ba, bb) */
    /*     ); */
    /*     return G2Point(X, Y); */
    /* } */

    // NOTE: function is exposed for testing...
    /* function blsSignatureIsValid( */
    /*     bytes32 message, */
    /*     bytes memory encodedPublicKey, */
    /*     bytes memory encodedSignature, */
    /*     FpLib.Fp memory publicKeyYCoordinate, */
    /*     Fp2 memory signatureYCoordinate */
    /* ) public view returns (bool) { */
    /*     G1Point memory publicKey = decodeG1Point(encodedPublicKey, publicKeyYCoordinate); */
    /*     G2Point memory signature = decodeG2Point(encodedSignature, signatureYCoordinate); */
    /*     G2Point memory messageOnCurve = hashToCurve(message); */
    /**/
    /*     return blsPairingCheck(publicKey, messageOnCurve, signature); */
    /* } */
}

