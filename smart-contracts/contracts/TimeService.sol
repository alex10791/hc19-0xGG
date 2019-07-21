pragma solidity ^0.5.10;

contract TimeService {

    address payable public owner;
    uint256 public create_timestamp;
    uint256 public end_timestamp;
    uint256 public funds;


    function() external payable {
        require(now > end_timestamp, "Contract already activated");
        create_timestamp = now;
        funds += msg.value;
        end_timestamp = create_timestamp + msg.value;
    }


    function getEndTime() public view returns (uint256) {
        require(now < end_timestamp, "Contract already activated");
        return end_timestamp;
    }


    function isActive() public view returns (bool) {
        return now < end_timestamp;
    }


    function withdraw() public payable {
        require(msg.sender == owner, "You must own the contract to withdraw");
        owner.transfer(funds);
        funds = 0;
    }


    constructor() public {
        owner = msg.sender;
        create_timestamp = 0;
        end_timestamp = 0;
        funds = 0;
    }

}
