import boa
import pytest

from script.deploy import INITIAL_SUPPLY, deploy

RANDOM_USER = boa.env.generate_address("random_user")


def test_token_supply():
    snek_token = deploy()
    assert snek_token.totalSupply() == INITIAL_SUPPLY


def test_transfer_fails_on_insufficient_balance():
    """Test transfer reverts when sender has insufficient balance"""
    snek_token = deploy()
    with boa.env.prank(RANDOM_USER), pytest.raises(Exception):
        snek_token.transfer(snek_token.owner(), INITIAL_SUPPLY)


def test_total_supply_remains_constant():
    """Test total supply doesn't change after transfers"""
    snek_token = deploy()
    initial_supply = snek_token.totalSupply()

    with boa.env.prank(snek_token.owner()):
        snek_token.transfer(RANDOM_USER, INITIAL_SUPPLY // 2)
        assert snek_token.totalSupply() == initial_supply


def test_token_emits_event():
    snek_token = deploy()
    with boa.env.prank(snek_token.owner()):
        snek_token.transfer(RANDOM_USER, INITIAL_SUPPLY)
        logs = snek_token.get_logs()
        log_owner = logs[0].topics[0]
        assert log_owner == snek_token.owner()
