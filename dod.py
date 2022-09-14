import requests
import json

from_addy = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'

to_addy = '0x514910771AF9Ca656af840dff83E8264EcF986CA'
chain = '1'


url = 'https://route-api.dodoex.io/dodoapi/getdodoroute?fromTokenAddress='+str(from_addy)+'&fromTokenDecimals=6&toTokenAddress='+str(to_addy)+'&toTokenDecimals=6&fromAmount=5000000000000&slippage=1&userAddr=0x9f456D1633Df3DF0D65a7c0c553b2186151B622F&chainId='+str(chain)+'&deadLine=1650266245'

resp = requests.get(url)

resp = resp.json()

print(resp)