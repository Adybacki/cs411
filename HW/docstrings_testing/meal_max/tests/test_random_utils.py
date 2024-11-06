import pytest
from meal_max.utils.random_utils import RandomUtils

def test_get_random_int():
    """Test fetching a random integer within a range."""
    min_value = 1
    max_value = 10
    rand_int = RandomUtils.get_random_int(min_value, max_value)
    assert min_value <= rand_int <= max_value, "Random integer should be within the specified range"

def test_get_random_int_boundaries():
    """Test fetching a random integer at the boundaries of the range."""
    min_value = 5
    max_value = 5
    rand_int = RandomUtils.get_random_int(min_value, max_value)
    assert rand_int == min_value == max_value, "When min and max are the same, random integer should be that value"

def test_get_random_float():
    """Test fetching a random float within a range."""
    min_value = 0.1
    max_value = 0.5
    rand_float = RandomUtils.get_random_float(min_value, max_value)
    assert min_value <= rand_float <= max_value, "Random float should be within the specified range"

def test_get_random_float_boundaries():
    """Test fetching a random float at the boundaries of the range."""
    min_value = 0.42
    max_value = 0.42
    rand_float = RandomUtils.get_random_float(min_value, max_value)
    assert rand_float == min_value == max_value, "When min and max are the same, random float should be that value"

def test_get_random_choice():
    """Test selecting a random item from a list."""
    options = ["apple", "banana", "cherry"]
    rand_choice = RandomUtils.get_random_choice(options)
    assert rand_choice in options, "Random choice should be one of the options in the list"

def test_get_random_choice_empty_list():
    """Test random choice with an empty list should raise an exception."""
    options = []
    with pytest.raises(ValueError):
        RandomUtils.get_random_choice(options)