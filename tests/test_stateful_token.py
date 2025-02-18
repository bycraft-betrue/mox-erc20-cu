from hypothesis.stateful import RuleBasedStateMachine, rule, invariant
from boa.test.strategies import strategy
from hypothesis import settings
from eth_utils import to_wei
from script.deploy import INITIAL_SUPPLY, deploy  # Add this import


class StatefulFuzzer(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.contract = deploy()
        self.total_minted = INITIAL_SUPPLY
        self.mint_amount = to_wei(100, "ether")  # Amount from super_mint()

    @rule()
    def mint_tokens(self):
        """Call super_mint and track minted amount"""
        initial_balance = self.contract.balanceOf(self.contract.owner())
        self.contract.super_mint()
        new_balance = self.contract.balanceOf(self.contract.owner())

        # Track total minted amount
        self.total_minted += self.mint_amount

    @invariant()
    def check_total_supply(self):
        """Total supply should equal sum of all minted amounts"""
        total_supply = self.contract.totalSupply()
        assert total_supply == self.total_minted, (
            f"Total supply {total_supply} does not match "
            f"expected minted amount {self.total_minted}"
        )

    @invariant()
    def check_balances_match_supply(self):
        """Sum of all balances should equal total supply"""
        owner_balance = self.contract.balanceOf(self.contract.owner())
        assert owner_balance == self.total_minted, (
            f"Owner balance {owner_balance} does not match "
            f"total minted {self.total_minted}"
        )


TestStatefulFuzzer = StatefulFuzzer.TestCase

TestStatefulFuzzer.settings = settings(max_examples=100, stateful_step_count=10)
