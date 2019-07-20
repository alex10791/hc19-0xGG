from web3 import Web3, HTTPProvider

class TimeService:

    def __init__(self, address, endpoint_uri='https://ropsten.infura.io/v3/26a6ff1496c847c08fde23842f92428c'):
        web3 = Web3(HTTPProvider(endpoint_uri=endpoint_uri))
        contract_address = web3.toChecksumAddress(address)
        contract_abi = '[{"constant":false,"inputs":[],"name":"create","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[],"name":"withdraw","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"constant":true,"inputs":[],"name":"create_timestamp","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"end_timestamp","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"funds","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getEndTime","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"isActive","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"}]'
        self.contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    def is_active(self):
        return self.contract.functions.isActive().call()

    def get_end_time(self):
        return self.contract.functions.getEndTime().call()


if __name__ == "__main__":
    time_service = TimeService('0x5f84CC9A8fcB1B470489DaB7d13Ab4298eE08535')
    print(time_service.is_active())
    print(time_service.get_end_time())
