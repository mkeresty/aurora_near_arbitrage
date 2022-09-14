from web3 import Web3
from web3.middleware import geth_poa_middleware # Needed for Binance

from json import loads
from decimal import Decimal


ETHER = 10 ** 18

WBNB = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'


web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org:443'))

CAKE_ROUTER_V2 = web3.toChecksumAddress('0x10ed43c718714eb63d5aa57b78b54704e256024e')
web3.middleware_onion.inject(geth_poa_middleware, layer=0) # Again, this is needed for Binance, not Ethirium

ABI = loads('[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"}]')

def get_price(token, decimals, pair_contract, is_reversed, is_price_in_peg):
    peg_reserve = 0
    token_reserve = 0
    (reserve0, reserve1, blockTimestampLast) = pair_contract.functions.getReserves().call()
    
    if is_reversed:
        peg_reserve = reserve0
        token_reserve = reserve1
    else:
        peg_reserve = reserve1
        token_reserve = reserve0
    
    if token_reserve and peg_reserve:
        if is_price_in_peg:
            # CALCULATE PRICE BY TOKEN PER PEG
            price = (Decimal(token_reserve) / 10 ** decimals) / (Decimal(peg_reserve) / ETHER)
        else:
            # CALCULATE PRICE BY PEG PER TOKEN
            price = (Decimal(peg_reserve) / ETHER) / (Decimal(token_reserve) / 10 ** decimals)
        
        return price
        
    return Decimal('0')


if __name__ == '__main__':
    CAKE_FACTORY_V2 = web3.eth.contract(address=CAKE_ROUTER_V2, abi=ABI).functions.factory().call()

    token = web3.toChecksumAddress('0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d')
    pair = web3.eth.contract(address=CAKE_FACTORY_V2, abi=ABI).functions.getPair(token, WBNB).call()
    pair_contract = web3.eth.contract(address=pair, abi=ABI)
    is_reversed = pair_contract.functions.token0().call() == WBNB
    decimals = web3.eth.contract(address=token, abi=ABI).functions.decimals().call()
    is_price_in_peg = True

    print(get_price(token, decimals, pair_contract, is_reversed, is_price_in_peg), 'BNB')

