// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";
import "@chainlink/contracts/src/v0.8/ConfirmedOwner.sol";

contract ClientConsumer is ChainlinkClient, ConfirmedOwner {
  using Chainlink for Chainlink.Request;

  uint256 constant private ORACLE_PAYMENT = 1 * LINK_DIVISIBILITY;
  // bytes public message;

  mapping(uint256 => bytes) public hashes;
  uint256 totalHashes;

  event RequestHashFullFilled(
    bytes32 indexed requestId,
    bytes indexed message
  );

  constructor() ConfirmedOwner(msg.sender){
    setPublicChainlinkToken();
  }

  function requestHash(address _oracle, string memory _jobId, string memory _path)
    public
    onlyOwner
  {
    Chainlink.Request memory req = buildChainlinkRequest(stringToBytes32(_jobId), address(this), this.fulfill.selector);
    req.add("path", _path);
    req.addInt("times", 100);
    sendChainlinkRequestTo(_oracle, req, ORACLE_PAYMENT);
  }

  function fulfill(bytes32 _requestId, bytes memory _message)
    public
    recordChainlinkFulfillment(_requestId)
  {
    emit RequestHashFullFilled(_requestId, _message);

    bytes storage hash = hashes[totalHashes];
    hash = _message;

    totalHashes += 1;
  }

  function getChainlinkToken() public view returns (address) {
    return chainlinkTokenAddress();
  }

  function withdrawLink() public onlyOwner {
    LinkTokenInterface link = LinkTokenInterface(chainlinkTokenAddress());
    require(link.transfer(msg.sender, link.balanceOf(address(this))), "Unable to transfer");
  }

  function cancelRequest(
    bytes32 _requestId,
    uint256 _payment,
    bytes4 _callbackFunctionId,
    uint256 _expiration
  )
    public
    onlyOwner
  {
    cancelChainlinkRequest(_requestId, _payment, _callbackFunctionId, _expiration);
  }

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