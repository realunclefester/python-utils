#!/usr/bin/env python3
"""Tests for validators module"""

import sys
import os
import pytest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.validators import (
    validate_email, validate_url, validate_ip, validate_uuid,
    validate_json, validate_type, validate_range, validate_length,
    validate_pattern, validate_not_empty, validate_in_options,
    ValidationError
)


def test_validate_email():
    """Test email validation"""
    # Valid emails
    assert validate_email("test@example.com") is True
    assert validate_email("user.name@domain.co.uk") is True
    assert validate_email("test123@test-domain.com") is True
    
    # Invalid emails
    with pytest.raises(ValidationError):
        validate_email("invalid-email")
    with pytest.raises(ValidationError):
        validate_email("@example.com")
    with pytest.raises(ValidationError):
        validate_email("test@")
    with pytest.raises(ValidationError):
        validate_email(123)


def test_validate_url():
    """Test URL validation"""
    # Valid URLs
    assert validate_url("https://example.com") is True
    assert validate_url("http://test.domain.com/path") is True
    assert validate_url("https://example.com/path?query=1") is True
    
    # Invalid URLs
    with pytest.raises(ValidationError):
        validate_url("not-a-url")
    with pytest.raises(ValidationError):
        validate_url("ftp://example.com")
    
    # HTTPS requirement
    assert validate_url("https://example.com", require_https=True) is True
    with pytest.raises(ValidationError):
        validate_url("http://example.com", require_https=True)


def test_validate_ip():
    """Test IP address validation"""
    # Valid IPv4
    assert validate_ip("192.168.1.1") is True
    assert validate_ip("127.0.0.1") is True
    assert validate_ip("10.0.0.1") is True
    
    # Valid IPv6
    assert validate_ip("::1") is True
    assert validate_ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334") is True
    
    # Invalid IPs
    with pytest.raises(ValidationError):
        validate_ip("invalid-ip")
    with pytest.raises(ValidationError):
        validate_ip("999.999.999.999")
    
    # Type restrictions
    with pytest.raises(ValidationError):
        validate_ip("192.168.1.1", allow_ipv4=False)
    with pytest.raises(ValidationError):
        validate_ip("::1", allow_ipv6=False)


def test_validate_uuid():
    """Test UUID validation"""
    # Valid UUIDs
    assert validate_uuid("550e8400-e29b-41d4-a716-446655440000") is True
    assert validate_uuid("6ba7b810-9dad-11d1-80b4-00c04fd430c8") is True
    
    # Invalid UUIDs
    with pytest.raises(ValidationError):
        validate_uuid("not-a-uuid")
    with pytest.raises(ValidationError):
        validate_uuid("550e8400-e29b-41d4-a716")


def test_validate_json():
    """Test JSON validation"""
    # Valid JSON
    assert validate_json('{"key": "value"}') is True
    assert validate_json('[]') is True
    assert validate_json('null') is True
    
    # Invalid JSON
    with pytest.raises(ValidationError):
        validate_json('{"key": value}')  # Missing quotes
    with pytest.raises(ValidationError):
        validate_json('{key: "value"}')  # Missing quotes


def test_validate_type():
    """Test type validation"""
    # Valid types
    assert validate_type("hello", str) is True
    assert validate_type(123, int) is True
    assert validate_type(123, (int, float)) is True
    
    # Invalid types
    with pytest.raises(ValidationError):
        validate_type("hello", int)
    with pytest.raises(ValidationError):
        validate_type(123, str)


def test_validate_range():
    """Test range validation"""
    # Valid ranges
    assert validate_range(5, min_value=1, max_value=10) is True
    assert validate_range(5.5, min_value=1.0, max_value=10.0) is True
    
    # Invalid ranges
    with pytest.raises(ValidationError):
        validate_range(0, min_value=1, max_value=10)
    with pytest.raises(ValidationError):
        validate_range(11, min_value=1, max_value=10)


def test_validate_length():
    """Test length validation"""
    # Valid lengths
    assert validate_length("hello", min_length=3, max_length=10) is True
    assert validate_length([1, 2, 3], min_length=2, max_length=5) is True
    
    # Invalid lengths
    with pytest.raises(ValidationError):
        validate_length("hi", min_length=3)
    with pytest.raises(ValidationError):
        validate_length("very long string", max_length=5)


def test_validate_pattern():
    """Test pattern validation"""
    # Valid patterns
    assert validate_pattern("ABC123", r"^[A-Z]+[0-9]+$") is True
    assert validate_pattern("test@example.com", r".*@.*\.com$") is True
    
    # Invalid patterns
    with pytest.raises(ValidationError):
        validate_pattern("123ABC", r"^[A-Z]+[0-9]+$")


def test_validate_not_empty():
    """Test not empty validation"""
    # Valid non-empty values
    assert validate_not_empty("hello") is True
    assert validate_not_empty([1, 2, 3]) is True
    assert validate_not_empty({"key": "value"}) is True
    
    # Invalid empty values
    with pytest.raises(ValidationError):
        validate_not_empty("")
    with pytest.raises(ValidationError):
        validate_not_empty([])
    with pytest.raises(ValidationError):
        validate_not_empty(None)
    with pytest.raises(ValidationError):
        validate_not_empty("   ")  # Whitespace only


def test_validate_in_options():
    """Test options validation"""
    # Valid options
    assert validate_in_options("red", ["red", "green", "blue"]) is True
    assert validate_in_options(1, [1, 2, 3]) is True
    
    # Invalid options
    with pytest.raises(ValidationError):
        validate_in_options("yellow", ["red", "green", "blue"])
    with pytest.raises(ValidationError):
        validate_in_options(4, [1, 2, 3])


if __name__ == "__main__":
    pytest.main([__file__])