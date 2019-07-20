
var TimeService = artifacts.require ("TimeService.sol");

module.exports = function (deployer) {
    deployer.deploy(TimeService);
};
