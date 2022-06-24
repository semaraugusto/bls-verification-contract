// SPDX-License-Identifier: The Unlicense
pragma solidity 0.8.14;
pragma experimental ABIEncoderV2;

interface IMath {
    function lmul(uint256 x, uint256 y) external pure returns (uint, uint);
    function bitLength(uint256 n) external pure returns (uint256);
    function lsub(uint256 x, uint256 y, uint256 carry) external pure returns (uint256, uint256);
    function lsub(uint256 x, uint256 y) external pure returns (uint256, uint256);
    function add(uint256 x, uint256 y) external pure returns (uint256, uint256);
    function add(uint256 x, uint256 y, uint256 carry) external pure returns (uint256, uint256);
    function expmod(bytes memory data, uint exponent, uint length) external view returns (uint, uint);
    function sliceToUintL(bytes memory data, uint start, uint end) external pure returns (uint);
    function sliceToUint(bytes memory data, uint start, uint end) external pure returns (uint);
    function cast(bool b) external pure returns (uint256 u);
}

library Math  {
    /* constructor() {} */

    uint8 constant MOD_EXP_PRECOMPILE_ADDRESS = 0x5;

    function lmul(uint256 x, uint256 y) internal pure returns (uint, uint) { unchecked {
        uint r0;
        uint r1;
        if(x == 0 || y == 0) {
            return (0, 0);
        }
        if(x == 1) {
            return (0, y);
        } else if(y == 1) {
            return (0, x);
        }
        assembly {
            let rem := mulmod(x, y, not(0))
            r0 := mul(x, y)
            r1 := sub(sub(rem, r0), lt(rem, r0))
        }
        return (r1, r0);
    }}

    function bitLength(uint256 n) internal pure returns (uint256) { unchecked {
        uint256 m;

        for (uint256 s = 128; s > 0; s >>= 1) {
            if (n >= 1 << s) {
                n >>= s;
                m |= s;
            }
        }

        return m + 1;
    }}

    function lsub(uint256 x, uint256 y, uint256 carry) internal pure returns (uint256, uint256) { unchecked {
        if (x > 0)
            return lsub(x - carry, y);
        if (y < type(uint256).max)
            return lsub(x, y + carry);
        return (1 - carry, 1);
    }}

    function lsub(uint256 x, uint256 y) internal pure returns (uint256, uint256) { unchecked {
        uint256 z = x - y;
        return (z, cast(z > x));
    }}
    function add(uint256 x, uint256 y) internal pure returns (uint256, uint256) { unchecked {
        uint256 z = x + y;
        return (z, cast(z < x));
    }}

    function add(uint256 x, uint256 y, uint256 carry) internal pure returns (uint256, uint256) { unchecked {
        if (x < type(uint256).max)
            return add(x + carry, y);
        if (y < type(uint256).max)
            return add(x, y + carry);
        return (type(uint256).max - 1 + carry, 1);
    }}


    function expmod(bytes memory data, uint exponent, uint length) internal view returns (uint, uint) {
        assert (length >= 0);
        assert (length <= data.length);

        bytes memory result = new bytes(48);

        bool success;
        assembly {
            let p := mload(0x40)
            // length of base
            mstore(p, length)
            // length of exponent
            mstore(add(p, 0x20), 0x20)
            // length of modulus
            mstore(add(p, 0x40), 48)
            // base
            // first, copy slice by chunks of EVM words
            let ctr := length
            let src := add(add(data, 0x20), 0)
            let dst := add(p, 0x60)
            for { }
                or(gt(ctr, 0x20), eq(ctr, 0x20))
                { ctr := sub(ctr, 0x20) }
            {
                mstore(dst, mload(src))
                dst := add(dst, 0x20)
                src := add(src, 0x20)
            }
            // next, copy remaining bytes in last partial word
            let mask := sub(exp(256, sub(0x20, ctr)), 1)
            let srcpart := and(mload(src), not(mask))
            let destpart := and(mload(dst), mask)
            mstore(dst, or(destpart, srcpart))
            // exponent
            mstore(add(p, add(0x60, length)), exponent)
            // modulus
            let modulusAddr := add(p, add(0x60, add(0x10, length)))
            mstore(modulusAddr, or(mload(modulusAddr), 0x1a0111ea397fe69a4b1ba7b6434bacd7)) // pt 1
            mstore(add(p, add(0x90, length)), 0x64774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab) // pt 2
            success := staticcall(
                sub(gas(), 2000),
                MOD_EXP_PRECOMPILE_ADDRESS,
                p,
                add(0xB0, length),
                add(result, 0x20),
                48)
            // Use "invalid" to make gas estimation work
            switch success case 0 { invalid() }
        }
        require(success, "call to modular exponentiation precompile failed");
        uint r1 = sliceToUintL(result, 0, 16);
        uint r0 = sliceToUintL(result, 16, 48);
        return (r1, r0);
    }

    function sliceToUintL(bytes memory data, uint start, uint end) internal pure returns (uint) {
        uint length = end - start;
        assert(length >= 0);
        assert(length <= 32);

        uint result;
        for (uint i = 0; i < length; i++) {
            bytes1 b = data[start+i];
            result = result + (uint8(b) * 2**(8*(length-i-1)));
        }
        return result;
    }
    function sliceToUint(bytes memory data, uint start, uint end) internal pure returns (uint) {
        uint length = end - start;
        assert(length >= 0);
        assert(length <= 32);

        uint result;
        for (uint i = 0; i < length; i++) {
            bytes1 b = data[start+i];
            result = result + (uint8(b) * 2**(8*(length-i-1)));
        }
        return result;
    }
    function cast(bool b) internal pure returns (uint256 u) { unchecked {
        assembly { u := b }
    }}
    // Reduce the number encoded as the big-endian slice of data[start:end] modulo the BLS12-381 field modulus.
    // Copying of the base is cribbed from the following:
    // https://github.com/ethereum/solidity-examples/blob/f44fe3b3b4cca94afe9c2a2d5b7840ff0fafb72e/src/unsafe/Memory.sol#L57-L74
    function reduceModulo(bytes memory data, uint start, uint end) internal view returns (bytes memory) {
        uint length = end - start;
        assert (length >= 0);
        assert (length <= data.length);

        bytes memory result = new bytes(48);

        bool success;
        assembly {
            let p := mload(0x40)
            // length of base
            mstore(p, length)
            // length of exponent
            mstore(add(p, 0x20), 0x20)
            // length of modulus
            mstore(add(p, 0x40), 48)
            // base
            // first, copy slice by chunks of EVM words
            let ctr := length
            let src := add(add(data, 0x20), start)
            let dst := add(p, 0x60)
            for { }
                or(gt(ctr, 0x20), eq(ctr, 0x20))
                { ctr := sub(ctr, 0x20) }
            {
                mstore(dst, mload(src))
                dst := add(dst, 0x20)
                src := add(src, 0x20)
            }
            // next, copy remaining bytes in last partial word
            let mask := sub(exp(256, sub(0x20, ctr)), 1)
            let srcpart := and(mload(src), not(mask))
            let destpart := and(mload(dst), mask)
            mstore(dst, or(destpart, srcpart))
            // exponent
            mstore(add(p, add(0x60, length)), 1)
            // modulus
            let modulusAddr := add(p, add(0x60, add(0x10, length)))
            mstore(modulusAddr, or(mload(modulusAddr), 0x1a0111ea397fe69a4b1ba7b6434bacd7)) // pt 1
            mstore(add(p, add(0x90, length)), 0x64774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab) // pt 2
            success := staticcall(
                sub(gas(), 2000),
                MOD_EXP_PRECOMPILE_ADDRESS,
                p,
                add(0xB0, length),
                add(result, 0x20),
                48)
            // Use "invalid" to make gas estimation work
            switch success case 0 { invalid() }
        }
        require(success, "call to modular exponentiation precompile failed");
        return result;
    }
}
