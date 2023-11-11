"""
# lucid Config Schema Helpers

* Description:

    A helper library to make traversing the tools_directory json easier.

* Update History:

    `2023-09-28` - Init

    `2023-11-11` - added get_tool_schema_value(), made config import a module constant
    (may convert to get function in the future).
"""


from pathlib import Path

import lucid.io_utils
import lucid.constants


CONFIG = lucid.io_utils.import_data_from_json(Path(lucid.constants.CONFIG_PATH, 'tools_directory.json'))


def get_tool_schema_value(tool_name: str, key: str) -> str:
    tool_schema = CONFIG[tool_name]
    return tool_schema[key]


def get_token_structure(tool_name: str) -> dict:
    """
    Gets the token structure dict from the tools_directory json.

    Args:
        tool_name(str): The name of the tool to look up in the tools_directory json.
        If a path is provided, the stem will be used as long as it matches
        a key in the tools_directory.

    Returns:
        dict: The token_structure dict for the tool, as outlined in the
        tools_directory json.
    """
    key = Path(tool_name).stem

    tools_dict = CONFIG[key]

    return tools_dict['token_structure']


def get_token_value(token: str, tool_name: str):
    """
    A shorthand way to look up a token_structure key's value
    in the tools_directory json.

    Args:
        token(str): The token name to get the fixed directory value for.

        tool_name(str): The name of the tool to look up in the tools_directory
        json.
    """
    token_structure = get_token_structure(tool_name)
    return token_structure[token]


def get_variable_tokens_keys(token_structure: dict) -> list[str]:
    """
    Gets the tokens for variable, or selectable, directories.

    Args:
        token_structure(dict): The dictionary token structure
        from the tools_directory json.

    Returns:
        list[str]: A list of the variable directory keys. These
        are the dict keys that are outlined in the
        tools_directory json.
    """
    tokens = []
    for k, v in token_structure.items():
        if not v:
            tokens.append(k)

    return tokens


def get_fixed_token_values(token_structure: dict) -> list[str]:
    """
    Gets the tokens for fixed, or non-selectable, directories.

    Args:
        token_structure(dict): The dictionary token structure
        from the tools_directory json.

    Returns:
        list[str]: A list of the fixed directory values. These
        are the dict values that are predefined in the
        tools_directory json.
    """
    tokens = []
    for _, v in token_structure.items():
        if v:
            tokens.append(v)

    return tokens


def create_path_from_tokens(tokens: list[str], tool_name: str) -> Path:
    """
    Creates a path from the tools_directory config, up to the next variable token slot
    after the ones provided, or the whole path if there are no remaining variable
    token slots.

    This helper function will only work assuming there are string values for the keys.
    If you have built a more complex variable system within the token_structure values
    then you may need to build your own version of this algorithm.

    Args:
        tokens(list[str]): The tokens used so far for path construction.

        tool_name(str): The name of the tool to look up in the tools_directory json.

    Returns:
        Path: A path object for the current path made from the given tokens and the
        fixed tokens within the tool's config entry in tools_directory json.
        The base for the path will be lucid.constants.SHOWS_PATH. All fixed or
        dynamic tokens will be appended from there.
    """
    token_structure = get_token_structure(tool_name)
    current_path = Path(lucid.constants.PROJECTS_PATH)
    values = []
    dyn_array_idx = 0  # Dynamic directories
    fixed_array_idx = 0  # Fixed directories
    for _, v in token_structure.items():
        if v:
            values.append(v)
        else:
            values.append('')

    for i in values:
        if not i:
            if dyn_array_idx == len(tokens):
                break
            current_path = Path(current_path, tokens[dyn_array_idx])
            dyn_array_idx += 1
        else:
            current_key = list(token_structure.keys())[dyn_array_idx + fixed_array_idx]
            current_value = token_structure[current_key]
            current_path = Path(current_path, current_value)
            fixed_array_idx += 1

    return current_path
