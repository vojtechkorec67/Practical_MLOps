import pytest
from hello import add


def test_add_positive_numbers():
    """Test add function with positive numbers"""
    assert add(1, 1) == 2


def test_add_negative_numbers():
    """Test add function with negative numbers"""
    assert add(-1, -1) == -2


def test_add_mixed_numbers():
    """Test add function with mixed positive and negative numbers"""
    assert add(5, -3) == 2


def test_add_zero():
    """Test add function with zero"""
    assert add(0, 5) == 5
    assert add(5, 0) == 5
    assert add(0, 0) == 0


def test_add_floats():
    """Test add function with float numbers"""
    assert add(1.5, 2.5) == 4.0
