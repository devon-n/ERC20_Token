from brownie import Lottery, accounts, network, config, exceptions
from scripts.deploy_token import deploy_token
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from web3 import Web3
import pytest

initial_supply = Web3.toWei(1000, 'ether')

def start_test():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    token = deploy_token()
    account = get_account()
    account2 = get_account(index=1)
    return token, account, account2

def test_total_supply():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    token = deploy_token(initial_supply)
    # Act
    total_supply = token.totalSupply()
    # Assert
    assert total_supply == initial_supply

def test_balance_of():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    token = deploy_token()
    account = get_account() 
    balance = token.balanceOf(account)
    # Assert
    assert balance > 0
    

def test_transfer():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    token = deploy_token()
    account = get_account()
    account2 = get_account(index=1)
    start_balance_account = token.balanceOf(account)
    start_balance_account2 = token.balanceOf(account2)
    # Act 
    transfer = token.transfer(account2, start_balance_account, {'from':account})
    end_balance_account = token.balanceOf(account)
    end_balance_account2 = token.balanceOf(account2)
    # Assert 
    assert (end_balance_account2 == start_balance_account + start_balance_account2) and (end_balance_account == 0)

def test_approve():
    # Arrange
    token, account, account2 = start_test()
    start_balance_account = token.balanceOf(account)
    # Act
    approve = token.approve(account2, start_balance_account, {'from':account})
    # Assert
    assert approve == True

def test_allowance():
    # Arrange
    token, account, account2 = start_test()
    start_balance_account = token.balanceOf(account)
    allowance_start = token.allowance(account, account2) # Should == 0
    approve = token.approve(account2, start_balance_account, {'from':account})
    # Act
    allowance_end = token.allowance(account, account2)
    # Assert
    assert allowance_end > allowance_start


def test_transfer_from():
    # Arrange
    token, account, account2 = start_test()
    start_balance_account = token.balanceOf(account)
    start_balance_account2 = token.balanceOf(account2)
    approve = token.approve(account2, start_balance_account, {'from':account})
    # Act
    token.transferFrom(account, account2, start_balance_account, {'from':account2})
    # Assert
    assert start_balance_account2 > start_balance_account
