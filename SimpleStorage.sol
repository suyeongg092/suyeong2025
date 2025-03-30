// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 private value;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    function set(uint256 _value) public onlyOwner {
        value = _value;
    }

    function get() public view returns (uint256) {
        return value;
    }
}
