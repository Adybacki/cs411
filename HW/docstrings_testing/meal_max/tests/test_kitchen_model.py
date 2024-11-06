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
def mock_db_connection(monkeypatch):
    """Fixture to mock the database connection and cursor."""
    # Create a mock connection and cursor
    mock_conn = pytest.Mock()
    mock_cursor = pytest.Mock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.__exit__.return_value = None
    
    # Mock the `get_db_connection` function to return our mock connection
    monkeypatch.setattr("meal_max.models.kitchen_model.get_db_connection", lambda: mock_conn)
    
    # Return both mock objects so they can be inspected in tests
    return mock_conn, mock_cursor

def test_create_meal(mock_db_connection):
    """Test creating a meal in the kitchen."""
    mock_conn, mock_cursor = mock_db_connection

    # Run the function we want to test
    create_meal("Spaghetti", "Italian", 10.99, "MED")

    # Assert that the correct SQL command was executed with expected parameters
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO meals (meal, cuisine, price, difficulty) VALUES (?, ?, ?, ?)",
        ("Spaghetti", "Italian", 10.99, "MED")
    )
    # Assert that the changes were committed
    mock_conn.commit.assert_called_once()

def test_delete_meal(mock_db_connection):
    """Test deleting a meal by setting its deleted flag to True."""
    mock_conn, mock_cursor = mock_db_connection

    # Simulate an existing meal that hasn't been deleted
    mock_cursor.fetchone.return_value = (0,)
    
    # Run the function we want to test
    delete_meal(1)

    # Assert that we checked the 'deleted' status and then updated it
    mock_cursor.execute.assert_any_call("SELECT deleted FROM meals WHERE id = ?", (1,))
    mock_cursor.execute.assert_any_call("UPDATE meals SET deleted = TRUE WHERE id = ?", (1,))
    # Assert that the changes were committed
    mock_conn.commit.assert_called_once()

def test_get_leaderboard(mock_db_connection):
    """Test retrieving the leaderboard with sorting by wins."""
    mock_conn, mock_cursor = mock_db_connection

    # Set up mock data for the leaderboard
    mock_cursor.fetchall.return_value = [
        (1, "Spaghetti", "Italian", 10.99, "MED", 5, 3, 0.6)
    ]
    
    # Run the function we want to test
    leaderboard = get_leaderboard("wins")
    
    # Assert the leaderboard data matches expected structure
    assert len(leaderboard) == 1
    assert leaderboard[0]["meal"] == "Spaghetti"
    assert leaderboard[0]["wins"] == 3
    assert leaderboard[0]["win_pct"] == 60.0 # Converted to percentage

def test_get_meal_by_id(mock_db_connection, sample_meal):
    """Test retrieving a meal by its ID."""
    mock_conn, mock_cursor = mock_db_connection

    # Set up mock data for a meal
    mock_cursor.fetchone.return_value = (1, "Spaghetti", "Italian", 10.99, "MED", False)

    # Run the function we want to test
    meal = get_meal_by_id(1)
    
    # Assert the meal's properties match the expected values
    assert meal.id == sample_meal.id
    assert meal.meal == sample_meal.meal
    assert meal.cuisine == sample_meal.cuisine
    assert meal.price == sample_meal.price
    assert meal.difficulty == sample_meal.difficulty

def test_get_meal_by_name(mock_db_connection, sample_meal):
    """Test retrieving a meal by its name."""
    mock_conn, mock_cursor = mock_db_connection

    # Set up mock data for a meal
    mock_cursor.fetchone.return_value = (1, "Spaghetti", "Italian", 10.99, "MED", False)

    # Run the function we want to test
    meal = get_meal_by_name("Spaghetti")
    
    # Assert the meal's properties match the expected values
    assert meal.id == sample_meal.id
    assert meal.meal == sample_meal.meal
    assert meal.cuisine == sample_meal.cuisine
    assert meal.price == sample_meal.price
    assert meal.difficulty == sample_meal.difficulty

def test_update_meal_stats_win(mock_db_connection):
    """Test updating meal stats with a win."""
    mock_conn, mock_cursor = mock_db_connection

    # Simulate an existing meal that hasn't been deleted
    mock_cursor.fetchone.return_value = (0,)
    
    # Run the function we want to test
    update_meal_stats(1, "win")
    
    # Assert the correct SQL command was executed to update battles and wins
    mock_cursor.execute.assert_any_call("UPDATE meals SET battles = battles + 1, wins = wins + 1 WHERE id = ?", (1,))
    # Assert that the changes were committed
    mock_conn.commit.assert_called_once()

def test_update_meal_stats_loss(mock_db_connection):
    """Test updating meal stats with a loss."""
    mock_conn, mock_cursor = mock_db_connection

    # Simulate an existing meal that hasn't been deleted
    mock_cursor.fetchone.return_value = (0,)
    
    # Run the function we want to test
    update_meal_stats(1, "loss")
    
    # Assert the correct SQL command was executed to update only battles
    mock_cursor.execute.assert_any_call("UPDATE meals SET battles = battles + 1 WHERE id = ?", (1,))
    # Assert that the changes were committed
    mock_conn.commit.assert_called_once()