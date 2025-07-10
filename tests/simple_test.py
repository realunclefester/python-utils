#!/usr/bin/env python3
"""Simple tests for python-utils without pytest dependency"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_validators():
    """Test validators module"""
    from utils.validation.validators import validate_email, validate_url, ValidationError
    
    # Test valid cases
    assert validate_email("test@example.com") == True
    assert validate_url("https://example.com") == True
    
    # Test invalid cases
    try:
        validate_email("invalid-email")
        assert False, "Should have raised ValidationError"
    except ValidationError:
        pass  # Expected
    
    print("✅ Validators tests passed")

def test_json_converter():
    """Test JSON converter module"""
    from utils.conversion.json_converter import to_json, from_json
    import datetime
    
    # Test with datetime
    data = {"name": "test", "date": datetime.datetime.now()}
    json_str = to_json(data)
    assert isinstance(json_str, str)
    assert "test" in json_str
    
    # Test parsing
    simple_data = {"key": "value"}
    json_str = to_json(simple_data)
    parsed = from_json(json_str)
    assert parsed["key"] == "value"
    
    print("✅ JSON converter tests passed")

def test_imports():
    """Test that all imports work correctly"""
    from utils import validate_email, to_json, ValidationError
    
    # Test that imports work
    assert callable(validate_email)
    assert callable(to_json)
    assert issubclass(ValidationError, Exception)
    
    print("✅ Import tests passed")

if __name__ == "__main__":
    try:
        test_validators()
        test_json_converter()
        test_imports()
        print("\n🎉 All tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)