import json
from web3 import Web3


infura_url = 'https://aurora-mainnet.infura.io/v3/'

a_url = 'https://mainnet.infura.io/v3/'

web3 = Web3(Web3.HTTPProvider(a_url))

pending = web3.geth.txpool.content()

print(pending)