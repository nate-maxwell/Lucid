"""
# Environment Variable Utilities

* Description:

    Some boilerplate elimination for handling environment variables.
    Largely these functions are for plugging in consistently used variables so
    developers do not have to remember them, and apply common formatting
    practices.
"""


import os

from lucid.core import const


def get_clean_var(var: str) -> str:
    return os.getenv(var, const.UNASSIGNED).replace(';', '')


def var_is_unassigned(end_var: str) -> bool:
    return get_clean_var(end_var) == const.UNASSIGNED
