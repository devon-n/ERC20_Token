from brownie import OurToken, network, config
from scripts.helpful_scripts import get_account
from web3 import Web3
import time

initial_supply = Web3.toWei(1000, 'ether')

def deploy_token():
    account = get_account()
    our_token = OurToken.deploy(initial_supply, {'from': account})
    print('Deployed Token: ', our_token.name())
    return our_token

def totalSupply():
    account = get_account()
    token = OurToken[-1]
    tx = token.totalSupply()
    # tx.wait(1)
    print('Token Supply: ', tx)

def balanceOf():
    account = get_account()
    token = OurToken[-1]
    tx = token.balanceOf(account)
    # tx.wait(1)
    print('Balance Of: ', tx)

def transfer():
    account = get_account()
    account2 = get_account(index=1)
    token = OurToken[-1]
    start_balance_account = token.balanceOf(account)
    start_balance_account2 = token.balanceOf(account2)
    tx = token.transfer(account2, start_balance_account, {'from': account})
    tx.wait(1)
    end_balance_account = token.balanceOf(account)
    end_balance_account2 = token.balanceOf(account2)
    print('Transfer from status: ', start_balance_account != end_balance_account)
    print('Transfer to status: ', start_balance_account2 != end_balance_account2)
    print('Sender balance == 0: ', end_balance_account == 0)
    print('Receiver balance == start balance 1 + start balance 2: ', end_balance_account2 == (start_balance_account + start_balance_account2))

def allowance():
    account = get_account()
    account2 = get_account(index=1)
    token = OurToken[-1]
    tx = token.allowance(account, account2)
    print('Allowance status: ', tx)

def approve():
    account = get_account()
    account2 = get_account(index=1)
    token = OurToken[-1]
    tx = token.approve(account2, 1)
    print('Approve status: ', tx)

def transferFrom():
    account = get_account()
    account2 = get_account(index=1)
    token = OurToken[-1]
    start_balance_account = token.balanceOf(account)
    start_balance_account2 = token.balanceOf(account2)
    approve = token.approve(account2, start_balance_account, {'from':account})
    tx = token.transferFrom(account, account2, start_balance_account, {'from': account2})
    end_balance_account = token.balanceOf(account)
    end_balance_account2 = token.balanceOf(account2)
    print('START BALANCE ACCOUNT: ', start_balance_account)
    print('END BALANCE ACCOUNT: ', end_balance_account)
    print('TRANSFERFROM status: ', tx)
    print('Transfer from status: ', start_balance_account != end_balance_account)
    print('Transfer to status: ', start_balance_account2 != end_balance_account2)
    print('Sender balance == 0: ', end_balance_account == 0)
    print('Receiver balance == start balance 1 + start balance 2: ', end_balance_account2 == (start_balance_account + start_balance_account2))


def main():
    deploy_token()
    totalSupply()
    balanceOf()
    transfer()
    allowance()
    approve()
    transferFrom()
    