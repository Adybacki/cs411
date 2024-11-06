import pytest
from meal_max.models.battle_model import BattleModel
from meal_max.models.kitchen_model import Meal

@pytest.fixture
def battle():
    """Fixture to provide a BattleModel instance."""
    return BattleModel()

@pytest.fixture
def meals():
    """Fixture to provide sample meals for testing."""
    return Meal("Spaghetti"), Meal("Lasagna")

def test_prep_meal_for_battle(battle):
    """Test preparing a meal for battle."""
    meal_name = "Spaghetti"
    result = battle.prep_meal_for_battle(meal_name)
    assert result is True, "Meal should be successfully prepared for battle"
    assert meal_name in battle.get_prepared_meals(), "Meal should be in the battle preparation list"

def test_remove_meal_from_battle(battle):
    """Test removing a meal from battle preparation."""
    meal_name = "Spaghetti"
    battle.prep_meal_for_battle(meal_name)
    result = battle.remove_meal_from_battle(meal_name)
    assert result is True, "Meal should be successfully removed from battle preparation"
    assert meal_name not in battle.get_prepared_meals(), "Meal should no longer be in the preparation list"

def test_get_meal_for_battle(battle):
    """Test retrieving a meal by name for battle."""
    meal_name = "Spaghetti"
    battle.prep_meal_for_battle(meal_name)
    meal = battle.get_meal_for_battle(meal_name)
    assert meal is not None, "Retrieved meal should not be None"
    assert meal.name == meal_name, "Retrieved meal name should match"

def test_assign_scores(battle, meals):
    """Test assigning scores to meals in battle."""
    meal1, meal2 = meals
    battle.prep_meal_for_battle(meal1)
    battle.prep_meal_for_battle(meal2)
    scores = battle.assign_scores()
    assert len(scores) == 2, "Scores should be assigned to both meals"
    assert scores[meal1] >= 0, "Score should be non-negative"
    assert scores[meal2] >= 0, "Score should be non-negative"

def test_determine_winner(battle, meals):
    """Test determining the winner between two meals."""
    meal1, meal2 = meals
    battle.prep_meal_for_battle(meal1)
    battle.prep_meal_for_battle(meal2)
    scores = {
        meal1: 10,
        meal2: 5
    }
    winner = battle.determine_winner(meal1, meal2, scores)
    assert winner == meal1, "The meal with the higher score should win"

def test_clear_battlefield(battle, meals):
    """Test clearing all prepared meals from the battlefield."""
    meal1, meal2 = meals
    battle.prep_meal_for_battle(meal1)
    battle.prep_meal_for_battle(meal2)
    battle.clear_battlefield()
    assert len(battle.get_prepared_meals()) == 0, "All meals should be removed from the preparation list"