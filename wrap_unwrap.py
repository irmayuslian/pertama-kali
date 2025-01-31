from web3 import Web3, HTTPProvider
import json
import time

web3 = Web3(Web3.HTTPProvider(input("Input RPC Url with https:// : "))) #rpc url
chainId = web3.eth.chain_id

#connecting web3
if  web3.is_connected() == True:
    print("Web3 Connected...\n")
else:
    print("Error Connecting Please Try Again...")
    exit()

print('Auto Wrap Unwrap POL | By ADFMIDN Team')
payerkey = input('Input Privatekey EVM : ')
amount = input('Input Amount Of POL For Wrap Unwrap : ')
loop = input('How Many You Want To Transaction ? : ')
print('')
payer = web3.eth.account.from_key(payerkey)
tokenaddr = web3.to_checksum_address("0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270")
tokenabi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"src","type":"address"},{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"guy","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Withdrawal","type":"event"}]')
token_contract = web3.eth.contract(address=tokenaddr, abi=tokenabi)

def Unwrap(amount):
    try:
        nonce = web3.eth.get_transaction_count(payer.address)
        amountwei = web3.to_wei(amount, 'ether')
        gasAmount = token_contract.functions.withdraw(amountwei).estimate_gas({
            'chainId': chainId,
            'from': payer.address,
            'nonce': nonce
        })
        gasPrice = web3.eth.gas_price
        unwraptx = token_contract.functions.withdraw(amountwei).build_transaction({
            'chainId': chainId,
            'from': payer.address,
            'gas': gasAmount,
            'gasPrice': gasPrice,
            'nonce': nonce
        })
        #sign & send the transaction
        print(f'Processing Unwrap {amount} POL')
        tx_hash = web3.eth.send_raw_transaction(web3.eth.account.sign_transaction(unwraptx, payer.key).rawTransaction)
        #wait for transaction
        print(f'Wait For Transaction Until Mined...')
        transaction_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        #get transaction hash
        print(f'Processing Unwrap {amount} POL Success!')
        print(f'TX-ID : {str(web3.to_hex(tx_hash))}')
        print(f'')
    except Exception as e:
        print(f"Error: {e}")
        pass

def Wrap():
    try:
        nonce = web3.eth.get_transaction_count(payer.address)
        gasAmount = token_contract.functions.deposit().estimate_gas({
            'chainId': chainId,
            'from': payer.address,
            'value': web3.to_wei(amount, 'ether'),
            'nonce': nonce
        })
        gasPrice = web3.eth.gas_price
        wraptx = token_contract.functions.deposit().build_transaction({
            'chainId': chainId,
            'from': payer.address,
            'value': web3.to_wei(amount, 'ether'),
            'gas': gasAmount,
            'gasPrice': gasPrice,
            'nonce': nonce
        })
        #sign & send the transaction
        print(f'Processing Wrap {amount} POL')
        tx_hash = web3.eth.send_raw_transaction(web3.eth.account.sign_transaction(wraptx, payer.key).rawTransaction)
        #wait for transaction
        print(f'Wait For Transaction Until Mined...')
        transaction_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        #get transaction hash
        print(f'Processing Wrap {amount} POL Success!')
        print(f'TX-ID : {str(web3.to_hex(tx_hash))}')
        print(f'')
        Unwrap(amount)
    except Exception as e:
        print(f"Error: {e}")
        pass
        
for i in range(0,int(loop)):        
    Wrap()