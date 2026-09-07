import collections
from typing import Dict, Any, Union, List

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    """
    Recursively flattens a nested dictionary structure into a single level.
    Useful for processing nested API payloads or configuration files.
    """
    items: List[tuple] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                list_key = f"{new_key}{sep}{i}"
                if isinstance(item, dict):
                    items.extend(flatten_dict(item, list_key, sep=sep).items())
                else:
                    items.append((list_key, item))
        else:
            items.append((new_key, v))
    return dict(items)

def clean_empty_values(data: Union[Dict[str, Any], List[Any]]) -> Union[Dict[str, Any], List[Any], None]:
    """
    Recursively strips out None, empty strings, empty dicts, and empty lists
    to clean up raw data payloads before sending or saving.
    """
    if isinstance(data, dict):
        cleaned_dict = {}
        for k, v in data.items():
            if v is not None and v != "" and v != {} and v != []:
                cleaned_val = clean_empty_values(v)
                if cleaned_val is not None and cleaned_val != {} and cleaned_val != []:
                    cleaned_dict[k] = cleaned_val
        return cleaned_dict
    elif isinstance(data, list):
        cleaned_list = []
        for item in data:
            if item is not None and item != "" and item != {} and item != []:
                cleaned_val = clean_empty_values(item)
                if cleaned_val is not None and cleaned_val != {} and cleaned_val != []:
                    cleaned_list.append(cleaned_val)
        return cleaned_list
    return data