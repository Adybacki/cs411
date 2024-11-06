import pytest
from unittest.mock import patch, Mock
from meal_max.models.battle_model import BattleModel
from meal_max.models.kitchen_model import Meal

@pytest.fixture
def battle_model():
    """Fixture to provide a BattleModel instance."""
    return BattleModel()

@pytest.fixture
def sample_meals():
    """Fixture to provide sample Meal instances for testing."""
    meal1 = Meal(id=1, meal="Spaghetti", cuisine="Italian", price=10.99, difficulty="MED")
    meal2 = Meal(id=2, meal="Lasagna", cuisine="Italian", price=12.99, difficulty="HIGH")
    return meal1, meal2

def test_prep_combatant(battle_model, sample_meals):
    """Test adding a combatant to the combatants list."""
    meal1, meal2 = sample_meals
    battle_model.prep_combatant(meal1)
    assert battle_model.get_combatants() == [meal1], "First combatant should be added"

    battle_model.prep_combatant(meal2)
    assert battle_model.get_combatants() == [meal1, meal2], "Second combatant should be added"

    # Check for exception when trying to add a third combatant
    with pytest.raises(ValueError, match="Combatant list is full"):
        battle_model.prep_combatant(meal1)

def test_get_combatants(battle_model, sample_meals):
    """Test retrieving the current list of combatants."""
    meal1, meal2 = sample_meals
    battle_model.prep_combatant(meal1)
    battle_model.prep_combatant(meal2)
    combatants = battle_model.get_combatants()
    assert combatants == [meal1, meal2], "Combatants should match the added meals"

def test_get_battle_score(battle_model, sample_meals):
    """Test calculating the battle score for a combatant."""
    meal1, meal2 = sample_meals
    score1 = battle_model.get_battle_score(meal1)
    score2 = battle_model.get_battle_score(meal2)
    assert score1 == (meal1.price * len(meal1.cuisine)) - 2, "Score calculation for meal1 is incorrect"
    assert score2 == (meal2.price * len(meal2.cuisine)) - 1, "Score calculation for meal2 is incorrect"

@patch("meal_max.models.battle_model.get_random", return_value=0.5)
@patch("meal_max.models.battle_model.update_meal_stats")
def test_battle(mock_update_meal_stats, mock_get_random, battle_model, sample_meals):
    """Test conducting a battle between two combatants."""
    meal1, meal2 = sample_meals
    battle_model.prep_combatant(meal1)
    battle_model.prep_combatant(meal2)

    # Force score difference and random number for predictable results
    with patch.object(battle_model, 'get_battle_score', side_effect=[70, 50]):
        winner = battle_model.battle()

    # Since the delta (20/100 = 0.2) is less than get_random (0.5), meal2 should win
    assert winner == meal2.meal, "meal2 should be the winner based on battle logic"
    mock_update_meal_stats.assert_any_call(meal2.id, 'win')
    mock_update_meal_stats.assert_any_call(meal1.id, 'loss')

def test_clear_combatants(battle_model, sample_meals):
    """Test clearing the combatants list."""
    meal1, meal2 = sample_meals
    battle_model.prep_combatant(meal1)
    battle_model.prep_combatant(meal2)

    assert len(battle_model.get_combatants()) == 2, "Combatants list should contain two meals"
    battle_model.clear_combatants()
    assert len(battle_model.get_combatants()) == 0, "Combatants list should be empty after clearing"
