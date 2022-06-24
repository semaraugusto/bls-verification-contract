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
