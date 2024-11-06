import pytest
from meal_max.models.kitchen_model import (
    create_meal,
    delete_meal,
    get_leaderboard,
    get_meal_by_id,
    get_meal_by_name,
    update_meal_stats,
    Meal
)

@pytest.fixture
def sample_meal():
    """Fixture to provide a sample Meal instance."""
    return Meal(id=1, meal="Spaghetti", cuisine="Italian", price=10.99, difficulty="MED")

@pytest.fixture
def mock_db_connection(mocker):
    """Fixture to mock the database connection and cursor."""
    # Create a mock connection and cursor using pytest-mock
    mock_conn = mocker.MagicMock()
    mock_cursor = mocker.Mock()
    mock_conn.cursor.return_value = mock_cursor

    # Mock the `get_db_connection` function to return our mock connection
    mocker.patch("meal_max.models.kitchen_model.get_db_connection", return_value=mock_conn)

    # Return both mock objects so they can be inspected in tests
    return mock_conn, mock_cursor

def test_create_meal(mock_db_connection):
    """Test creating a new meal in the database."""
    mock_conn, mock_cursor = mock_db_connection
    create_meal("Spaghetti", "Italian", 10.99, "MED")
    
    # Assert that the correct SQL command was executed with expected parameters
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO meals (meal, cuisine, price, difficulty) VALUES (?, ?, ?, ?)",
        ("Spaghetti", "Italian", 10.99, "MED")
    )
    mock_conn.commit.assert_called_once()

# Repeat the rest of your tests with the same `mock_db_connection` fixture
