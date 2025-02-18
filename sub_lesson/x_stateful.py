from hypothesis.stateful import RuleBasedStateMachine, rule, invariant
from contracts.sub_lesson import stateful_fuzz_solvable
from boa.test.strategies import strategy
from hypothesis import settings


class StatefulFuzzer(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.contract = stateful_fuzz_solvable.deploy()

    # "Rule" -> Actions, and can have properties / invariants
    # "Invariant" -> Properties that should always hold true
    @rule(new_number=strategy("uint256"))
    def change_number(self, new_number):
        self.contract.change_number(new_number)
        # can add a rule here: assert ...

    @rule(input_number=strategy("uint256"))
    def input_number_returns_itself(self, input_number):
        response = self.contract.always_returns_input_number(input_number)
        assert response == input_number, f"Expected {input_number}, got {response}"


TestStatefulFuzzer = StatefulFuzzer.TestCase

TestStatefulFuzzer.settings = settings(max_examples=10000, stateful_step_count=50)
