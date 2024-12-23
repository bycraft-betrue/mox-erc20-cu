# pragma version 0.4.0
"""
@license MIT
@title snek_token
@author ByCraft
@notice An ERC20 token with snek
"""
from ethereum.ercs import IERC20

implements: IERC20
# even if we are not implementing all these functions,
# contract will still compile because snekmate implements them all and we are importing it

# ------------------------------------------------------------------
#                             IMPORTS
# ------------------------------------------------------------------

from pcaversaccio.snekmate.src.snekmate.auth import ownable
from pcaversaccio.snekmate.src.snekmate.tokens import erc20

initializes: ownable
initializes: erc20[ownable := ownable]

exports: erc20.__interface__

# ------------------------------------------------------------------
#                         STATE VARIABLES
# ------------------------------------------------------------------

NAME: constant(String[25]) = "snek_token"
SYMBOL: constant(String[5]) = "SNEK"
DECIMALS: constant(uint8) = 18
EIP712_NAME: constant(String[50]) = "snek_token"
EIP712_VERSION: constant(String[20]) = "1"


# ------------------------------------------------------------------
#                            FUNCTIONS
# ------------------------------------------------------------------


# 0 tokens when first deployed without minting
@deploy
def __init__(initial_supply: uint256):
    ownable.__init__()
    erc20.__init__(NAME, SYMBOL, DECIMALS, EIP712_NAME, EIP712_VERSION)
    erc20._mint(msg.sender, initial_supply)


# This is a bug! Remove it (but our stateful tests should catch it!)
@external
def super_mint():
    # We forget to update the total supply!
    # self.totalSupply += amount
    amount: uint256 = as_wei_value(100, "ether")
    erc20.balanceOf[msg.sender] = erc20.balanceOf[msg.sender] + amount
    log IERC20.Transfer(empty(address), msg.sender, amount)
    
# if you do it yourself you need to implement a lot of functions
# instead we'll use libraries
# def name() -> String[100]:
#     return "Snek Token"

# def symbol() -> String[10]:
#     return "SNEK"
#
# ...


