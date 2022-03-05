// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";
import "@chainlink/contracts/src/v0.8/ConfirmedOwner.sol";

contract Validator is ChainlinkClient, ConfirmedOwner {
    using Chainlink for Chainlink.Request;

    uint256 constant private ORACLE_PAYMENT = 1 * LINK_DIVISIBILITY;

    string path;
    bool isValid;
    bytes hashIpfs;

    address oracle;
    string jobId;

    constructor(string memory _path, string memory _jobId, address _oracle) ConfirmedOwner(msg.sender) {  
        path = _path;
        jobId = _jobId;  
        oracle = _oracle;  

        setPublicChainlinkToken();
    }

    function setPath(
        string memory _jobId
    )
        public
        onlyOwner
    {
        jobId = _jobId;
    }

    function setOracle(
        address _oracle
    )
        public
        onlyOwner
    {
        oracle = _oracle;
    }

    function getHash() public view returns (bytes memory) {       
        return hashIpfs;       
    } 

    function getPath() public view returns (string memory) {       
        return path;       
    } 

    event RequestHashFullFilled(
        bytes32 indexed requestId,
        bytes indexed message
    );

    function requestUpdateHash()
        public
        onlyOwner
    {
        Chainlink.Request memory req = buildChainlinkRequest(stringToBytes32(jobId), address(this), this.fulfill.selector);
        req.add("path", path);
        req.addInt("times", 100);
        sendChainlinkRequestTo(oracle, req, ORACLE_PAYMENT);
    }

    function fulfill(bytes32 _requestId, bytes memory _message)
        public
        recordChainlinkFulfillment(_requestId)
    {
        emit RequestHashFullFilled(_requestId, _message);
        hashIpfs = _message;
    }


    // function getChainlinkToken() public view returns (address) {
    //     return chainlinkTokenAddress();
    // }

    // function withdrawLink() public onlyOwner {
    //     LinkTokenInterface link = LinkTokenInterface(chainlinkTokenAddress());
    //     require(link.transfer(msg.sender, link.balanceOf(address(this))), "Unable to transfer");
    // }

    // function cancelRequest(
    //     bytes32 _requestId,
    //     uint256 _payment,
    //     bytes4 _callbackFunctionId,
    //     uint256 _expiration
    // )
    //     public
    //     onlyOwner
    // {
    //     cancelChainlinkRequest(_requestId, _payment, _callbackFunctionId, _expiration);
    // }

    function stringToBytes32(string memory source) private pure returns (bytes32 result) {
        bytes memory tempEmptyStringTest = bytes(source);
        if (tempEmptyStringTest.length == 0) {
        return 0x0;
        }

        assembly { // solhint-disable-line no-inline-assembly
        result := mload(add(source, 32))
        }
    }
}