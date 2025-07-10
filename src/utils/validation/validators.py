"""
Validators for common data types and formats.

A collection of validation functions for strings, numbers, emails, URLs, IPs, and more.
All validators raise ValidationError on failure or return True on success.
"""

import re
import json
import ipaddress
import uuid
from typing import Any, List, Dict, Union, Optional, Pattern, Type, TypeVar, Set, Tuple
from datetime import datetime


T = TypeVar('T')


class ValidationError(Exception):
    """Error raised when validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        """
        Initialize validation error.
        
        Args:
            message: Error message
            field: Field that failed validation
            details: Additional error details
        """
        self.message = message
        self.field = field
        self.details = details or {}
        
        # Format error message
        formatted_message = message
        if field:
            formatted_message = f"Field '{field}': {message}"
            
        super().__init__(formatted_message)


# Type validators
def validate_type(value: Any, expected_type: Union[Type, Tuple[Type, ...]], field: Optional[str] = None) -> bool:
    """
    Validate that a value is of the expected type.
    
    Args:
        value: Value to validate
        expected_type: Expected type or tuple of types
        field: Field name for error message
        
    Returns:
        True if validation passes
        
    Raises:
        ValidationError if validation fails
        
    Example:
        >>> validate_type("hello", str)
        True
        >>> validate_type(123, (int, float))
        True
    """
    if not isinstance(value, expected_type):
        type_names = (
            [t.__name__ for t in expected_type]
            if isinstance(expected_type, tuple)
            else [expected_type.__name__]
        )
        
        raise ValidationError(
            f"Expected {' or '.join(type_names)}, got {type(value).__name__}",
            field=field
        )
        
    return True


# Numeric validators
def validate_range(
    value: Union[int, float], 
    min_value: Optional[Union[int, float]] = None, 
    max_value: Optional[Union[int, float]] = None, 
    field: Optional[str] = None
) -> bool:
    """
    Validate that a numeric value is within a specified range.
    
    Args:
        value: Value to validate
        min_value: Minimum allowed value (inclusive)
        max_value: Maximum allowed value (inclusive)
        field: Field name for error message
        
    Returns:
        True if validation passes
        
    Raises:
        ValidationError if validation fails
        
    Example:
        >>> validate_range(5, min_value=1, max_value=10)
        True
    """
    if not isinstance(value, (int, float)):
        raise ValidationError(f"Expected numeric value, got {type(value).__name__}", field=field)
        
    if min_value is not None and value < min_value:
        raise ValidationError(f"Value must be at least {min_value}", field=field)
        
    if max_value is not None and value > max_value:
        raise ValidationError(f"Value must be at most {max_value}", field=field)
        
    return True


# Length validators
def validate_length(
    value: Union[str, List, Dict, Set], 
    min_length: Optional[int] = None, 
    max_length: Optional[int] = None, 
    field: Optional[str] = None
) -> bool:
    """
    Validate that a value's length is within a specified range.
    
    Args:
        value: Value to validate (must have __len__)
        min_length: Minimum allowed length
        max_length: Maximum allowed length
        field: Field name for error message
        
    Returns:
        True if validation passes
        
    Raises:
        ValidationError if validation fails
        
    Example:
        >>> validate_length("hello", min_length=3, max_length=10)
        True
    """
    if not hasattr(value, "__len__"):
        raise ValidationError(f"Expected a value with length, got {type(value).__name__}", field=field)
        
    length = len(value)
    
    if min_length is not None and length < min_length:
        raise ValidationError(f"Length must be at least {min_length}", field=field)
        
    if max_length is not None and length > max_length:
        raise ValidationError(f"Length must be at most {max_length}", field=field)
        
    return True


# Pattern validators
def validate_pattern(value: str, pattern: Union[str, Pattern], field: Optional[str] = None) -> bool:
    """
    Validate that a string matches a regex pattern.
    
    Args:
        value: String to validate
        pattern: Regex pattern to match
        field: Field name for error message
        
    Returns:
        True if validation passes
        
    Raises:
        ValidationError if validation fails
        
    Example:
        >>> validate_pattern("ABC123", r"^[A-Z]+[0-9]+$")
        True
    """
    if not isinstance(value, str):
        raise ValidationError(f"Expected string, got {type(value).__name__}", field=field)
        
    if isinstance(pattern, str):
        pattern = re.compile(pattern)
        
    if not pattern.match(value):
        raise ValidationError(f"Value does not match pattern", field=field)
        
    return True


# Email validator
def validate_email(value: str, field: Optional[str] = None) -> bool:
    """
    Validate that a string is a valid email address.
    
    Args:
        value: String to validate
        field: Field name for error message
        
    Returns:
        True if validation passes
        
    Raises:
        ValidationError if validation fails
        
    Example:
        >>> validate_email("user@example.com")
        True
    """
    if not isinstance(value, str):
        raise ValidationError(f"Expected string, got {type(value).__name__}", field=field)
        
    # Basic email pattern (not RFC compliant but practical)
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, value):
        raise ValidationError("Invalid email address", field=field)
        
    return True


# URL validator
def validate_url(value: str, require_https: bool = False, field: Optional[str] = None) -> bool:
    """
    Validate that a string is a valid URL.
    
    Args:
        value: String to validate
        require_https: Whether to require HTTPS protocol
        field: Field name for error message
        
    Returns:
        True if validation passes
        
    Raises:
        ValidationError if validation fails
        
    Example:
        >>> validate_url("https://example.com")
        True
    """
    if not isinstance(value, str):
        raise ValidationError(f"Expected string, got {type(value).__name__}", field=field)
        
    # Basic URL pattern
    pattern = r'^https?://[a-zA-Z0-9][-a-zA-Z0-9.]*\.[a-zA-Z]{2,}(/[-a-zA-Z0-9%_.~#+]*)*(\?[-a-zA-Z0-9%_.~+=&;]*)*$'
    
    if not re.match(pattern, value):
        raise ValidationError("Invalid URL", field=field)
        
    if require_https and not value.startswith("https://"):
        raise ValidationError("URL must use HTTPS protocol", field=field)
        
    return True


# IP address validator
def validate_ip(value: str, allow_ipv4: bool = True, allow_ipv6: bool = True, field: Optional[str] = None) -> bool:
    """
    Validate that a string is a valid IP address.
    
    Args:
        value: String to validate
        allow_ipv4: Whether to allow IPv4 addresses
        allow_ipv6: Whether to allow IPv6 addresses
        field: Field name for error message
        
    Returns:
        True if validation passes
        
    Raises:
        ValidationError if validation fails
        
    Example:
        >>> validate_ip("192.168.1.1")
        True
        >>> validate_ip("::1", allow_ipv4=False)
        True
    """
    if not isinstance(value, str):
        raise ValidationError(f"Expected string, got {type(value).__name__}", field=field)
        
    try:
        ip = ipaddress.ip_address(value)
        
        if isinstance(ip, ipaddress.IPv4Address) and not allow_ipv4:
            raise ValidationError("IPv4 addresses are not allowed", field=field)
            
        if isinstance(ip, ipaddress.IPv6Address) and not allow_ipv6:
            raise ValidationError("IPv6 addresses are not allowed", field=field)
            
    except ValueError:
        raise ValidationError("Invalid IP address", field=field)
        
    return True


# JSON validator
def validate_json(value: str, field: Optional[str] = None) -> bool:
    """
    Validate that a string is valid JSON.
    
    Args:
        value: String to validate
        field: Field name for error message
        
    Returns:
        True if validation passes
        
    Raises:
        ValidationError if validation fails
        
    Example:
        >>> validate_json('{"key": "value"}')
        True
    """
    if not isinstance(value, str):
        raise ValidationError(f"Expected string, got {type(value).__name__}", field=field)
        
    try:
        json.loads(value)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON: {str(e)}", field=field)
        
    return True


# UUID validator
def validate_uuid(value: str, version: Optional[int] = None, field: Optional[str] = None) -> bool:
    """
    Validate that a string is a valid UUID.
    
    Args:
        value: String to validate
        version: UUID version to require (1-5)
        field: Field name for error message
        
    Returns:
        True if validation passes
        
    Raises:
        ValidationError if validation fails
        
    Example:
        >>> validate_uuid("550e8400-e29b-41d4-a716-446655440000")
        True
    """
    if not isinstance(value, str):
        raise ValidationError(f"Expected string, got {type(value).__name__}", field=field)
        
    try:
        uuid_obj = uuid.UUID(value)
        
        if version is not None and uuid_obj.version != version:
            raise ValidationError(f"Expected UUID version {version}, got version {uuid_obj.version}", field=field)
            
    except ValueError:
        raise ValidationError("Invalid UUID", field=field)
        
    return True


# Empty value validator
def validate_not_empty(value: Any, field: Optional[str] = None) -> bool:
    """
    Validate that a value is not empty.
    
    Args:
        value: Value to validate
        field: Field name for error message
        
    Returns:
        True if validation passes
        
    Raises:
        ValidationError if validation fails
        
    Example:
        >>> validate_not_empty("hello")
        True
        >>> validate_not_empty([1, 2, 3])
        True
    """
    if value is None:
        raise ValidationError("Value cannot be None", field=field)
        
    if hasattr(value, "__len__") and len(value) == 0:
        raise ValidationError("Value cannot be empty", field=field)
        
    if isinstance(value, str) and value.strip() == "":
        raise ValidationError("Value cannot be empty or whitespace", field=field)
        
    return True


# Options validator
def validate_in_options(value: Any, options: List[Any], field: Optional[str] = None) -> bool:
    """
    Validate that a value is one of the allowed options.
    
    Args:
        value: Value to validate
        options: List of allowed options
        field: Field name for error message
        
    Returns:
        True if validation passes
        
    Raises:
        ValidationError if validation fails
        
    Example:
        >>> validate_in_options("red", ["red", "green", "blue"])
        True
    """
    if value not in options:
        options_str = ", ".join(str(o) for o in options)
        raise ValidationError(f"Value must be one of: {options_str}", field=field)
        
    return True