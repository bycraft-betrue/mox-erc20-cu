from boa.test.strategies import strategy
from hypothesis import given, HealthCheck, settings
from contracts.sub_lesson import stateless_fuzz_solvable


@settings(
    max_examples=1000, suppress_health_check=[HealthCheck.function_scoped_fixture]
)
@given(input=strategy("uint256"))  # 0, MaxUINT256
def test_always_returns_input_number(input):
    contract = stateless_fuzz_solvable.deploy()
    assert contract.always_returns_input_number(input) == input


# hypothesis doesn't like fixtures, but you can make the compiler ignore it with HealthCheck

# import pytest

# @pytest.fixture(scope="function")
# def contract():
#     return stateless_fuzz_solvable.deploy()

# # unit test example
# def test_always_returns_input(contract):
#     input = 0
#     assert contract.always_returns_input_number(input) == input
