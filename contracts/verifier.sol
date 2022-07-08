// SPDX-License-Identifier: The Unlicense
pragma solidity 0.8.14;
pragma experimental ABIEncoderV2;
/* import "hardhat/console.sol"; */

/* import {Math} from "./libs/math.sol"; */
import {FpLib} from "./libs/FpLib.sol";
import {Math} from "./libs/math.sol";

contract Verifier  {
    uint constant PUBLIC_KEY_LENGTH = 48;
    uint constant SIGNATURE_LENGTH = 96;
    uint constant WITHDRAWAL_CREDENTIALS_LENGTH = 32;
    uint constant WEI_PER_GWEI = 1e9;
    uint constant UINT_MAX = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff;
    /* uint constant P_MINUS_9_DIV_16 = 1001205140483106588246484290269935788605945006208159541241399033561623546780709821462541004956387089373434649096260670658193992783731681621012512651314777238193313314641988297376025498093520728838658813979860931248214124593092835; */

    string constant BLS_SIG_DST = "BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_POP_+";
    bytes1 constant BLS_BYTE_WITHOUT_FLAGS_MASK = bytes1(0x1f);

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
    Fp2 ZERO = Fp2(FpLib.Fp(0, 0), FpLib.Fp(0, 0));
    uint256 constant BLS_BASE_FIELD_B = 0x64774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab;
    uint256 constant BLS_BASE_FIELD_A = 0x1a0111ea397fe69a4b1ba7b6434bacd7;
    FpLib.Fp BASE_FIELD = FpLib.Fp(BLS_BASE_FIELD_A, BLS_BASE_FIELD_B);

    uint256 P_MINUS_9_DIV_16_r2 = 0x2a437a4b8c35fc74bd278eaa22f25e9e2dc90e50e7046b466e59e49349e8bd;
    uint256 P_MINUS_9_DIV_16_r1 = 0x050a62cfd16ddca6ef53149330978ef011d68619c86185c7b292e85a87091a04;
    uint256 P_MINUS_9_DIV_16_r0 = 0x966bf91ed3e71b743162c338362113cfd7ced6b1d76382eab26aa00001c718e3;
    uint RV1_r1 = 0x6af0e0437ff400b6831e36d6bd17ffe;
    uint RV1_r0= 0x48395dabc2d3435e77f76e17009241c5ee67992f72ec05f4c81084fbede3cc09;
    FpLib.Fp RV1 = FpLib.Fp(RV1_r1, RV1_r0);

    Fp2 ISO_3_A = Fp2(FpLib.Fp(0, 0), FpLib.Fp(0, 240));
    Fp2 ISO_3_B = Fp2(FpLib.Fp(0, 1012), FpLib.Fp(0, 1012));
    Fp2 ISO_3_Z = Fp2(FpLib.lsub(BASE_FIELD, FpLib.Fp(0, 2)), FpLib.lsub(BASE_FIELD, FpLib.Fp(0, 1)));

    uint EV1_r1 = 0x699be3b8c6870965e5bf892ad5d2cc7;
    uint EV1_r0 = 0xb0e85a117402dfd83b7f4a947e02d978498255a2aaec0ac627b5afbdf1bf1c90;
    FpLib.Fp EV1 = FpLib.Fp(EV1_r1, EV1_r0);
    uint EV2_r1 = 0x8157cd83046453f5dd0972b6e3949e4;
    uint EV2_r0 = 0x288020b5b8a9cc99ca07e27089a2ce2436d965026adad3ef7baba37f2183e9b5;
    FpLib.Fp EV2 = FpLib.Fp(EV2_r1, EV2_r0);
    uint EV3_r1 = 0xab1c2ffdd6c253ca155231eb3e71ba0;
    uint EV3_r0 = 0x44fd562f6f72bc5bad5ec46a0b7a3b0247cf08ce6c6317f40edbc653a72dee17;
    FpLib.Fp EV3 = FpLib.Fp(EV3_r1, EV3_r0);
    uint EV4_r1 = 0xaa404866706722864480885d68ad0cc;
    uint EV4_r0 = 0xac1967c7544b447873cc37e0181271e006df72162a3d3e0287bf597fbf7f8fc1;
    FpLib.Fp EV4 = FpLib.Fp(EV4_r1, EV4_r0);
    /* Fp2[4] ETAS = [Fp2([EV1, EV2]), FQ2([-EV2, EV1]), FQ2([EV3, EV4]), FQ2([-EV4, EV3])] */
    
    /* Fp2 ISO_3_A = Fp2(FpLib.Fp(0, 0), FpLib.Fp(0, 240)); */
    /* Fp2 ISO_3_B = Fp2(FpLib.Fp(0, 1012), FpLib.Fp(0, 1012)); */
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

    function G2_isZeroNoPrecompile(Fp2 memory x, Fp2 memory y) public pure returns (bool) {
        return((x.a.a | x.a.b | x.b.a | x.b.b | y.a.a | y.a.b | y.b.a | y.b.b) == 0);
    }

    function lmul(Fp2 memory x, Fp2 memory y) public view returns (Fp2 memory) {
        /* Fp2 memory ONE = Fp2(FpLib.Fp(0, 1), FpLib.Fp(0, 0)); */
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
        
        return Fp2(r1, r0);
    }
    function lmul(Fp2 memory x, uint scalar) public view returns (Fp2 memory) {
        FpLib.Fp memory scalar_point = FpLib.Fp(0, scalar);
        if(scalar == 0) {
            // TODO: Fix this. Probably a bug, but dont know what to put instead
            return ONE;
        }

        // TODO: Check this logic
        FpLib.Fp memory r1 = FpLib.lmul(x.a, scalar_point); 
        FpLib.Fp memory r0 = FpLib.lmul(x.b, scalar_point); 
        return Fp2(r1, r0);
    }

    function lsquare(Fp2 memory x) public view returns (Fp2 memory) {
        return lmul(x, x);
    }

    function invert(Fp2 memory numb, Fp2 memory modulo) public view returns (Fp2 memory) { unchecked {
        FpLib.Fp memory factor = FpLib.ladd(FpLib.lmul(numb.a, numb.a), FpLib.lmul(numb.b, numb.b));
        return factor;
    }}

    function ldiv(Fp2 memory x, Fp2 memory y) public view returns (Fp2 memory) { unchecked {
        revert("not implemented!");
        /* FpLib.Fp memory a = FpLib.ldiv(x.a, y.a); */
        /* FpLib.Fp memory b = FpLib.ldiv(x.b, y.b); */
        /* return Fp2(a, b); */
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

    function addG2(G2Point memory a, G2Point memory b) public view returns (G2PointTmp memory) {
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
            /* Fp2 memory ONE = Fp2(FpLib.Fp(0, 1), FpLib.Fp(0, 0)); */
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
            Fp2 memory V_sqr_times_v2 = lmul(V_sqr, V2);
            Fp2 memory V_cubed = lmul(V_sqr, V);
            Fp2 memory W = lmul(ONE, ONE);
/* A = U * U * W - V_cubed - 2 * V_squared_times_V2 */
            Fp2 memory A1 = lmul(lmul(U, U), W);
            Fp2 memory A = lsub(lsub(A1, V_cubed), lmul(V_sqr_times_v2, 2));

            /* Fp2 memory A = lsub(lmul(lmul(U, U), W), V_cubed), ; */
            // reutilizing variables due to stack size
            // V1 = New X
            // V2 = New Y
            // A = New Z
            /* U1 = lsub(lsub(A1, V_cubed), A3); */
            V1 = lmul(V, A);
            V2 = lsub(lmul(U, lsub(V_sqr_times_v2, A)), lmul(V_cubed, U2));
            A = lmul(V_cubed, W);

            // TODO: normalize
            // (x / z, y / z)
            return G2PointTmp(V1, V2, A);
        }
    }
    function bigFastExp(Fp2 memory p, uint exp_r0, uint exp_r1, uint exp_r2) public view returns (Fp2 memory result) {
        require(exp_r1 > 0, "bigFastExp needs to receive a 784 non left padded value");
        require(exp_r2 > 0, "bigFastExp needs to receive a 784 non left padded value");
        Fp2 memory x = p;
        result = ONE;
        uint n = exp_r0;
        uint i;
        for (i = 0; i < 256; i++) {
        /* while (n > 0) { */
            if(n % 2 == 1) {
                result = lmul(result, x);
            }
            n = n>>1;
            x = lmul(x, x);
        }
        n = exp_r1;
        for (i = 0; i < 256; i++) {
        /* while (n > 0) { */
            if(n % 2 == 1) {
                result = lmul(result, x);
            }
            n = n>>1;
            x = lmul(x, x);
        }
        n = exp_r2;
        while (n > 0) {
            if(n % 2 == 1) {
                result = lmul(result, x);
            }
            n = n>>1;
            x = lmul(x, x);
        }
        return result;
    }

    function fastExp(Fp2 memory p, uint exp) public view returns (Fp2 memory result) {
        if(exp == 0) {
            return ONE;
        } else if (exp == 1) {
            return p;
        }
        Fp2 memory x = p;
        result = ONE;
        uint n = exp;
        while (n > 0) {
            if(n % 2 == 1) {
                result = lmul(result, x);
            }
            n = n>>1;
            x = lmul(x, x);
        }
        return result;
    }
    function get_roots_of_unity() public view returns (Fp2[] memory) {

        Fp2[] memory POSITIVE_EIGTH_ROOTS_OF_UNITY = new Fp2[](4);
        POSITIVE_EIGTH_ROOTS_OF_UNITY[0] = ONE;
        POSITIVE_EIGTH_ROOTS_OF_UNITY[1] = Fp2(FpLib.Fp(0, 0), FpLib.Fp(0, 1));
        POSITIVE_EIGTH_ROOTS_OF_UNITY[2] = Fp2(RV1, RV1);
        POSITIVE_EIGTH_ROOTS_OF_UNITY[3] = Fp2(RV1, FpLib.lsub(BASE_FIELD, RV1));

        return POSITIVE_EIGTH_ROOTS_OF_UNITY;
    }

    function get_etas() public view returns (Fp2[] memory) {

        Fp2[] memory ETAS = new Fp2[](4);
        ETAS[0] = Fp2(EV1, EV2);
        ETAS[1] = Fp2(FpLib.lsub(BASE_FIELD, EV2), EV1);
        ETAS[2] = Fp2(EV3, EV4);
        ETAS[3] = Fp2(FpLib.lsub(BASE_FIELD, EV4), EV3);
        /* ETAS[2] = Fp2(RV1, RV1); */
        /* ETAS[3] = Fp2(RV1, FpLib.lsub(BASE_FIELD, RV1)); */

        return ETAS;
    }

    function checkRoots(Fp2 memory gamma, Fp2 memory u, Fp2 memory v) public view returns (bool, Fp2 memory) {
        Fp2[] memory POSITIVE_EIGTH_ROOTS_OF_UNITY;
        POSITIVE_EIGTH_ROOTS_OF_UNITY = get_roots_of_unity();
        Fp2 memory result;
        bool is_valid_root = false;
        for(uint i = 0; i < 4; i++) {
            // Valid if (root * gamma)^2 * v - u == 0
            Fp2 memory root = POSITIVE_EIGTH_ROOTS_OF_UNITY[i];
            Fp2 memory sqrt_candidate = lmul(root, gamma);
            Fp2 memory temp2 = lsub(lmul(lmul(sqrt_candidate, sqrt_candidate), v), u);
            if (leq(temp2, ZERO) && !is_valid_root) {
                is_valid_root = true;
                result = sqrt_candidate;
            }
        }
        return (is_valid_root, result);
    }

    // Square Root Division
    // Return: uv^7 * (uv^15)^((p^2 - 9) / 16) * root of unity
    // If valid square root is found return true, else false
    function sqrtDivision(Fp2 memory u, Fp2 memory v) public view returns (bool, Fp2 memory) {

        Fp2 memory v7 = fastExp(v, 7);
        // uv^7
        Fp2 memory temp1 = lmul(u, v7);

        // uv^15
        Fp2 memory temp2 = lmul(temp1, lmul(v7, v));

        // gamma =  uv^7 * (uv^15)^((p^2 - 9) / 16)
        /* Fp2 memory gamma = temp2; */
        Fp2 memory gamma = bigFastExp(temp2, P_MINUS_9_DIV_16_r0, P_MINUS_9_DIV_16_r1, P_MINUS_9_DIV_16_r2);
        gamma = lmul(gamma, temp1);

        return checkRoots(gamma, u, v);
    }
    function sqrtDivisionTest(Fp2 memory u, Fp2 memory v) public view returns (G2PointTmp memory result) {

        Fp2 memory v7 = fastExp(v, 7);
        // uv^7
        Fp2 memory temp1 = lmul(u, v7);

        // uv^15
        Fp2 memory temp2 = lmul(temp1, lmul(v7, v));

        // gamma =  uv^7 * (uv^15)^((p^2 - 9) / 16)
        /* Fp2 memory gamma = temp2; */
        Fp2 memory gamma = bigFastExp(temp2, P_MINUS_9_DIV_16_r0, P_MINUS_9_DIV_16_r1, P_MINUS_9_DIV_16_r2);
        gamma = lmul(gamma, temp1);

        return G2PointTmp(temp1, temp2, gamma);
    }


    function mapToCurveGetFraction(Fp2 memory t) public view returns (Fp2 memory, Fp2 memory, Fp2 memory) {
        Fp2 memory t2 = lmul(t, t);
        Fp2 memory iso_3_z_t2 = lmul(ISO_3_Z, t2);
        Fp2 memory iso_3_z_t2_sqr = lmul(iso_3_z_t2, iso_3_z_t2);
        Fp2 memory temp = ladd(iso_3_z_t2, iso_3_z_t2_sqr);
        /* t2 = lmul(temp, ISO_3_A); */
        Fp2 memory denominator = lsub(ZERO, lmul(temp, ISO_3_A));
        temp = ladd(temp, ONE);
        Fp2 memory numerator = lmul(ISO_3_B, temp);
        if (leq(denominator, ZERO)) {
            denominator = lmul(ISO_3_Z, ISO_3_A);
        }
        return (iso_3_z_t2, numerator, denominator);
    }
    function mapToCurveGetUV(Fp2 memory numerator, Fp2 memory denominator) public view returns (Fp2 memory, Fp2 memory) {
        Fp2 memory denominator_sqr = lmul(denominator, denominator);

        Fp2 memory v = lmul(denominator, denominator_sqr);
        Fp2 memory temp1 = lmul(lmul(numerator, ISO_3_A), denominator_sqr);
        Fp2 memory temp2 = lmul(ISO_3_B, v);
        Fp2 memory numerator_sqr = lmul(numerator, numerator);
        Fp2 memory numerator_cube = lmul(numerator_sqr, numerator);
        Fp2 memory u = ladd(ladd(numerator_cube, temp1), temp2);
        return (u, v);
    }

    function mapToCurveGetDivisionParams(Fp2 memory t, Fp2 memory iso_3_z_t2, Fp2 memory numerator, Fp2 memory denominator) public view returns (bool, Fp2 memory, Fp2 memory, Fp2 memory, Fp2 memory) {

        Fp2 memory t3 = fastExp(t, 3);
        Fp2 memory iso_3_z_t2_cube = fastExp(iso_3_z_t2, 3);
        /* Fp2 memory denominator_sqr = lmul(denominator, denominator); */

        /* Fp2 memory v = lmul(denominator, denominator_sqr); */
        /* // t2, temp being used as temporary variable */
        /* // t2 == (ISO_3_A * numerator * (denominator ** 2)) */
        /* // temp == (ISO_3_B * v) */
        /* Fp2 memory temp1 = lmul(lmul(numerator, ISO_3_A), denominator_sqr); */
        /* Fp2 memory temp2 = lmul(ISO_3_B, v); */
        /* Fp2 memory numerator_sqr = lmul(numerator, numerator); */
        /* Fp2 memory numerator_cube = lmul(numerator_sqr, numerator); */
        /* Fp2 memory u = ladd(ladd(numerator_cube, temp1), temp2); */
        Fp2 memory u;
        Fp2 memory v;
        (u, v) = mapToCurveGetUV(numerator, denominator);
        bool success;
        Fp2 memory sqrt_candidate;
        (success, sqrt_candidate) = sqrtDivision(u, v);
        Fp2 memory y = sqrt_candidate;
        // sqrt_candidate = sqrt_candidate * t ** 3
        sqrt_candidate = lmul(sqrt_candidate, t3);

        // u(x1) = Z^3 * t^6 * u(x0)
        // u = (iso_3_z_t2) ** 3 * u
        u = lmul(iso_3_z_t2_cube, u);

        return (success, u, v, y, sqrt_candidate);
    }

    // Optimized SWU Map - FQ2 to G2': y^2 = x^3 + 240i * x + 1012 + 1012i
    // Found in Section 4 of https://eprint.iacr.org/2019/403
    function mapToCurve(Fp2 memory t) public view returns (bool, G2PointTmp memory result) {
        Fp2 memory numerator;
        Fp2 memory denominator;
        Fp2 memory iso_3_z_t2;
        (iso_3_z_t2, numerator, denominator) = mapToCurveGetFraction(t);
        Fp2 memory v;
        Fp2 memory u;
        Fp2 memory sqrt_candidate;
        Fp2 memory y;
        bool success;
        (success, u, v, y, sqrt_candidate) = mapToCurveGetDivisionParams(t, iso_3_z_t2, numerator, denominator);
        bool success_2 = false;
        /* Fp2 memory y = sqrt_candidate; */
        if(!success) {
            Fp2[] memory etas = get_etas();
            for(uint i = 0; i < etas.length; i++) {
            /* eta_sqrt_candidate = eta * sqrt_candidate */
                Fp2 memory eta_sqrt_candidate = lmul(sqrt_candidate, etas[i]);
            /* temp1 = eta_sqrt_candidate ** 2 * v - u */
                Fp2 memory eta_sqrt_candidate_sqr = lmul(eta_sqrt_candidate, eta_sqrt_candidate);
                Fp2 memory temp1 = lsub(lmul(eta_sqrt_candidate_sqr, v), u);
            /* if temp1 == FQ2.zero() and not success and not success_2: */
            /*     y = eta_sqrt_candidate */
            /*     success_2 = True */
                if(leq(temp1, ZERO) && !success_2) {
                    y = eta_sqrt_candidate;
                    success_2 = true;
                }
            }
        }
        if(!success && !success_2) {
            revert("Hash to curve - optimized swu failure");
        }

        if (!success) {
            numerator = lmul(numerator, iso_3_z_t2);
        }


        // TODO: Check wtf is this
        /* if t.sgn0 != y.sgn0: */
        /*     y = -y */

        y = lmul(y, denominator);
        /* result = G2PointTmp(numerator, denominator, y); */

        result = G2PointTmp(numerator, y, denominator);
        // normalize (x / z, y / z)
        /* u = ldiv(numerator, denominator); */
        /* v = ldiv(y, denominator); */

        return (success, result);
        /* result = G2PointTmp(v, u, sqrt_candidate); */
        /* result = G2PointTmp(v, u, u); */
        /* return result; */
    }

    /* function signature_to_g2_points(bytes32 message) public view returns (G2Point memory, G2Point memory) { */
    /*     Fp2[2] memory messageElementsInField = hashToField(message); */
    /*     G2Point memory firstPoint = mapToCurve(messageElementsInField[0]); */
    /*     G2Point memory secondPoint = mapToCurve(messageElementsInField[1]); */
    /*     return (firstPoint, secondPoint); */
    /* } */

    function decodeG1Point(bytes memory encodedX, FpLib.Fp memory Y) private pure returns (G1Point memory) {
        encodedX[0] = encodedX[0] & BLS_BYTE_WITHOUT_FLAGS_MASK;
        uint a = Math.sliceToUint(encodedX, 0, 16);
        uint b = Math.sliceToUint(encodedX, 16, 48);
        FpLib.Fp memory X = FpLib.Fp(a, b);
        return G1Point(X,Y);
    }

    function decodeG2Point(bytes memory encodedX, Fp2 memory Y) private pure returns (G2Point memory) {
        encodedX[0] = encodedX[0] & BLS_BYTE_WITHOUT_FLAGS_MASK;
        // NOTE: the "flag bits" of the second half of `encodedX` are always == 0x0

        // NOTE: order is important here for decoding point...
        uint aa = Math.sliceToUint(encodedX, 48, 64);
        uint ab = Math.sliceToUint(encodedX, 64, 96);
        uint ba = Math.sliceToUint(encodedX, 0, 16);
        uint bb = Math.sliceToUint(encodedX, 16, 48);
        Fp2 memory X = Fp2(
            FpLib.Fp(aa, ab),
            FpLib.Fp(ba, bb)
        );
        return G2Point(X, Y);
    }
    /* function hashToCurve(bytes32 message) public view returns (G2PointTmp memory) { */
    /*     Fp2[2] memory messageElementsInField = hashToField(message); */
    /*     bool suc1; */
    /*     bool suc2; */
    /*     G2PointTmp memory firstPoint; */
    /*     G2PointTmp memory secondPoint; */
    /*     (suc1, firstPoint) = mapToCurve(messageElementsInField[0]); */
    /*     (suc2, secondPoint) = mapToCurve(messageElementsInField[1]); */
    /*     return addG2(firstPoint, secondPoint); */
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
    /*     return blsPairingCheck(publicKey, messageOnCurve, signature); */
    /* } */
}

