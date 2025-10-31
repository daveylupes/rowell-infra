"""
Basic tests to verify the testing framework is working
"""

import pytest


def test_basic_math():
    """Test basic math operations"""
    assert 2 + 2 == 4
    assert 3 * 3 == 9
    assert 10 - 5 == 5


def test_string_operations():
    """Test string operations"""
    assert "hello" + " " + "world" == "hello world"
    assert len("test") == 4
    assert "test".upper() == "TEST"


@pytest.mark.asyncio
async def test_async_function():
    """Test async function"""
    async def async_add(a, b):
        return a + b
    
    result = await async_add(2, 3)
    assert result == 5


class TestBasicClass:
    """Test class with multiple test methods"""
    
    def test_instance_method(self):
        """Test instance method"""
        assert True
    
    def test_another_method(self):
        """Test another method"""
        assert 1 + 1 == 2


@pytest.mark.unit
def test_unit_marker():
    """Test with unit marker"""
    assert True


@pytest.mark.integration
def test_integration_marker():
    """Test with integration marker"""
    assert True


@pytest.mark.slow
def test_slow_marker():
    """Test with slow marker"""
    assert True
