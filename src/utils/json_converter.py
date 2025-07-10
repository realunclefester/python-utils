"""
JSON conversion utilities with extended type support.

Handles conversion of datetime, UUID, Decimal, and custom objects to/from JSON.
"""

import json
import datetime
import uuid
import decimal
from typing import Any, Dict, List, Optional, Union, Type, TypeVar, Set, Callable


T = TypeVar('T')


class ExtendedJSONEncoder(json.JSONEncoder):
    """JSON encoder that handles additional types like datetime, UUID, Decimal, etc."""
    
    def default(self, obj):
        """Convert non-standard types to JSON-serializable types."""
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return str(obj)
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj, set):
            return list(obj)
        elif hasattr(obj, 'to_json'):
            return obj.to_json()
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        return super().default(obj)


def to_json(
    data: Any, 
    pretty: bool = False, 
    ensure_ascii: bool = True,
    sort_keys: bool = False,
    custom_encoder: Optional[Type[json.JSONEncoder]] = None
) -> str:
    """
    Convert any Python object to JSON string.
    
    Args:
        data: Data to convert (dict, list, object, etc.)
        pretty: Whether to format the JSON for readability
        ensure_ascii: Whether to escape non-ASCII characters
        sort_keys: Whether to sort dictionary keys
        custom_encoder: Custom JSON encoder class
        
    Returns:
        JSON string
        
    Example:
        >>> to_json({"name": "John", "age": 30}, pretty=True)
        {
          "name": "John",
          "age": 30
        }
        
        >>> to_json(datetime.datetime.now())
        "2025-01-01T12:00:00.000000"
    """
    indent = 2 if pretty else None
    encoder_class = custom_encoder or ExtendedJSONEncoder
    
    return json.dumps(
        data,
        indent=indent,
        ensure_ascii=ensure_ascii,
        sort_keys=sort_keys,
        cls=encoder_class
    )


def from_json(
    json_str: str,
    target_type: Optional[Type[T]] = None,
    strict: bool = False
) -> Union[T, Dict, List]:
    """
    Convert JSON string to Python object.
    
    Args:
        json_str: JSON string to parse
        target_type: Optional type to convert to
        strict: Whether to raise exception on error
        
    Returns:
        Parsed object (dict/list by default, or instance of target_type)
        
    Raises:
        ValueError: If JSON is invalid and strict=True
        
    Example:
        >>> from_json('{"name": "John", "age": 30}')
        {'name': 'John', 'age': 30}
        
        >>> class Person:
        ...     def __init__(self, name, age):
        ...         self.name = name
        ...         self.age = age
        >>> from_json('{"name": "John", "age": 30}', Person)
        <Person object>
    """
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        if strict:
            raise ValueError(f"Invalid JSON: {str(e)}") from e
        return {} if target_type in (dict, None) else []
    
    # If no target type specified, return parsed data as-is
    if target_type is None:
        return data
        
    # If target is dict or list, return as-is
    if target_type in (dict, list):
        return data
        
    # Try to convert to target type
    try:
        # Check for custom deserialization methods
        if hasattr(target_type, 'from_json'):
            return target_type.from_json(json_str)
        elif hasattr(target_type, 'from_dict') and isinstance(data, dict):
            return target_type.from_dict(data)
            
        # Try to create instance with data as kwargs (for dict data)
        if isinstance(data, dict):
            return target_type(**data)
        else:
            return target_type(data)
    except Exception as e:
        if strict:
            raise ValueError(f"Failed to convert JSON to {target_type.__name__}: {str(e)}") from e
        # Return empty instance on error
        try:
            return target_type()
        except:
            return None


def json_to_file(
    data: Any,
    filepath: str,
    pretty: bool = True,
    ensure_ascii: bool = True,
    sort_keys: bool = False
) -> None:
    """
    Write data to JSON file.
    
    Args:
        data: Data to write
        filepath: Path to output file
        pretty: Whether to format the JSON
        ensure_ascii: Whether to escape non-ASCII characters
        sort_keys: Whether to sort dictionary keys
        
    Example:
        >>> json_to_file({"name": "John"}, "person.json")
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(
            data,
            f,
            indent=2 if pretty else None,
            ensure_ascii=ensure_ascii,
            sort_keys=sort_keys,
            cls=ExtendedJSONEncoder
        )


def json_from_file(
    filepath: str,
    target_type: Optional[Type[T]] = None,
    strict: bool = False
) -> Union[T, Dict, List]:
    """
    Read JSON from file.
    
    Args:
        filepath: Path to JSON file
        target_type: Optional type to convert to
        strict: Whether to raise exception on error
        
    Returns:
        Parsed object
        
    Example:
        >>> json_from_file("person.json")
        {'name': 'John', 'age': 30}
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return from_json(content, target_type, strict)
    except Exception as e:
        if strict:
            raise
        return {} if target_type in (dict, None) else []


def merge_json(
    base: Union[str, Dict],
    update: Union[str, Dict],
    deep: bool = True
) -> Dict:
    """
    Merge two JSON objects.
    
    Args:
        base: Base JSON string or dict
        update: Update JSON string or dict
        deep: Whether to do deep merge
        
    Returns:
        Merged dictionary
        
    Example:
        >>> merge_json({"a": 1}, {"b": 2})
        {'a': 1, 'b': 2}
        
        >>> merge_json({"a": {"x": 1}}, {"a": {"y": 2}}, deep=True)
        {'a': {'x': 1, 'y': 2}}
    """
    # Convert to dicts if needed
    base_dict = from_json(base) if isinstance(base, str) else base.copy()
    update_dict = from_json(update) if isinstance(update, str) else update
    
    if not deep:
        base_dict.update(update_dict)
        return base_dict
    
    # Deep merge
    def deep_merge(d1, d2):
        for key, value in d2.items():
            if key in d1 and isinstance(d1[key], dict) and isinstance(value, dict):
                deep_merge(d1[key], value)
            else:
                d1[key] = value
        return d1
    
    return deep_merge(base_dict, update_dict)