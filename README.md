# Python Utils

A collection of useful Python utilities for validation, conversion, and common operations.

## Features

- **Zero dependencies** - Uses only Python standard library
- **Comprehensive validation** - Email, URL, IP, UUID, JSON, and more
- **Extended JSON support** - Handles datetime, UUID, Decimal, and custom objects
- **Type-safe** - Full type hints and proper error handling
- **Well-tested** - Reliable utilities for production use

## Installation

```bash
pip install python-utils
```

## Quick Start

### Validators

```python
from utils.validators import (
    validate_email, validate_url, validate_ip, 
    validate_uuid, validate_json, ValidationError
)

# Email validation
try:
    validate_email("user@example.com")
    print("Valid email!")
except ValidationError as e:
    print(f"Invalid: {e}")

# URL validation
validate_url("https://example.com")
validate_url("https://example.com", require_https=True)

# IP address validation
validate_ip("192.168.1.1")  # IPv4
validate_ip("::1")  # IPv6
validate_ip("::1", allow_ipv4=False)  # IPv6 only

# UUID validation
validate_uuid("550e8400-e29b-41d4-a716-446655440000")
validate_uuid("550e8400-e29b-41d4-a716-446655440000", version=4)

# JSON validation
validate_json('{"key": "value"}')
```

### JSON Converter

```python
from utils.json_converter import to_json, from_json, json_to_file, json_from_file
import datetime
import uuid

# Convert complex objects to JSON
data = {
    "name": "John",
    "created": datetime.datetime.now(),
    "id": uuid.uuid4(),
    "tags": {"python", "utils"}
}

json_str = to_json(data, pretty=True)
print(json_str)

# Convert back from JSON
parsed = from_json(json_str)

# Save to file
json_to_file(data, "data.json")

# Load from file
loaded = json_from_file("data.json")
```

### More Validators

```python
from utils.validators import (
    validate_type, validate_range, validate_length,
    validate_pattern, validate_not_empty, validate_in_options
)

# Type validation
validate_type("hello", str)
validate_type(123, (int, float))

# Range validation
validate_range(5, min_value=1, max_value=10)

# Length validation
validate_length("hello", min_length=3, max_length=10)
validate_length([1, 2, 3], min_length=2)

# Pattern validation
validate_pattern("ABC123", r"^[A-Z]+[0-9]+$")

# Not empty validation
validate_not_empty("hello")
validate_not_empty([1, 2, 3])

# Options validation
validate_in_options("red", ["red", "green", "blue"])
```

## API Reference

### Validators

All validators return `True` on success or raise `ValidationError` on failure.

#### Basic Validators
- `validate_type(value, expected_type, field=None)` - Type validation
- `validate_range(value, min_value=None, max_value=None, field=None)` - Numeric range
- `validate_length(value, min_length=None, max_length=None, field=None)` - Length validation
- `validate_pattern(value, pattern, field=None)` - Regex pattern matching
- `validate_not_empty(value, field=None)` - Non-empty validation
- `validate_in_options(value, options, field=None)` - Options validation

#### Specialized Validators
- `validate_email(value, field=None)` - Email address validation
- `validate_url(value, require_https=False, field=None)` - URL validation
- `validate_ip(value, allow_ipv4=True, allow_ipv6=True, field=None)` - IP address validation
- `validate_uuid(value, version=None, field=None)` - UUID validation
- `validate_json(value, field=None)` - JSON validation

### JSON Converter

#### Basic Operations
- `to_json(data, pretty=False, ensure_ascii=True, sort_keys=False)` - Convert to JSON
- `from_json(json_str, target_type=None, strict=False)` - Parse from JSON

#### File Operations
- `json_to_file(data, filepath, pretty=True)` - Write JSON to file
- `json_from_file(filepath, target_type=None, strict=False)` - Read JSON from file

#### Advanced Operations
- `merge_json(base, update, deep=True)` - Merge JSON objects

### Error Handling

```python
from utils.validators import ValidationError

try:
    validate_email("invalid-email")
except ValidationError as e:
    print(f"Error: {e.message}")
    print(f"Field: {e.field}")
    print(f"Details: {e.details}")
```

## Extended JSON Support

The JSON converter automatically handles:

- `datetime.datetime`, `datetime.date`, `datetime.time` → ISO format strings
- `datetime.timedelta` → String representation
- `uuid.UUID` → String representation
- `decimal.Decimal` → Float
- `set` → List
- Objects with `to_json()` method
- Objects with `__dict__` attribute

## Requirements

- Python 3.6+
- No external dependencies

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.