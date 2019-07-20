const web3 = global.web3

var TimeService = artifacts.require("./TimeService.sol")

contract('TimeService', function(accounts) {


    let rpi = accounts[0]
    let user1 = accounts[1]
    let user2 = accounts[1]

    const timeTravel = function (time) {
        return new Promise((resolve, reject) => {
                web3.currentProvider.sendAsync({
                jsonrpc: "2.0",
                method: "evm_increaseTime",
                params: [time], // 86400 is num seconds in day
                id: new Date().getSeconds()
            }, (err, result) => {
                if(err){ return reject(err) }
                return resolve(result)
            })
        })
    }

    const mineBlock = function () {
        web3.currentProvider.send({jsonrpc: "2.0", method: "evm_mine", params: [], id: 0})
    }

    before(async function () {
        //Create contract instances

        timeService = await TimeService.new(
            {from: rpi}    // value: web3.toWei(200)
        )
    })

    it("rpi is the owner of TimeService", async function() {
        const ownerAddress = await timeService.owner.call({from: rpi})
        assert.equal(ownerAddress, rpi)
    })

    it("Check initial state", async function() {
        const create_timestamp = await timeService.create_timestamp.call({from: rpi})
        const end_timestamp = await timeService.end_timestamp.call({from: rpi})
        const funds = await timeService.funds.call({from: rpi})
        assert.equal(create_timestamp, 0, 'create_timestamp must be 0')
        assert.equal(end_timestamp, 0, 'end_timestamp must be 0')
        assert.equal(funds, 0, 'funds must be 0')
    })

    it("Should not get end time", async function() {
        let error
        try {
            const end_time = await timeService.getEndTime.call({from: rpi})
        } catch (err) {
            error = err
        }
        assert.notEqual(error, undefined, 'Error must be thrown')
    })

    it("Activated should be false", async function() {
        const end_time = await timeService.isActive.call({from: rpi})
        assert.equal(end_time, false, 'The contract should not be active')
    })

    it("Creation should succeed", async function() {
        wei = 10
        await timeTravel(3000);
        mineBlock();
        
        const end_time = await timeService.create({from: user1, value: wei})
        const create_timestamp = await timeService.create_timestamp.call({from: rpi})
        const end_timestamp = await timeService.end_timestamp.call({from: rpi})
        const funds = await timeService.funds.call({from: rpi})

        assert.notEqual(create_timestamp, 0, 'create_timestamp must not be 0')
        assert.notEqual(end_timestamp, 0, 'end_timestamp must not be 0')
        assert.equal(funds, wei, 'funds must be ' + wei)
        assert.equal(end_timestamp.toNumber(), create_timestamp.toNumber()+funds.toNumber(), 'end_timestamp must be equal to create_timestamp+funds')
    })

    it("Creation should fail", async function() {
        let error
        try {
            const end_time = await timeService.create({from: user2, value: wei})
        } catch (err) {
            error = err
        }
        assert.notEqual(error, undefined, 'Error must be thrown')
    })

    it("Should get end time", async function() {
        let error
        try {
            const end_time = await timeService.getEndTime.call({from: rpi})
        } catch (err) {
            error = err
        }
        assert.equal(error, undefined, 'Error must be thrown')
    })

    it("Activated should be true", async function() {
        const end_time = await timeService.isActive.call({from: rpi})
        assert.equal(end_time, true, 'The contract should be active')
    })

    it("Activated should be false when finished", async function() {
        await timeTravel(11);
        mineBlock()
        const end_time = await timeService.isActive.call({from: rpi})
        assert.equal(end_time, false, 'The contract should not be active')
    })

    it("Widthraw should fail", async function() {
        let error
        try {
            const widthraw = await timeService.withdraw({from: user1})
        } catch (err) {
            error = err
        }
        assert.notEqual(error, undefined, 'Error must be thrown')
    })

    it("Widthraw should succeed", async function() {
        let error
        try {
            const widthraw = await timeService.withdraw({from: rpi})
        } catch (err) {
            error = err
        }
        assert.equal(error, undefined, 'Error must not be thrown')
    })

});