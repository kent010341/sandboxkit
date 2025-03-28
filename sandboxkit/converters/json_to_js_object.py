import json
import re
from typing import Union

def json_to_js_object(obj: Union[str, dict, list], indent: int = 4) -> str:
    """
    Convert a JSON object (as string or Python dict/list) into a JavaScript object literal.
    This is useful for converting backend data into front-end-friendly JS code.

    :param obj: A JSON string, or a Python dict/list already parsed from JSON.
    :param indent: Indentation level for the resulting JS object.
    :return: A JavaScript object literal string, with unquoted keys where allowed.
    :raises ValueError: If the input is not a JSON string, dict, or list.
    :raises json.JSONDecodeError: If the input is a malformed JSON string.
    :raises ValueError: If any key is illegal in JavaScript (e.g., starts with a number, contains special characters).
    """
    # Parse JSON input if it's a string
    if isinstance(obj, str):
        parsed = json.loads(obj)  # Let original JSONDecodeError propagate if parsing fails
        json_str = json.dumps(parsed, indent=indent)
    elif isinstance(obj, (dict, list)):
        json_str = json.dumps(obj, indent=indent)
    else:
        raise ValueError("Input must be a JSON string, dict, or list")

    # Validate all object keys before removing quotes
    parsed_obj = json.loads(json_str)
    if isinstance(parsed_obj, dict):
        for key in parsed_obj.keys():
            __validate_key(key)
    elif isinstance(parsed_obj, list):
        for item in parsed_obj:
            if isinstance(item, dict):
                for key in item.keys():
                    __validate_key(key)

    # Replace quoted keys like "foo": → foo:
    js_object_str = re.sub(r'"([a-zA-Z_]\w*)"\s*:', r'\1:', json_str)

    return js_object_str


def __validate_key(key: str):
    """
    Ensure the key is a valid JavaScript identifier.
    Raises ValueError if the key is invalid.
    """
    if not re.match(r'^[a-zA-Z_]\w*$', key):
        raise ValueError(f"Invalid JavaScript object key: '{key}'")
